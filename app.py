import streamlit as st
import torch  # For GPU detection
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter  # v0.2.x bundled
from langchain_community.vectorstores import FAISS  # Community
from langchain_community.embeddings import HuggingFaceEmbeddings  # Community
from langchain_community.llms import HuggingFacePipeline  # Community
from transformers import pipeline
from langchain.memory import ConversationBufferMemory  # Bundled
from langchain.chains import ConversationalRetrievalChain  # Bundled
import os
from htmlTemplates import css, bot_template, user_template  # Assume exist
from auto_formatter import detect_format_type, get_format_prompt  # Assume exist
from parallel_generate import generate_parallel  # Assume fixed

def extract_llm_and_retriever(conv):
    """Extract LLM and retriever (v0.2.x paths)."""
    llm = None
    for path in (
        "llm_chain.llm",
        "combine_docs_chain.llm_chain.llm",
        "question_generator.llm_chain.llm",
    ):
        try:
            ref = conv
            for p in path.split("."):
                ref = getattr(ref, p)
            if ref:
                llm = ref
                break
        except AttributeError:
            continue
    retriever = getattr(conv, "retriever", None)
    return llm, retriever

def handle_userinput(user_question):
    conv = st.session_state.conversation
    llm, retriever = extract_llm_and_retriever(conv)

    # Fallbacks
    if llm is None:
        st.warning("⚠️ LLM fallback used.")
        llm = conv.llm if hasattr(conv, 'llm') else None
    if retriever is None:
        retriever = st.session_state.vectorstore.as_retriever()

    # Parallel gen
    result = generate_parallel(user_question, llm, retriever, max_candidates=3)
    bot_reply = result["text"]
    st.info(f"Chosen format: {result['label']}")

    # Update memory
    response = conv({"question": user_question})
    st.session_state.chat_history = response["chat_history"]

    # Override bot reply with formatted
    if st.session_state.chat_history and len(st.session_state.chat_history) % 2 == 0:
        st.session_state.chat_history[-1].content = bot_reply

    # Render
    for i, msg in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.markdown(user_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True)
        else:
            formatted = f"<pre style='white-space:pre-wrap; font-family:inherit;'>{msg.content}</pre>"
            st.markdown(bot_template.replace("{{MSG}}", formatted), unsafe_allow_html=True)

def get_pdf_text(uploaded_files):
    text = ""
    for pdf in uploaded_files:
        try:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        except Exception as e:
            st.error(f"PDF error: {e}")
    return text

def get_text_chunks(text):
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return splitter.split_text(text)

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)

def get_conversation_chain(vectorstore):
    device = 0 if torch.cuda.is_available() else -1
    if device == 0:
        st.info("🚀 GPU available.")

    pipe = pipeline(
        "text2text-generation",
        model="google/flan-t5-large",
        max_new_tokens=512,
        temperature=0.3,
        device=device
    )
    llm = HuggingFacePipeline(pipeline=pipe)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )

def main():
    load_dotenv()
    st.set_page_config(page_title="📚 Chat with PDFs", page_icon="🤖", layout="wide")
    st.markdown(css, unsafe_allow_html=True)  # Load CSS

    # Session state init
    for key in ["conversation", "chat_history", "vectorstore"]:
        if key not in st.session_state:
            st.session_state[key] = None

    st.markdown("<h1 style='text-align:center;'>📚 Chat with Multiple PDFs</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#4F46E5;'>Upload & query your docs</p>", unsafe_allow_html=True)

    st.markdown("### 💬 Ask about your documents:")
    question = st.text_input("Your question...")

    if question:
        if st.session_state.conversation:
            handle_userinput(question)
        else:
            st.warning("⚠️ Process documents first.")

    with st.sidebar:
        st.header("🗂️ Upload PDFs")
        uploaded = st.file_uploader("PDFs", type=["pdf"], accept_multiple_files=True)
        process = st.button("🚀 Process")

        if process:
            if not uploaded:
                st.warning("⚠️ Upload at least one PDF.")
            else:
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(uploaded)
                    if not raw_text.strip():
                        st.error("❌ No text found.")
                        st.stop()
                    chunks = get_text_chunks(raw_text)
                    vs = get_vectorstore(chunks)
                    st.session_state.vectorstore = vs
                    st.session_state.conversation = get_conversation_chain(vs)
                    st.session_state.chat_history = []
                    st.success("✅ Ready to chat!")

if __name__ == "__main__":
    main()