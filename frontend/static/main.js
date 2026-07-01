const fileInput = document.getElementById('fileInput');
const fileDrop = document.getElementById('fileDrop');
const resumeText = document.getElementById('resumeText');

// Drag-and-drop handling
fileDrop.addEventListener('dragover', e => { e.preventDefault(); fileDrop.classList.add('drag-over'); });
fileDrop.addEventListener('dragleave', () => fileDrop.classList.remove('drag-over'));
fileDrop.addEventListener('drop', e => {
  e.preventDefault();
  fileDrop.classList.remove('drag-over');
  if (e.dataTransfer.files.length) {
    fileInput.files = e.dataTransfer.files;
    fileDrop.querySelector('div').textContent = `✓ ${e.dataTransfer.files[0].name}`;
  }
});

fileInput.addEventListener('change', () => {
  if (fileInput.files.length) {
    fileDrop.querySelector('div').textContent = `✓ ${fileInput.files[0].name}`;
  }
});

async function runAnalysis() {
  const jobDesc = document.getElementById('jobDesc').value.trim();
  const generateCL = document.getElementById('coverLetter').checked;
  const btn = document.getElementById('analyzeBtn');

  if (!jobDesc) return alert('Please paste a job description.');
  if (!fileInput.files.length && !resumeText.value.trim()) {
    return alert('Please upload a resume file or paste your resume text.');
  }

  // Show results panel + loading
  const resultsPanel = document.getElementById('results');
  resultsPanel.classList.add('visible');
  document.getElementById('loadingState').style.display = 'block';
  document.getElementById('resultContent').style.display = 'none';
  btn.disabled = true;
  resultsPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });

  const fd = new FormData();
  fd.append('job_description', jobDesc);
  fd.append('generate_cover_letter', generateCL);
  if (fileInput.files.length) fd.append('resume_file', fileInput.files[0]);
  else fd.append('resume_text', resumeText.value.trim());

  try {
    const resp = await fetch('/api/analyze', { method: 'POST', body: fd });
    if (!resp.ok) {
      const err = await resp.json();
      throw new Error(err.detail || 'Analysis failed');
    }
    const data = await resp.json();
    renderResults(data);
  } catch (e) {
    document.getElementById('loadingState').innerHTML = `<p style="color:#dc2626">Error: ${e.message}</p>`;
  } finally {
    btn.disabled = false;
  }
}

function scoreColor(score) {
  if (score >= 80) return '#16a34a';
  if (score >= 60) return '#d97706';
  return '#dc2626';
}

function renderResults(data) {
  document.getElementById('loadingState').style.display = 'none';
  const content = document.getElementById('resultContent');
  content.style.display = 'block';

  const color = scoreColor(data.match_score);
  const circumference = 2 * Math.PI * 30;
  const offset = circumference - (data.match_score / 100) * circumference;

  const matchedTags = (data.matched_keywords || []).slice(0, 12)
    .map(k => `<span class="tag matched">${k}</span>`).join('');
  const missingTags = (data.missing_keywords || []).slice(0, 12)
    .map(k => `<span class="tag missing">${k}</span>`).join('');

  const strengthItems = (data.strengths || []).map(s => `<li>${s}</li>`).join('');
  const improvementItems = (data.improvements || []).map(i => `<li>${i}</li>`).join('');

  const coverLetterSection = data.cover_letter ? `
    <div class="list-section" style="grid-column:1/-1">
      <h3>Generated Cover Letter</h3>
      <div class="cover-letter">${data.cover_letter}</div>
    </div>` : '';

  content.innerHTML = `
    <div class="score-ring">
      <div class="ring-wrap">
        <svg width="80" height="80" viewBox="0 0 80 80">
          <circle cx="40" cy="40" r="30" fill="none" stroke="#e7e5e4" stroke-width="8"/>
          <circle cx="40" cy="40" r="30" fill="none" stroke="${color}" stroke-width="8"
            stroke-dasharray="${circumference}" stroke-dashoffset="${offset}"
            stroke-linecap="round" style="transition: stroke-dashoffset 1s ease"/>
        </svg>
        <div class="ring-score" style="color:${color}">${data.match_score}</div>
      </div>
      <div class="summary-text">${data.summary}</div>
    </div>

    <div class="results-grid">
      <div>
        <h3 style="font-size:0.85rem;font-weight:600;color:#78716c;text-transform:uppercase;letter-spacing:0.04em;margin-bottom:0.5rem">Matched Keywords</h3>
        <div class="tags">${matchedTags || '<span style="color:#a8a29e;font-size:0.85rem">None found</span>'}</div>
      </div>
      <div>
        <h3 style="font-size:0.85rem;font-weight:600;color:#78716c;text-transform:uppercase;letter-spacing:0.04em;margin-bottom:0.5rem">Missing Keywords</h3>
        <div class="tags">${missingTags || '<span style="color:#a8a29e;font-size:0.85rem">None — great coverage!</span>'}</div>
      </div>

      <div class="list-section">
        <h3>Strengths</h3>
        <ul>${strengthItems}</ul>
      </div>
      <div class="list-section">
        <h3>Suggested Improvements</h3>
        <ul>${improvementItems}</ul>
      </div>

      ${coverLetterSection}
    </div>
  `;
}
