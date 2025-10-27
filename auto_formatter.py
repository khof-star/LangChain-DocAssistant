# auto_formatter.py
def detect_format_type(query: str) -> str:
    q = query.lower()
    categories = {
        "candidate_info": ["candidate", "application", "village", "bihar", "sheikhpura", "form", "personal detail"],
        "email_reply": ["email", "reply", "mail", "draft", "compose", "message"],
        "summary": ["summary", "summarize", "abstract", "main points", "gist"],
        "explanation": ["explain", "definition", "concept", "meaning", "describe"],
        "research_paper": ["research", "doi", "journal", "conclusion", "abstract"],
        "project_plan": ["project", "plan", "milestone", "timeline", "phase"],
        "business_proposal": ["business", "proposal", "pitch", "investor"],
        "report": ["report", "analysis", "findings", "conclusion"],
        "meeting_minutes": ["meeting", "minutes", "discussion", "summary"],
        "code_explanation": ["code", "python", "error", "debug", "explain code"],
        "blog_post": ["blog", "article", "content", "post"],
        "social_media_caption": ["instagram", "tweet", "caption", "reel", "social"],
        "product_description": ["product", "features", "specification", "description"],
        "resume": ["resume", "cv", "curriculum vitae"],
        "cover_letter": ["cover letter", "application letter", "job apply"],
        "press_release": ["press release", "announcement"],
        "newsletter": ["newsletter", "update", "bulletin"],
        "faq": ["faq", "frequently asked"],
        "interview_question": ["interview", "question", "answers"],
        "lesson_plan": ["lesson", "teaching", "class plan"],
        "exam_question": ["exam", "test", "question paper"],
        "academic_note": ["note", "study", "lecture"],
        "data_summary": ["data", "dataset", "summary"],
        "statistical_analysis": ["anova", "regression", "correlation", "statistical"],
        "graph_description": ["graph", "plot", "chart", "visualization"],
        "financial_report": ["financial", "balance sheet", "income", "profit"],
        "invoice": ["invoice", "bill", "payment"],
        "contract": ["contract", "agreement", "terms"],
        "legal_notice": ["legal", "notice", "case", "law"],
        "policy_document": ["policy", "guideline", "protocol"],
        "research_objectives": ["objective", "goal", "aim"],
        "experiment_result": ["experiment", "result", "observation"],
        "lab_report": ["lab", "test", "observation", "conclusion"],
        "scientific_analysis": ["scientific", "study", "hypothesis"],
        "medical_report": ["patient", "medical", "diagnosis", "symptom"],
        "prescription": ["prescription", "medicine", "drug"],
        "recipe": ["recipe", "ingredients", "cooking", "steps"],
        "instruction_manual": ["instruction", "guide", "how to", "manual"],
        "algorithm_description": ["algorithm", "flowchart", "steps"],
        "pseudo_code": ["pseudo code", "algorithm", "logic"],
        "app_specification": ["app", "feature", "functionality"],
        "software_requirement": ["srs", "software requirement", "system requirement"],
        "ui_design": ["ui", "ux", "interface", "layout"],
        "data_model": ["schema", "entity", "database", "er diagram"],
        "api_documentation": ["api", "endpoint", "response", "request"],
        "architecture_diagram": ["architecture", "system design"],
        "network_topology": ["network", "router", "connection"],
        "iot_project": ["iot", "sensor", "arduino"],
        "ml_pipeline": ["machine learning", "model", "training", "accuracy"],
        "deep_learning": ["cnn", "rnn", "transformer", "neural network"],
        "dataset_description": ["dataset", "features", "columns"],
        "evaluation_report": ["evaluation", "metrics", "performance"],
        "comparison_table": ["compare", "versus", "difference"],
        "timeline": ["timeline", "schedule", "gantt"],
        "budget_plan": ["budget", "cost", "expense"],
        "marketing_plan": ["marketing", "strategy", "campaign"],
        "sales_report": ["sales", "customer", "revenue"],
        "market_analysis": ["market", "trend", "competition"],
        "user_feedback": ["feedback", "review", "rating"],
        "customer_support": ["support", "complaint", "service ticket"],
        "training_material": ["training", "tutorial", "guide"],
        "quiz": ["quiz", "mcq", "questionnaire"],
        "survey_result": ["survey", "poll", "responses"],
        "policy_brief": ["policy brief", "recommendation"],
        "technical_specification": ["technical", "specification", "details"],
        "maintenance_report": ["maintenance", "repair", "status"],
        "incident_report": ["incident", "accident", "issue"],
        "environmental_report": ["environmental", "impact", "assessment"],
        "sustainability_report": ["sustainability", "carbon", "energy"],
        "urban_planning": ["urban", "infrastructure", "city"],
        "transport_study": ["transport", "traffic", "mobility"],
        "cycling_safety": ["cycling", "bicycle", "road safety"],
        "health_assessment": ["health", "commuter", "well-being"],
        "agriculture_report": ["crop", "soil", "ndvi", "vegetation"],
        "remote_sensing": ["landsat", "sentinel", "earth engine"],
        "ai_research": ["agi", "llm", "ai system", "cognitive"],
        "startup_pitch": ["startup", "idea", "funding", "pitch deck"],
        "business_model_canvas": ["canvas", "business model"],
        "risk_assessment": ["risk", "hazard", "safety"],
        "security_report": ["cybersecurity", "vulnerability", "penetration"],
        "resume_review": ["resume review", "cv improvement"],
        "job_description": ["job description", "jd", "role"],
        "internship_summary": ["internship", "experience", "learning"],
        "presentation_outline": ["presentation", "slide", "ppt"],
        "speech_script": ["speech", "script", "talk"],
        "video_script": ["video", "youtube", "narration"],
        "advertisement_copy": ["ad", "advertisement", "copywriting"],
        "seo_content": ["seo", "keyword", "meta description"],
        "product_review": ["review", "rating", "feedback"],
        "research_proposal": ["proposal", "research topic"],
        "thesis_outline": ["thesis", "dissertation", "outline"],
        "data_cleaning": ["clean", "preprocess", "data quality"],
        "visualization_description": ["plot", "graph", "visual"],
        "simulation_result": ["simulation", "result", "output"],
        "performance_report": ["performance", "efficiency", "output"],
        "optimization_result": ["optimization", "parameter", "result"],
        "mathematical_derivation": ["derive", "formula", "equation"],
        "physics_experiment": ["force", "velocity", "momentum"],
        "chemistry_report": ["compound", "reaction", "molecule"],
        "architecture_plan": ["building", "design", "blueprint"],
        "civil_engineering": ["bridge", "structure", "load"],
        "electrical_system": ["circuit", "voltage", "power"],
        "mechanical_design": ["engine", "gear", "pump"],
        "robotics": ["robot", "actuator", "servo", "path"],
        "aerospace": ["rocket", "flight", "aero"],
        "marine_engineering": ["ship", "propeller", "marine"],
    }

    for k, keywords in categories.items():
        if any(word in q for word in keywords):
            return k
    return "general"


