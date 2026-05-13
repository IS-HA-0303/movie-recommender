# 🎬 CineAI — Hybrid Movie Recommender System
A production-grade, AI-powered movie recommendation system combining **BERT Semantic Embeddings**, **TF-IDF Content Filtering**, and **ALS Collaborative Filtering** into a 3-layer hybrid engine — deployed on Streamlit with a cinematic UI.

## 🚀 Live App
👉 **[https://movie-recommender-isha.streamlit.app/](https://movie-recommender-isha.streamlit.app/)**

## 🧠 How It Works
This system uses a **3-layer hybrid architecture**:

| Layer | Technology | Role |
|-------|-----------|------|
| 🧠 **BERT** | Sentence Transformers `all-MiniLM-L6-v2` | Understands semantic meaning — themes, tone, plot |
| 📝 **TF-IDF** | Count Vectorizer + Cosine Similarity | Matches genres, cast, director, keywords |
| 👥 **ALS** | Implicit Matrix Factorization | Learns from 15M+ real user ratings |

### Hybrid Score Formula
Final Score = α × BERT_score + β × TF-IDF_score + γ × Collab_score

Default weights: BERT `0.5` · TF-IDF `0.3` · Collab `0.2` (adjustable in sidebar)

## ✨ Features
- 🎯 **3-Layer Hybrid Recommendations** — BERT + TF-IDF + ALS combined
- 🧠 **BERT Semantic Understanding** — finds thematically similar movies, not just keyword matches
- 👥 **Personalised Mode** — toggle guest mode off to get user-specific recommendations
- 🎬 **Movie Posters** — fetched live from TMDB API
- 📊 **Score Breakdown** — see exactly how each recommendation was scored
- 🎚️ **Adjustable Weights** — tune BERT/TF-IDF/Collab balance in real time
- ✨ **Mouse Trail Animation** — interactive gold + green particle effect
- 📱 **4 Recommendation Modes** — Hybrid, BERT only, TF-IDF only, Collaborative only
- 🌙 **Cinematic Dark UI** — Spotify-inspired design with hover effects
- 
## 📈 Model Performance
| Metric | Value |
|--------|-------|
| ALS Precision@10 | **71.2%** |
| Movies Indexed | **4,806** |
| Users Trained On | **84,222** |
| Ratings Used | **15,087,343** |
| BERT Embedding Dims | **384** |

## 🏗️ Tech Stack
| Category | Tools |
|----------|-------|
| **Language** | Python 3.11 |
| **UI Framework** | Streamlit |
| **NLP / Embeddings** | Sentence Transformers (BERT) |
| **Collaborative Filtering** | Implicit (ALS Matrix Factorization) |
| **Content Filtering** | Scikit-learn (TF-IDF + Cosine Similarity) |
| **Data Processing** | Pandas, NumPy, SciPy |
| **Movie Metadata** | TMDB API |
| **Training Data** | MovieLens 25M + TMDB 5000 |
| **Deployment** | Streamlit Cloud + GitHub + Google Drive |

## 🔄 System Architecture
```
User selects a movie
        ↓
┌───────────────────────────────────┐
│         Hybrid Engine             │
│                                   │
│  BERT Layer  →  Semantic Score    │
│  TF-IDF Layer → Content Score     │
│  ALS Layer   → Collab Score       │
│                                   │
│  Final = α×BERT + β×TF + γ×ALS    │
└───────────────────────────────────┘
        ↓
Top N recommendations ranked by Final Score
        ↓
Posters fetched from TMDB API
        ↓
Results displayed with score breakdown
```
## 🗃️ Datasets Used
 
| Dataset | Size | Purpose |
|---------|------|---------|
| [TMDB 5000 Movies](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) | 4,806 movies | Content features (genres, cast, crew, overview) |
| [MovieLens 25M](https://grouplens.org/datasets/movielens/25m/) | 25M ratings | Collaborative filtering training |  Movie(https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) | 4,806 movies | Content features (genres, cast, crew, overview) |
| [MovieLens 25M](https://grouplens.org/datasets/movielens/25m/) | 25M ratings | Collaborative filtering training |
