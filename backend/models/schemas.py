from pydantic import BaseModel, Field
from typing import Optional


class AnalysisRequest(BaseModel):
    resume_text: str = Field(..., description="Extracted text from the resume")
    job_description: str = Field(..., description="Full job description text")
    generate_cover_letter: bool = Field(
        default=False, description="Whether to generate a tailored cover letter"
    )


class SkillGap(BaseModel):
    skill: str
    present_in_resume: bool
    importance: str  # "required" | "preferred"
    suggestion: Optional[str] = None


class AnalysisResult(BaseModel):
    match_score: int = Field(..., ge=0, le=100, description="ATS keyword match score 0-100")
    summary: str = Field(..., description="1-2 sentence overall assessment")
    matched_keywords: list[str]
    missing_keywords: list[str]
    skill_gaps: list[SkillGap]
    strengths: list[str]
    improvements: list[str]
    cover_letter: Optional[str] = None


class ParsedDocument(BaseModel):
    text: str
    page_count: Optional[int] = None
    source_type: str  # "pdf" | "docx" | "text"
