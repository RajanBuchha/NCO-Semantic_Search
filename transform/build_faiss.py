import pandas as pd
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

print("Loading dataset...")
df = pd.read_csv("nco_500_embed.csv", dtype=str)
df = df.fillna("")

texts = df["embed_data"].tolist()
metadatas = df.drop(columns=["description", "embed_data"]).to_dict(orient="records")

print("Loading embedding model...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

print("Generating embeddings...")
vectors = embeddings.embed_documents(texts)

# 🔥 Normalize vectors
print("Normalizing vectors...")
vectors = np.array(vectors)
norms = np.linalg.norm(vectors, axis=1, keepdims=True)
vectors = vectors / norms

# Pair text with its vector
text_embeddings = list(zip(texts, vectors.tolist()))

print("Building normalized FAISS index...")
faiss_store = FAISS.from_embeddings(
    text_embeddings,
    embeddings,
    metadatas=metadatas
)

print("Saving FAISS index...")
faiss_store.save_local("faiss_index")

print("\nNormalized FAISS index saved successfully.")
