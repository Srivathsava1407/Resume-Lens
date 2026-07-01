from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from backend.services.parser import parse_document
from backend.services.ai_service import analyze_resume
from backend.models.schemas import AnalysisRequest, AnalysisResult

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyze", response_model=AnalysisResult)
async def analyze(
    job_description: str = Form(...),
    generate_cover_letter: bool = Form(default=False),
    resume_file: UploadFile = File(None),
    resume_text: str = Form(default=""),
):
    """
    Main analysis endpoint. Accepts either a file upload or raw resume text,
    plus a job description, and returns a structured analysis.
    """
    # Resolve resume text from file or direct input
    if resume_file and resume_file.filename:
        parsed = await parse_document(resume_file)
        final_resume_text = parsed.text
    elif resume_text.strip():
        final_resume_text = resume_text.strip()
    else:
        raise HTTPException(
            status_code=400,
            detail="Provide either a resume file or paste resume text.",
        )

    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    request = AnalysisRequest(
        resume_text=final_resume_text,
        job_description=job_description.strip(),
        generate_cover_letter=generate_cover_letter,
    )

    return await analyze_resume(request)


@router.get("/health")
async def health():
    return {"status": "ok"}
