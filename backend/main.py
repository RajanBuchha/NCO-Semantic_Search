from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# import from transform layer
import sys
import os
sys.path.append(os.path.abspath("../transform"))

from search_engine import semantic_search

app = FastAPI(title="NCO Semantic Search")

# for frontend later (optional now)

origins = ["*"]  # allow everything for now

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "NCO Semantic Search API running"}

@app.get("/exact_search")
def exact_search(query: str):
    query = query.lower()
    
    matches = []
    for r in semantic_search(query, k=50):  # search larger pool
        if query in r["occupation_title"].lower():
            matches.append(r)

    return matches

@app.get("/semantic_search")
def search(query: str = Query(...), k: int = 5):
    results = semantic_search(query, k)
    return results

@app.get("/hybrid_search")
def hybrid_search(query: str, k: int = 10):
    query_lower = query.lower()

    # semantic results pool
    semantic_pool = semantic_search(query, k=50)

    exact_matches = []
    semantic_matches = []

    for r in semantic_pool:
        if query_lower in r["occupation_title"].lower():
            exact_matches.append(r)
        else:
            semantic_matches.append(r)

    final_results = exact_matches + semantic_matches
    return final_results[:k]
