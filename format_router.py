# format_router.py
from typing import List, Dict
from transformers import pipeline

# -------------  A. Labels (add more anytime)  -------------
FORMAT_LABELS = [
    "candidate_info", "email_reply", "summary", "explanation", "report",
    "project_plan", "business_proposal", "meeting_minutes", "faq",
    "dataset_description", "ml_pipeline", "research_paper", "invoice",
    "policy_document", "cv_resume", "cover_letter", "presentation_outline",
    "video_script", "marketing_plan", "timeline", "comparison_table",
    "lab_report", "experiment_result", "sustainability_report", "remote_sensing"
]

# -------------  B. Templates  -------------
TEMPLATES: Dict[str, str] = {
    "candidate_info": """🧾 CANDIDATE INFORMATION
1. Name:
2. Gender:
3. Father's Name:
4. Mother's Name:
5. Mobile Number:
6. Email:
7. State:
8. District:
9. Sub-Division:
10. Block:
11. Village/Town:
12. Post Office:
13. Police Station:
14. Occupation:
15. Caste:
16. Sub-Caste:
17. Date of Application:
18. Notes:
""",
    "email_reply": """📧 PROFESSIONAL EMAIL REPLY
To: [Recipient Name]
Subject: [Auto]
Body:
[Write a concise, polite and professional reply here.]

Best regards,
Rahul Kumar
Indian Institute of Science, Bangalore
""",
    "summary": """📝 DOCUMENT SUMMARY
Title:
Main Points:
1.
2.
3.
Conclusion:
""",
    "explanation": """📘 EXPLANATION
Topic:
Definition:
Detailed Explanation:
Example:
""",
    "report": """📊 REPORT
Title:
Objective:
Method:
Results:
Conclusion:
Recommendations:
""",
    "project_plan": """📅 PROJECT PLAN
Goal:
Phases:
Milestones:
Timeline:
Risks & Mitigations:
Deliverables:
""",
    "business_proposal": """💼 BUSINESS PROPOSAL
Problem:
Solution:
Target Market:
Business Model:
Go-to-Market:
Budget:
ROI:
""",
    "meeting_minutes": """🗓️ MEETING MINUTES
Date:
Participants:
Agenda:
Discussion Points:
Decisions:
Action Items (Owner, Deadline):
""",
    "faq": """❓ FAQ
Q1:
A1:
Q2:
A2:
Q3:
A3:
""",
    "dataset_description": """🧾 DATASET DESCRIPTION
Name:
Rows:
Columns (with types):
Target Variable:
Missing Values:
Notes:
""",
    "ml_pipeline": """🤖 ML PIPELINE
Problem Type:
Data:
Features:
Model:
Training Setup:
Metrics:
Next Steps:
""",
    "research_paper": """📚 RESEARCH PAPER SNAPSHOT
Title:
Authors:
Journal:
DOI:
Abstract (2-3 lines):
Key Findings:
Conclusion:
""",
    "invoice": """🧾 INVOICE
Bill To:
Items (Name, Qty, Rate):
Subtotal:
Tax:
Total:
Payment Terms:
""",
    "policy_document": """📜 POLICY DOCUMENT
Scope:
Definitions:
Policy:
Responsibilities:
Compliance:
Review Cycle:
""",
    "cv_resume": """📄 RESUME OUTLINE
Name:
Contact:
Summary:
Skills:
Experience:
Projects:
Education:
""",
    "cover_letter": """✉️ COVER LETTER
Greeting:
Opening (Role + Fit):
Relevant Experience:
Motivation:
Closing:
Signature:
""",
    "presentation_outline": """🖥️ PRESENTATION OUTLINE
Title:
Slide 1 (Intro):
Slide 2 (Problem):
Slide 3 (Solution):
Slide 4 (Evidence):
Slide 5 (Conclusion/CTA):
""",
    "video_script": """🎬 VIDEO SCRIPT
Hook:
Context:
Main Points:
Demo/Example:
Call-to-Action:
""",
    "marketing_plan": """📣 MARKETING PLAN
Audience:
Positioning:
Channels:
Budget:
KPIs:
Timeline:
""",
    "timeline": """🗓️ TIMELINE
Phase 1:
Phase 2:
Phase 3:
Milestones:
Dependencies:
""",
    "comparison_table": """📊 COMPARISON
Criteria:
Option A:
Option B:
Pros/Cons:
Recommendation:
""",
    "lab_report": """🔬 LAB REPORT
Objective:
Apparatus:
Procedure:
Observations:
Results:
Conclusion:
""",
    "experiment_result": """🧪 EXPERIMENT RESULTS
Setup:
Variables:
Trials:
Observations:
Result Summary:
""",
    "sustainability_report": """🌱 SUSTAINABILITY REPORT
Boundary:
Energy:
Emissions:
Water:
Waste:
Recommendations:
""",
    "remote_sensing": """🛰️ REMOTE SENSING OUTPUT
AOI:
Date Range:
Sensors/Bands:
Indices (NDVI/NDWI/NDBI):
Findings:
Map Notes:
""",
}

# -------------  C. Zero-shot router  -------------
_ZS = None
def _get_zero_shot():
    global _ZS
    if _ZS is None:
        _ZS = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    return _ZS

def route_formats(query: str, top_k: int = 3) -> List[str]:
    zs = _get_zero_shot()
    res = zs(query, candidate_labels=FORMAT_LABELS, multi_label=True)
    # Sort by scores desc and pick top_k
    pairs = sorted(zip(res["labels"], res["scores"]), key=lambda x: x[1], reverse=True)
    return [label for label, _ in pairs[:top_k]]

def template_for(label: str) -> str:
    return TEMPLATES.get(label, "💬 GENERAL RESPONSE\nAnswer:\n")
