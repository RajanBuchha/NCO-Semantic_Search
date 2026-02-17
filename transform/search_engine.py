from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

print("Loading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

print("Loading stored FAISS index...")

faiss_store = FAISS.load_local(
    "../transform/faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

print("FAISS loaded successfully.")

# ---- search function ----
def semantic_search(query, k=5):
    results = faiss_store.similarity_search_with_score(query, k=k)
    output = []

    for doc, score in results:
        row = doc.metadata
        row["similarity_score"] = float(score)
        output.append(row)

    return output