def get_format_prompt(format_type: str):
    templates = {
        "candidate_info": """
🧾 CANDIDATE INFORMATION
1. Name:
2. Gender:
3. Father's Name:
4. Mother's Name:
5. Mobile Number:
6. Email:
7. Address:
8. Village/Town:
9. District:
10. State:
11. Date of Application:
12. Notes:
""",
        "email_reply": """
📧 PROFESSIONAL EMAIL
To: [Recipient]
Subject: [Auto-detected]
Body:
[Professional, polite, concise email text]
Best regards,
[Your Name]
""",
        "summary": """
📝 DOCUMENT SUMMARY
Title:
Main Topics:
1.
2.
3.
Conclusion:
""",
        "explanation": """
📘 EXPLANATION
Topic:
Definition:
Explanation:
Examples:
""",
        "report": """
📊 REPORT FORMAT
Title:
Objective:
Method:
Results:
Conclusion:
""",
        "project_plan": """
📅 PROJECT PLAN
Goal:
Timeline:
Phases:
Milestones:
Deliverables:
""",
        "business_proposal": """
💼 BUSINESS PROPOSAL
Idea:
Problem Statement:
Solution:
Market:
Budget:
Expected ROI:
""",
        "research_paper": """
📚 RESEARCH PAPER SUMMARY
Title:
Authors:
Journal:
DOI:
Abstract:
Key Findings:
Conclusion:
""",
        "meeting_minutes": """
🗓️ MEETING MINUTES
Date:
Participants:
Agenda:
Discussion Points:
Decisions:
Action Items:
""",
        # ... (add similar concise blocks up to 100+ using same pattern)
        "general": """
💬 GENERAL ANSWER
Response:
"""
    }
    return templates.get(format_type, templates["general"])
