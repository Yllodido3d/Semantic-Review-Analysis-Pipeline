#  Project: Semantic Review Analyzer (AI-Powered E-commerce Intelligence)

##  Project Goal

This project demonstrates an **end-to-end data intelligence pipeline** capable of extracting raw customer reviews from a protected e-commerce site (Best Buy) and transforming them into an actionable **Intelligence Matrix** using state-of-the-art **Embedding Models**.

The final product allows a client to ask conceptual questions (e.g., "What are the common complaints about screen quality?") and receive the most relevant reviews, regardless of exact keyword matching.

## 🛠️ Technology Stack

* **Extraction:** Python, Selenium, Pandas
* **AI/NLP:** PyTorch, Sentence-Transformers (`all-MiniLM-L6-v2`), Hugging Face Transformers (`distilbert`)
* **Techniques:** Advanced JavaScript Evasion, Data Safety (`try...finally`), Semantic Search (Cosine Similarity).

## 💡 Key Features Implemented

### 1. Advanced Evasion & Data Safety (`collector.py`)
* **JavaScript Click Bypass:** Solves the common problem of non-clickable, disabled, or overlapping "Next" buttons by forcing the click via `driver.execute_script("arguments[0].click()")`.
* **Dynamic Scroll Logic:** Implements logic to scroll within the review element to load all content blocks on a single page, adapting to dynamic content loading.
* **Interrupt Safety:** Uses the `try...finally` block to guarantee that all collected data is saved to `raw_reviews.csv` even if the script is terminated manually (`Ctrl+C`).

### 2. Core AI: Semantic Search (`analyzer.py`)
The system converts all reviews into dense numerical vectors (Embeddings) 

[Image of semantic search architecture diagram]
. This enables conceptual understanding.

* **Input:** Query text (e.g., "bad return policy").
* **Process:** The query is also converted to a vector and compared against all review vectors using **Cosine Similarity**.
* **Output:** The most semantically similar review, even if it doesn't contain the exact keywords.

### 3. Proof of Concept: Sentiment Filtering
To improve the quality of negative searches, a second model (`distilbert`) was integrated to classify all reviews as Positive or Negative, allowing the semantic search to be **filtered** only within the pool of negative reviews.

## 📈 Engineering Insight & Conclusion (The Value Proposition)

The project successfully achieved the technical goals, but exposed a critical trade-off common in lightweight AI solutions:

| Component | Result | Diagnosis/Actionable Insight |
| :--- | :--- | :--- |
| **Collector** | Stable, resilient to soft detection, safe on interruption. | ✅ **Success.** Ready for PyInstaller packaging. |
| **Embedding Search** | Finds the correct **topic** (e.g., 'pixels', 'resolution'). | ✅ **Success.** Proves the core value of semantic search. |
| **Sentiment Filter** | The lightweight `distilbert` model misclassified complex reviews (e.g., a long positive review was flagged as negative). | **❌ Failure (of the model).** The system requires a larger, fine-tuned sentiment model to be commercially viable, demonstrating a need for model upgrade or custom fine-tuning. |

**Final Status:** The architecture is complete. The system is stable, requiring only a better-performing sentiment model to reach commercial-grade accuracy.

---

## 🚀 How to Run

1.  **Clone the Repository:** `git clone (https://github.com/Yllodido3d/Semantic-Review-Analysis-Pipeline.git)`
2.  **Install Dependencies:** `pip install -r requirements.txt` (Needs `selenium`, `pandas`, `torch`, `sentence-transformers`, `transformers`)
3.  **Run Collector:** `python collector.py` (Creates `raw_reviews.csv`)
4.  **Run Analyzer:** `python analyzer.py` (Performs the AI search and prints the result)
