import streamlit as st
import pickle
import re
import os
from pdfminer.high_level import extract_text as pdf_extract_text

# ─────────────────────────────────────────────────────────────────────────────
#  Page Config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Resume Intelligence",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
#  Global Styling — Pure Dark Mode
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

  :root {
    --bg:        #0d0d0f;
    --surface:   #141417;
    --surface2:  #1c1c21;
    --border:    #2a2a32;
    --accent:    #e8622a;
    --accent2:   #f0a070;
    --gold:      #c9a84c;
    --green:     #3ecf8e;
    --blue:      #4a9eff;
    --text:      #e8e6e1;
    --muted:     #6b6875;
    --radius:    12px;
  }

  /* ── Reset & base ── */
  html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background: var(--bg) !important;
    color: var(--text) !important;
  }
  .main .block-container { padding: 2rem 2.5rem; max-width: 1100px; }
  .stApp { background: var(--bg) !important; }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
  }
  [data-testid="stSidebar"] * { color: var(--text) !important; }
  [data-testid="stSidebar"] .stRadio label {
    font-size: .88rem !important;
    padding: .4rem .2rem !important;
    transition: color .15s;
  }
  [data-testid="stSidebar"] hr { border-color: var(--border) !important; }
  [data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    color: var(--muted) !important;
    font-size: .7rem !important;
    letter-spacing: .12em;
    text-transform: uppercase;
    font-weight: 600;
  }

  /* ── Sidebar brand ── */
  .sidebar-brand {
    padding: 1.2rem 0 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.2rem;
  }
  .sidebar-brand-name {
    font-size: 1.3rem;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -.01em;
  }
  .sidebar-brand-dot { color: var(--accent); }

  /* ── Hero ── */
  .hero {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
  }
  .hero::after {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(232,98,42,.18) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
  }
  .hero-eyebrow {
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: .2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: .6rem;
    font-family: 'DM Mono', monospace;
  }
  .hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1.1;
    margin: 0 0 .75rem;
    letter-spacing: -.02em;
  }
  .hero-title span { color: var(--accent); }
  .hero-sub {
    font-size: .9rem;
    color: var(--muted);
    max-width: 460px;
    line-height: 1.65;
    font-weight: 400;
  }

  /* ── Upload zone ── */
  .upload-zone {
    background: var(--surface);
    border: 1.5px dashed var(--border);
    border-radius: var(--radius);
    padding: 3rem 2rem;
    text-align: center;
    margin-top: 1rem;
    transition: border-color .2s;
  }
  .upload-zone:hover { border-color: var(--accent); }
  .upload-icon { font-size: 2.2rem; margin-bottom: .6rem; }
  .upload-title { font-weight: 700; font-size: 1.05rem; margin-bottom: .3rem; }
  .upload-hint { font-size: .82rem; color: var(--muted); }

  /* ── Status strip ── */
  .status-strip {
    display: flex;
    align-items: center;
    gap: .6rem;
    background: rgba(62, 207, 142, .08);
    border: 1px solid rgba(62, 207, 142, .25);
    border-radius: 8px;
    padding: .65rem 1rem;
    color: var(--green);
    font-size: .88rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    font-family: 'DM Mono', monospace;
  }

  /* ── Section title ── */
  .section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -.01em;
    margin: 1.8rem 0 1rem;
    display: flex;
    align-items: center;
    gap: .5rem;
  }
  .section-title::before {
    content: '';
    display: inline-block;
    width: 3px;
    height: 1.1em;
    background: var(--accent);
    border-radius: 2px;
    flex-shrink: 0;
  }

  /* ── Result card ── */
  .result-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem 1.8rem;
    margin-bottom: 1rem;
  }
  .result-card.green { border-left: 3px solid var(--green); }
  .result-card.blue  { border-left: 3px solid var(--blue); }
  .result-label {
    font-size: .65rem;
    font-weight: 700;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    margin-bottom: .5rem;
  }
  .result-value {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -.01em;
  }

  /* ── Info block ── */
  .info-block {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    margin-bottom: .6rem;
  }
  .info-key {
    font-size: .63rem;
    font-weight: 700;
    letter-spacing: .15em;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
  }
  .info-val {
    font-size: .97rem;
    font-weight: 600;
    color: var(--text);
    margin-top: .3rem;
    word-break: break-all;
  }

  /* ── Badge ── */
  .badge {
    display: inline-block;
    background: rgba(232,98,42,.1);
    color: var(--accent2);
    border: 1px solid rgba(232,98,42,.25);
    border-radius: 20px;
    padding: 3px 11px;
    font-size: .76rem;
    font-weight: 600;
    margin: 3px;
  }
  .edu-tag {
    display: inline-block;
    background: rgba(62,207,142,.08);
    color: var(--green);
    border: 1px solid rgba(62,207,142,.2);
    border-radius: 20px;
    padding: 3px 11px;
    font-size: .76rem;
    font-weight: 600;
    margin: 3px;
  }

  /* ── Divider ── */
  .divider { height: 1px; background: var(--border); margin: 2rem 0; }

  /* ── Expander ── */
  .stExpander {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
  }
  .stExpander summary { color: var(--muted) !important; font-size: .85rem !important; }

  /* ── Button ── */
  .stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: .01em !important;
  }

  /* ── File uploader ── */
  div[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
  }
  div[data-testid="stFileUploader"] * { color: var(--text) !important; }

  /* ── Code block ── */
  .stCodeBlock { background: var(--surface2) !important; }
  pre, code { background: var(--surface2) !important; color: var(--muted) !important; }

  /* ── Misc ── */
  p, span, div, label { color: var(--text); }
  .stSpinner > div { border-top-color: var(--accent) !important; }
  .stAlert { background: var(--surface2) !important; border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  Utilities
# ─────────────────────────────────────────────────────────────────────────────
def clean_resume(text: str) -> str:
    text = re.sub(r"http\S+\s", " ", text)
    text = re.sub(r"RT|cc", " ", text)
    text = re.sub(r"#\S+\s", " ", text)
    text = re.sub(r"@\S+", " ", text)
    text = re.sub(r'[%s]' % re.escape(r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), " ", text)
    text = re.sub(r'[^\x00-\x7f]', " ", text)
    text = re.sub(r'\s+', " ", text)
    return text.strip()


def extract_text_from_pdf(uploaded_file) -> str:
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    text = pdf_extract_text(tmp_path)
    os.remove(tmp_path)
    return text


MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "saved_models")


