# parallel_generate.py
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List
from langchain.chains import RetrievalQA, StuffDocumentsChain, LLMChain
from langchain.prompts import PromptTemplate
from format_router import route_formats, template_for

def build_chain(llm, retriever, template_text: str) -> RetrievalQA:
    """
    Build a RetrievalQA chain with a manually constructed StuffDocumentsChain so that:
    - the document variable name is explicitly 'context', and
    - the PromptTemplate includes both 'question' and 'context'.

    This alignment avoids the common Pydantic validation error about missing
    'document_variable_name' in llm_chain input variables.
    """
    # Safely insert template_text (escape any literal {} in it if needed; assuming it's plain text here)
    safe_template_text = template_text.replace("{", "{{").replace("}", "}}")  # Escape for literal insertion

    # The prompt MUST include both placeholders: {question} and {context}
    prompt = PromptTemplate(
        input_variables=["question", "context"],
        template=(
            "You are a helpful assistant. Fill the following template clearly and concisely.\n\n"
            f"{safe_template_text}\n\n"
            "User Question: {{question}}\n\n"
            "Context:\n{{context}}\n"
        ).format(safe_template_text=safe_template_text),  # Use .format() to avoid f-string parsing issues with {}
    )

    # Inner LLM chain that actually formats the answer
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Wrap with StuffDocumentsChain and explicitly name the docs variable
    stuff_chain = StuffDocumentsChain(
        llm_chain=llm_chain,
        document_variable_name="context",
    )

    # RetrievalQA with our custom combine_docs_chain
    qa = RetrievalQA(
        retriever=retriever,
        combine_documents_chain=stuff_chain,
    )
    return qa

def score_output(label: str, text: str) -> float:
    """Tiny heuristic: prefer outputs that filled more lines of the template."""
    filled = sum(1 for line in text.splitlines() if ":" in line and line.strip().split(":")[1].strip())
    bonus = 0.2 if label in ("candidate_info","invoice","research_paper","ml_pipeline") else 0.0
    return filled + bonus

def generate_parallel(query: str, llm, retriever, max_candidates: int = 3) -> Dict:
    labels = route_formats(query, top_k=max_candidates)
    tasks = {}
    with ThreadPoolExecutor(max_workers=max_candidates) as ex:
        for label in labels:
            tmpl = template_for(label)
            chain = build_chain(llm, retriever, tmpl)
            fut = ex.submit(lambda: chain.run(query))
            tasks[fut] = (label, tmpl)
    best = {"label": None, "text": "", "score": -1, "template": ""}
    for fut in as_completed(tasks):
        label, tmpl = tasks[fut]
        try:
            text = fut.result()
            s = score_output(label, text or "")
            if s > best["score"]:
                best = {"label": label, "text": text, "score": s, "template": tmpl}
        except Exception as e:
            # ignore failed branch
            pass
    return best