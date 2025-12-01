from sentence_transformers import SentenceTransformer
from transformers import pipeline
import pandas as pd
import torch
import torch.nn.functional as F

# --- 1. DATA LOADING & CLEANING ---
print("📂 Loading raw data from CSV...")
try:
    # Note: Using 'raw_reviews.csv' to match the collector.py output
    df = pd.read_csv('raw_reviews.csv')
    print(f"✅ Data loaded successfully! Total reviews: {len(df)}")
except FileNotFoundError:
    print("❌ Error: 'raw_reviews.csv' not found. Run the collector script first!")
    exit()

# Basic cleaning and index reset (Crucial for later indexing)
df.dropna(subset=['review_text'], inplace=True)
df.reset_index(drop=True, inplace=True)

# --- 2. SENTIMENT ANALYSIS (TO FILTER BY TOPIC EMOTION) ---
print("\n🔎 Classifying sentiment for each review...")
# Loads the lightweight DistilBERT model for binary classification
sentiment_pipeline = pipeline(
    "sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Classify and ensure long reviews are cut off (truncation=True)
results = sentiment_pipeline(df['review_text'].tolist(), truncation=True)

# Extracts the positive score. If the label is NEGATIVE, we flip the score (1 - score)
df['sentiment_score'] = [res['score'] if res['label'] ==
                         'POSITIVE' else 1 - res['score'] for res in results]

print("✅ Sentiment classified!")
print(df[['review_text', 'sentiment_score']].head())

# --- 3. EMBEDDING GENERATION (THE CORE OF SEMANTIC SEARCH) ---
print("\n🤖 Loading Embedding Model (all-MiniLM-L6-v2)...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("\n🧠 Transforming text into numerical vectors (Embeddings)...")
review_embeddings = model.encode(
    df['review_text'].tolist(),
    convert_to_tensor=True,
    show_progress_bar=True
)

print("\n✅ Embeddings Generated Successfully!")
print(f"📐 Intelligence Matrix Dimension: {review_embeddings.shape}")

# --- 4. SEMANTIC QUERY & FILTERED SEARCH ---
# Define the query (The customer's question)
query = ["Dead pixels and bad return policy"]

# Transform the query into a 384-dimensional vector
query_embedding = model.encode(query, convert_to_tensor=True)

# 4a. 🛑 SENTIMENT FILTER
# Since the Query is negative, we filter for reviews with a score < 0.5 (or low confidence of being positive)
negative_filter = (df['sentiment_score'] < 0.5)

# Apply the filter to the Intelligence Matrix
negative_embeddings = review_embeddings[negative_filter]

# Map the indices back to the original DataFrame
original_negative_indices = df[negative_filter].index

if len(negative_embeddings) == 0:
    print("\n❌ No negative reviews were found to filter the search.")

else:
    # 4b. SEMANTIC SEARCH on the Negative Subset
    similarities_filtered = F.cosine_similarity(
        query_embedding, negative_embeddings)

    # Find the index of the closest vector within the filtered subset
    best_match_index_in_subset = torch.argmax(similarities_filtered)

    # Map back to the final DataFrame index
    best_match_index_int = original_negative_indices[best_match_index_in_subset.item()]
    best_match_score = similarities_filtered[best_match_index_in_subset]

    # --- 5. FINAL RESULT ---
    print("\n--- Semantic Search Result (FILTERED) ---")
    print(f"💰 Query: {query[0]} (Searching only negative reviews)")
    print("-" * 35)
    print(f"✅ Best Match Score: {best_match_score.item():.4f}")
    print("📦 Original Review:")
    print(df.iloc[best_match_index_int]['review_text'])
    print("-" * 35)