@st.cache_resource
def load_model(name_prefix: str):
    rf    = pickle.load(open(os.path.join(MODELS_DIR, f"rf_{name_prefix}.pkl"),    "rb"))
    tfidf = pickle.load(open(os.path.join(MODELS_DIR, f"tfidf_{name_prefix}.pkl"), "rb"))
    return rf, tfidf


# ─────────────────────────────────────────────────────────────────────────────
#  Extraction helpers
# ─────────────────────────────────────────────────────────────────────────────
def extract_name(text):
    m = re.search(r'(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)', text)
    return m.group() if m else None

def extract_email(text):
    m = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
    return m.group() if m else None

def extract_phone(text):
    m = re.search(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', text)
    return m.group() if m else None

SKILLS_LIST = [
    'Python','Data Analysis','Machine Learning','Communication','Project Management',
    'Deep Learning','SQL','Tableau','Java','C++','JavaScript','HTML','CSS','React',
    'Angular','Node.js','MongoDB','Express.js','Git','Research','Statistics',
    'Quantitative Analysis','Qualitative Analysis','SPSS','R','Data Visualization',
    'Matplotlib','Seaborn','Plotly','Pandas','Numpy','Scikit-learn','TensorFlow',
    'Keras','PyTorch','NLTK','Text Mining','Natural Language Processing',
    'Computer Vision','Image Processing','OCR','Speech Recognition',
    'Recommendation Systems','Reinforcement Learning','Neural Networks',
    'XGBoost','Random Forest','Decision Trees','Support Vector Machines',
    'Linear Regression','Logistic Regression','K-Means Clustering','Apache Spark',
    'MapReduce','Apache Kafka','Data Warehousing','ETL','Big Data Analytics',
    'Cloud Computing','Amazon Web Services (AWS)','Microsoft Azure',
    'Google Cloud Platform (GCP)','Docker','Kubernetes','Linux','Shell Scripting',
    'Cybersecurity','Network Security','Penetration Testing','Encryption',
    'CI/CD','DevOps','Agile Methodology','Scrum','Kanban','Software Development',
    'Web Development','Mobile Development','Frontend Development','Backend Development',
    'Full-Stack Development','UI/UX Design','Figma','Product Management',
    'Market Research','Business Development','Sales','Marketing','SEO','SEM',
    'Google Analytics','Salesforce','Quality Assurance','Manual Testing',
    'Automated Testing','Selenium','API Testing','Technical Writing','Copywriting',
    'WordPress','E-commerce','SAP','Oracle','Power BI','Looker','Data Engineering',
    'Predictive Analytics','Business Intelligence','Data Mining','Web Scraping',
    'RESTful APIs','GraphQL','Microservices','Django','Flask','FastAPI',
    'MySQL','PostgreSQL','SQLite','Microsoft SQL Server','NoSQL','Redis',
    'Elasticsearch','Firebase','Blockchain','Smart Contracts','Chatbots',
    'Sentiment Analysis','Object Detection','Fraud Detection',
]

EDUCATION_LIST = [
    'Computer Science','Information Technology','Software Engineering',
    'Electrical Engineering','Mechanical Engineering','Civil Engineering',
    'Chemical Engineering','Biomedical Engineering','Aerospace Engineering',
    'Data Science','Data Analytics','Business Analytics','Cybersecurity',
    'Biotechnology','Biochemistry','Microbiology','Neuroscience','Bioinformatics',
    'Public Health','Nursing','Medicine','Pharmacy','Psychology','Sociology',
    'Economics','Finance','Accounting','Business Administration','Management',
    'Marketing','Entrepreneurship','Supply Chain Management','Operations Management',
    'Human Resource Management','Project Management','Architecture','Graphic Design',
    'Fine Arts','Film Studies','Journalism','English Literature','Linguistics',
    'History','Philosophy','Education','Instructional Design','Library Science',
    'Network Engineering','Digital Marketing','Game Development',
    'Environmental Science','Renewable Energy','Geography',
]

def extract_skills(text):
    return [s for s in SKILLS_LIST if re.search(r'\b{}\b'.format(re.escape(s)), text, re.IGNORECASE)]

def extract_education(text):
    return [e for e in EDUCATION_LIST if re.search(r'\b{}\b'.format(re.escape(e)), text, re.IGNORECASE)]


# ─────────────────────────────────────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
      <div class="sidebar-brand-name">Resume Analysis<span class="sidebar-brand-dot">Lens</span></div>
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio(
        "Select an analysis:",
        options=[
            "🚀 Complete Analysis",
            "📂 Category Detection",
            "💼 Job Recommendation",
            "🔍 Information Extraction",
        ],
        index=0,
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Hero
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">AI · Resume Intelligence</div>
  <div class="hero-title">Resume <span>Screening</span> & Analysis</div>
  <p class="hero-sub">
    Extract structured insights from any resume — category, role fit,
    skills, education, and contact details in seconds.
  </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  Upload
# ─────────────────────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Drop a resume PDF here or click to browse",
    type=["pdf"],
    label_visibility="collapsed",
)

if uploaded_file is None:
    st.markdown("""
    <div class="upload-zone">
      <div class="upload-icon">📄</div>
      <div class="upload-title">Upload a Resume to Begin</div>
      <div class="upload-hint">PDF format · Max 200 MB</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
#  Parse PDF
# ─────────────────────────────────────────────────────────────────────────────
with st.spinner("Parsing resume…"):
    raw_text = extract_text_from_pdf(uploaded_file)

st.markdown(f"""
<div class="status-strip">
  ✅ &nbsp;{uploaded_file.name}
</div>
""", unsafe_allow_html=True)

with st.expander("📄 Preview extracted text"):
    st.code(raw_text[:3000] + ("…" if len(raw_text) > 3000 else ""), language=None)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

cleaned_text = clean_resume(raw_text)


# ─────────────────────────────────────────────────────────────────────────────
#  Rendering helpers
# ─────────────────────────────────────────────────────────────────────────────
def render_category():
    st.markdown('<div class="section-title">Category Detection</div>', unsafe_allow_html=True)
    try:
        rf, tfidf = load_model("category")
        prediction = rf.predict(tfidf.transform([cleaned_text]))[0]
        st.markdown(f"""
        <div class="result-card green">
          <div class="result-label">Detected Resume Category</div>
          <div class="result-value">{prediction}</div>
        </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Model files not found: `rf_category.pkl` / `tfidf_category.pkl`")


def render_recommendation():
    st.markdown('<div class="section-title">Job Recommendation</div>', unsafe_allow_html=True)
    try:
        rf, tfidf = load_model("recommendation")
        prediction = rf.predict(tfidf.transform([cleaned_text]))[0]
        st.markdown(f"""
        <div class="result-card blue">
          <div class="result-label">Best-Fit Role</div>
          <div class="result-value">{prediction}</div>
        </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Model files not found: `rf_recommendation.pkl` / `tfidf_recommendation.pkl`")


def render_info():
    st.markdown('<div class="section-title">Candidate Profile</div>', unsafe_allow_html=True)

    name       = extract_name(raw_text)
    email      = extract_email(raw_text)
    phone      = extract_phone(raw_text)
    skills     = extract_skills(raw_text)
    educations = extract_education(raw_text)

    col1, col2, col3 = st.columns(3)

    def info_block(label, value, emoji):
        return f"""
        <div class="info-block">
          <div class="info-key">{emoji} &nbsp;{label}</div>
          <div class="info-val">{value if value else "—"}</div>
        </div>
        """

    with col1:
        st.markdown(info_block("Full Name", name, "👤"), unsafe_allow_html=True)
    with col2:
        st.markdown(info_block("Email", email, "📧"), unsafe_allow_html=True)
    with col3:
        st.markdown(info_block("Phone", phone, "📞"), unsafe_allow_html=True)

    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:.78rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#6b6875;margin-bottom:.5rem;">🛠️ &nbsp;Skills</div>', unsafe_allow_html=True)
    if skills:
        badges = " ".join(f'<span class="badge">{s}</span>' for s in skills)
        st.markdown(f"<div>{badges}</div>", unsafe_allow_html=True)
    else:
        st.markdown('<span style="color:#6b6875;font-size:.85rem;">No skills detected.</span>', unsafe_allow_html=True)

    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:.78rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#6b6875;margin-bottom:.5rem;">🎓 &nbsp;Education Fields</div>', unsafe_allow_html=True)
    if educations:
        tags = " ".join(f'<span class="edu-tag">{e}</span>' for e in educations)
        st.markdown(f"<div>{tags}</div>", unsafe_allow_html=True)
    else:
        st.markdown('<span style="color:#6b6875;font-size:.85rem;">No education fields detected.</span>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  Mode dispatch
# ─────────────────────────────────────────────────────────────────────────────
if mode == "🚀 Complete Analysis":
    render_category()
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    render_recommendation()
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    render_info()

elif mode == "📂 Category Detection":
    render_category()

elif mode == "💼 Job Recommendation":
    render_recommendation()

elif mode == "🔍 Information Extraction":
    render_info()
