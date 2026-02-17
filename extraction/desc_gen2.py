import pandas as pd
import requests
import time

# Load base CSV
df = pd.read_csv("nco_data.csv")

# STRICT 500 LIMIT (like your friend)
df = df.head(500)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:1b"

descriptions = []

for idx, row in df.iterrows():
    prompt = f"""
You are generating occupational descriptions for a national classification database.

Write a factual 3-4 sentence description of the occupation "{row['occupation_title']}".

The description must:
- Be a single paragraph
- Be written in declarative tone
- Not include options
- Not ask follow-up questions
- Not include headings or bullet points

Division: {row['division']}
Subdivision: {row['subdivision']}
Group: {row['group']}
Family: {row['family']}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    description = result.get("response", "").strip()

    descriptions.append(description)

    print(f"Generated {idx + 1}/500")

    time.sleep(0.3)  # prevent overload

df["description"] = descriptions

df.to_csv("nco_500_with_description.csv", index=False)

print("Saved nco_500_with_description.csv")
