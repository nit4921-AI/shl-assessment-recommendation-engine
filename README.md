# 🧠 SHL Assessment Recommendation Engine

> A smart recommendation engine that suggests relevant SHL assessments based on a given job description or natural language query — built for the **SHL AI Internship Generative AI Assignment**.

---

## 🚀 Overview

This project implements a **FastAPI-based microservice** that recommends SHL assessments (Knowledge & Skills + Personality & Behavior) based on a job description or query text.

It uses **Sentence Transformer embeddings** for semantic similarity and supports **LLM-based reranking (Gemini)** for enhanced contextual recommendations.

The project also includes a **modern SHL-themed frontend** for live testing.

---

## 🧩 Features

✅ Recommend top-K most relevant assessments from SHL’s product catalog
✅ Balance between **Knowledge & Skills (K)** and **Personality & Behavior (P)** tests
✅ Supports **natural language** or **JD input**
✅ Easy REST API: `/health` and `/recommend`
✅ Interactive **frontend UI** (HTML + JS + CSS) styled like [shl.com](https://www.shl.com)
✅ Ready for deployment on Render / Hugging Face / GCP

---

## 🌇 Architecture

```
📦 shl_assessment_recommender
├── app/
│   ├─ main.py               # FastAPI app with endpoints
│   ├─ recommender.py        # Embedding & recommendation logic
│   └─ utils.py              # Helper functions (LLM, evaluation, etc.)
│
├── frontend/
│   ├─ index.html            # SHL-themed frontend
│   ├─ app.js                # Frontend logic to call API
│   └─ style.css             # Centered, light SHL design
│
├── data/
│   ├─ shl_catalog.csv       # Crawled assessment catalog
│   ├─ labelled_train_set.csv
│   └─ test_queries.csv
│
├── scripts/
│   └─ generate_predictions.py   # Used for automated testing
│
├── requirements.txt
└─ README.md
```

---

## ⚙️ Setup & Run Locally

### 1️⃣ Clone the repo

```bash
git clone https://github.com/<your-username>/shl-assessment-recommendation-engine.git
cd shl-assessment-recommendation-engine
```

### 2️⃣ Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate   # (Windows)
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run backend API

```bash
uvicorn app.main:app --reload
```

You’ll see:

```
Uvicorn running on http://127.0.0.1:8000
```

---

## 🧠 API Endpoints

| Endpoint     | Method | Description                              |
| ------------ | ------ | ---------------------------------------- |
| `/health`    | GET    | Returns API health status                |
| `/recommend` | POST   | Returns top-K assessment recommendations |

### Example Request

```json
POST /recommend
{
  "query": "Need a Java developer who collaborates with teams",
  "top_k": 5,
  "balance": true
}
```

### Example Response

```json
{
  "query": "Need a Java developer who collaborates with teams",
  "recommendations": [
    {
      "assessment_name": ".NET WCF (New)",
      "url": "https://www.shl.com/products/product-catalog/view/net-wcf-new/",
      "test_type": "K",
      "score": 0.396
    }
  ]
}
```

---

## 💻 Frontend (SHL-Style Interface)

Open your frontend manually:

```
frontend/index.html
```

It connects to your running API (default `http://127.0.0.1:8000`)
and allows querying assessments interactively.

🖼️ **Preview Screenshot**
<img width="1899" height="898" alt="image" src="https://github.com/user-attachments/assets/dbf41eb2-2542-4f7d-8f70-a6c4b6247100" />


---

## 📊 Evaluation

Your submission can be scored automatically using:

```
python scripts/generate_predictions.py --test_csv data/test_queries.csv --out_csv submission.csv
```

Metrics include:

* **Mean Recall@10**
* **Balance K/P ratio**
* **Relevance ranking**

---

## 🧬 Technologies Used

| Area           | Tech                                |
| -------------- | ----------------------------------- |
| Backend        | FastAPI, Uvicorn                    |
| NLP            | Sentence Transformers, Transformers |
| LLM (optional) | Gemini API                          |
| Frontend       | HTML5, CSS3, Vanilla JS             |
| Data           | Pandas, Scikit-learn                |

---

## 🤎 Example Queries

| Query                                                 | Expected Outcome                                 |
| ----------------------------------------------------- | ------------------------------------------------ |
| “Need a Java developer good at teamwork”              | Mix of `.NET` + “Interpersonal Communication”    |
| “Hiring sales professionals for customer interaction” | Mix of “Sales Test” + “Personality / Team Style” |
| “Looking for leader for technical team”               | Leadership + Technical K tests                   |

---

## 📦 Requirements

```
fastapi==0.115.0
uvicorn==0.32.0
transformers==4.57.1
sentence-transformers==2.7.0
pandas==2.2.3
scikit-learn==1.5.2
numpy==1.26.4
requests==2.32.3
google-generativeai==0.8.2
selenium==4.38.0
python-dotenv==1.0.1
```

---

## 🤰 Deployment Options

You can deploy this API easily using:

* [Render](https://render.com)
* [Hugging Face Spaces](https://huggingface.co/spaces)
* [Google Cloud Run](https://cloud.google.com/run)
* [Railway](https://railway.app)

---

## 🏁 Author

👤 **Nitish Kopparaju**
🚀 AI & ML Engineer | DevOps Enthusiast
📧 [[nitishkopparaju@gmail.com]]
🌐 [https://www.linkedin.com/in/nitish-kopparaju/]
---

> ⚠️ *Disclaimer:* This project is a **themed educational implementation** and is **not affiliated with SHL**.
> The dataset and links are used only for demonstration and skill assessment purposes.
