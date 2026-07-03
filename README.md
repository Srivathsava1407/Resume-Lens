# ResumeLens 🔍

An AI-powered resume and job description analyzer built with FastAPI and Google Gemini. Upload your resume, paste a job description, and get an instant ATS match score, keyword gap analysis, skill assessment, and optional tailored cover letter — all in your browser.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-4285F4?logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## What it does

- **ATS Match Score** — rates how well your resume matches a job description on a 0–100 scale
- **Keyword Analysis** — shows exactly which keywords from the JD are present and which are missing
- **Skill Gap Breakdown** — lists required and preferred skills with an actionable suggestion for each gap
- **Strengths & Improvements** — specific, honest feedback on what works and what to fix
- **Cover Letter Generator** — optionally generates a tailored 3-paragraph cover letter for the role
- **Multi-format Support** — accepts PDF, DOCX, or plain text resumes

---

## Demo

Upload your resume (PDF/DOCX/TXT) or paste it as text, paste the job description, and hit **Analyze Match**.

```
Score: 78/100
Matched: Python, FastAPI, REST API, Git, SQL
Missing: Docker, AWS, Kubernetes

Strengths:
→ Strong Python background matches the core requirement
→ REST API experience directly relevant to the role

Improvements:
→ Add containerization experience to your projects section
→ Mention any cloud platform usage, even personal projects
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Uvicorn |
| AI | Google Gemini 2.5 Flash (`google-generativeai`) |
| Document Parsing | pdfplumber (PDF), python-docx (DOCX) |
| Validation | Pydantic v2 |
| Frontend | Vanilla JS, Jinja2 templates, SVG |
| Testing | pytest, pytest-asyncio |

---

## Project Structure

```
resume-lens/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── routers/
│   │   └── analyze.py       # POST /api/analyze endpoint
│   ├── services/
│   │   ├── ai_service.py    # Gemini API integration + prompt engineering
│   │   └── parser.py        # PDF / DOCX / TXT text extraction
│   └── models/
│       └── schemas.py       # Pydantic request & response models
├── frontend/
│   ├── templates/
│   │   └── index.html       # Single-page UI
│   └── static/
│       └── main.js          # Fetch, drag-and-drop, results rendering
├── tests/
│   └── test_analyze.py      # Endpoint tests with mocked AI calls
├── .env.example             # API key template
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- A free Google Gemini API key — get one at [aistudio.google.com](https://aistudio.google.com) (no credit card required)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/Srivathsava1407/Resume-Lens.git
cd Resume-Lens
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set your API key**

Copy the example env file and add your key:
```bash
cp .env.example .env
# then open .env and set GOOGLE_API_KEY=your_key_here
```

On Windows PowerShell you can set it directly in your terminal instead:
```powershell
$env:GOOGLE_API_KEY="your_gemini_api_key_here"
```

**4. Run the server**
```bash
python -m uvicorn backend.main:app --reload
```

**5. Open in your browser**
```
http://localhost:8000
```

---

## Running Tests

Tests use mocked AI calls so no API key is needed to run them:
```bash
pytest tests/ -v
```

---

## How it works

1. **User submits** a resume (file upload or pasted text) and a job description via the browser
2. **FastAPI router** validates inputs — returns HTTP 400 if required fields are missing
3. **Parser service** extracts plain text from PDF, DOCX, or TXT files using format-specific libraries
4. **AI service** builds a structured prompt and calls Gemini with `response_mime_type: application/json` to enforce machine-readable output
5. **Pydantic models** validate and deserialize the JSON response into typed Python objects
6. **Frontend** renders the animated SVG score ring, keyword tags, skill gaps, and feedback — no page reload required

---

## Future Improvements

- [ ] Persistent storage with SQLite to track multiple job applications over time
- [ ] Streaming responses via Server-Sent Events to show results token-by-token
- [ ] Rate limiting per user with `slowapi` to protect API quota
- [ ] Resume version comparison — upload two versions and see which scores higher

---

## License

MIT — free to use, modify, and distribute.
