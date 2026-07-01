import json
import os
import google.generativeai as genai
from fastapi import HTTPException
from backend.models.schemas import AnalysisRequest, AnalysisResult, SkillGap

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
client = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={"response_mime_type": "application/json"},
)

ANALYSIS_SYSTEM_PROMPT = """You are an expert ATS (Applicant Tracking System) and career coach.
Analyze resumes against job descriptions and return ONLY valid JSON — no preamble, no markdown fences.

Your JSON must exactly match this schema:
{
  "match_score": <integer 0-100>,
  "summary": "<1-2 sentence overall assessment>",
  "matched_keywords": ["<keyword>", ...],
  "missing_keywords": ["<keyword>", ...],
  "skill_gaps": [
    {
      "skill": "<skill name>",
      "present_in_resume": <true|false>,
      "importance": "<required|preferred>",
      "suggestion": "<brief actionable suggestion or null>"
    }
  ],
  "strengths": ["<strength>", ...],
  "improvements": ["<improvement>", ...],
  "cover_letter": "<full cover letter text or null>"
}

Scoring guide:
- 80-100: Strong match, most keywords present
- 60-79: Good match, some gaps
- 40-59: Moderate match, notable gaps
- 0-39: Weak match, significant rework needed

Be specific, actionable, and honest. Do NOT inflate scores."""


def _build_user_prompt(request: AnalysisRequest) -> str:
    cover_letter_instruction = (
        "Also generate a tailored, professional cover letter for this role (3 paragraphs)."
        if request.generate_cover_letter
        else "Set cover_letter to null."
    )

    return f"""RESUME:
{request.resume_text}

---

JOB DESCRIPTION:
{request.job_description}

---

{cover_letter_instruction}

Return the JSON analysis now."""


async def analyze_resume(request: AnalysisRequest) -> AnalysisResult:
    full_prompt = ANALYSIS_SYSTEM_PROMPT + "\n\n" + _build_user_prompt(request)
    response = client.generate_content(full_prompt)
    raw_text = response.text.strip()

    # Strip markdown fences as a safety net
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"Gemini returned: {raw_text[:300]}")

    skill_gaps = [SkillGap(**sg) for sg in data.get("skill_gaps", [])]

    return AnalysisResult(
        match_score=data["match_score"],
        summary=data["summary"],
        matched_keywords=data.get("matched_keywords", []),
        missing_keywords=data.get("missing_keywords", []),
        skill_gaps=skill_gaps,
        strengths=data.get("strengths", []),
        improvements=data.get("improvements", []),
        cover_letter=data.get("cover_letter"),
    )