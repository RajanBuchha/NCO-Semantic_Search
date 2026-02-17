import pandas as pd

# Load structured data
df = pd.read_csv("nco_data.csv")

# Create a simple description
df["description"] = df.apply(
    lambda row: f"{row['occupation_title']} belongs to the {row['family']} family under "
                f"{row['group']} group in the {row['division']} division.",
    axis=1
)

# Create embed_data column (this is what will be embedded later)
df["embed_data"] = df.apply(
    lambda row: f"The occupation {row['occupation_title']} "
                f"NCO 2015: {row['nco_2015']}, "
                f"NCO 2004: {row['nco_2004']} belongs to division {row['division']}, "
                f"subdivision {row['subdivision']}, "
                f"group {row['group']}, "
                f"and family {row['family']}. "
                f"Description: {row['description']}",
    axis=1
)

# Save new CSV
df.to_csv("nco_with_description.csv", index=False)

print("Saved nco_with_description.csv")
