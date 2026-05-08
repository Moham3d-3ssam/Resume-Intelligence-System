# 🔬 Full Resume Analysis App

> An AI-powered Streamlit application that extracts structured insights from any PDF resume — category classification, job role recommendation, and candidate profile extraction in seconds.

---

## 🖥️ Live Demo

🚀 Try the deployed Streamlit application here:

[🔗 Full Resume Analysis App](https://69ugfpkntg2ep8kkdnouz7.streamlit.app/)

Upload any PDF resume → choose an analysis mode from the sidebar → get instant AI-driven results instantly.

---

## ✨ Features

| Feature | Description |
|---|---|
| **📂 Category Detection** | Classifies a resume into one of 25+ job categories using a trained Random Forest model |
| **💼 Job Recommendation** | Predicts the best-fit role/job title based on resume content |
| **🔍 Information Extraction** | Extracts name, email, phone number, 100+ skills, and 50+ education fields |
| **🚀 Complete Analysis** | Runs all three analyses at once in a single view |

**Additional highlights:**
- 📄 PDF upload and automatic text extraction via `pdfminer`
- 🌑 Sleek pure dark-mode UI with custom CSS
- ⚡ Model caching with `@st.cache_resource` for fast repeated analysis
- 🔎 Text preview of extracted resume content

---

## 🖥️ Demo

Upload any PDF resume → choose an analysis mode from the sidebar → get instant AI-driven results.

```
┌─────────────────────────────────────────────────────────┐
│  Sidebar                │  Main Panel                   │
│  ─────────────────────  │  ──────────────────────────   │
│  🚀 Complete Analysis   │  ✅ resume.pdf               │
│  📂 Category Detection  │                               │
│  💼 Job Recommendation  │  ┌─────────────────────────┐  │
│  🔍 Info Extraction     │  │ Category: Data Science  │  │
│                         │  ├──────────────────────────┤ │
│                         │  │ Role: ML Engineer        │ │
│                         │  ├──────────────────────────┤ │
│                         │  │ Name · Email · Phone     │ │
│                         │  │ Skills · Education       │ │
│                         │  └──────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Full-Resume-Analysis-App/
├── app/
│   └── app.py                    # Streamlit application
├── data/
│   └── Link.txt                  # Kaggle dataset link
├── notebooks/
│   ├── resume_category.ipynb     # Model training: category classification
│   ├── resume_recommendation.ipynb # Model training: job recommendation
│   └── resume_info.ipynb         # EDA & information extraction
└── saved_models/
    ├── tfidf_category.pkl        # TF-IDF vectorizer for category model
    ├── rf_category.pkl           # Random Forest classifier (category)
    ├── tfidf_recommendation.pkl  # TF-IDF vectorizer for recommendation model
    └── rf_recommendation.pkl     # Random Forest classifier (recommendation)
```

---

## 🛠️ Tech Stack

| Layer | Library |
|---|---|
| **Web UI** | [Streamlit](https://streamlit.io/) |
| **PDF Parsing** | [pdfminer.six](https://pdfminersix.readthedocs.io/) |
| **ML Models** | [scikit-learn](https://scikit-learn.org/) — TF-IDF + Random Forest |
| **Data Processing** | pandas, NumPy |
| **EDA / Visualization** | Matplotlib, Seaborn |
| **Model Serialization** | pickle |

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.8+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/Moham3d-3ssam/Full-Resume-Analysis-App.git
cd Full-Resume-Analysis-App
```

### 2. Install dependencies

```bash
pip install streamlit pdfminer.six scikit-learn pandas numpy matplotlib seaborn
```

### 3. Run the app

```bash
streamlit run app/app.py
```

Then open **http://localhost:8501** in your browser.

---

## 🤖 Machine Learning Pipeline

Both classification tasks follow the same pipeline:

```
Raw Resume Text
      │
      ▼
  Text Cleaning          # Remove URLs, hashtags, special chars, non-ASCII
      │
      ▼
  TF-IDF Vectorizer      # Fitted on training corpus
      │
      ▼
  Random Forest (n=200)  # Trained on balanced dataset
      │
      ▼
  Predicted Label        # Category / Job Role
```

### Dataset

Sourced from Kaggle: [Resume Datasets by noorsaeed](https://www.kaggle.com/datasets/noorsaeed/resume-datasets)

The dataset is balanced via upsampling before training to ensure equal class representation.

### Model Training

Refer to the Jupyter notebooks in `notebooks/` to retrain or fine-tune models:

```bash
jupyter notebook notebooks/resume_category.ipynb
jupyter notebook notebooks/resume_recommendation.ipynb
```

Trained models are saved automatically to `saved_models/`.

---

## 📊 Analysis Modes

### 🚀 Complete Analysis
Runs all three analyses in sequence: category → recommendation → candidate profile.

### 📂 Category Detection
Classifies the resume into one of the trained job categories (e.g., *Data Science*, *Web Development*, *Finance*, *HR*, etc.).

### 💼 Job Recommendation
Recommends the single best-fit job role based on the resume's skills and experience.

### 🔍 Information Extraction
Uses regex patterns to extract:

- **Name** — first two capitalized words (e.g., `John Smith`)
- **Email** — standard email pattern
- **Phone** — supports international formats
- **Skills** — matched against a curated list of 100+ technical and professional skills
- **Education Fields** — matched against 60+ academic disciplines

---

## 🗂️ Detected Skills (sample)

`Python` · `Machine Learning` · `Deep Learning` · `SQL` · `TensorFlow` · `PyTorch` · `Docker` · `Kubernetes` · `AWS` · `React` · `Node.js` · `NLP` · `Computer Vision` · `DevOps` · `CI/CD` · `Power BI` · `Tableau` · *and 80+ more*

## 🎓 Detected Education Fields (sample)

`Computer Science` · `Data Science` · `Software Engineering` · `Cybersecurity` · `Business Administration` · `Finance` · `Psychology` · *and 50+ more*

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is open source. Feel free to use, modify, and distribute it.

---

## 👤 Author

**Mohamed Essam**  
[GitHub](https://github.com/Moham3d-3ssam)
