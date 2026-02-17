import pandas as pd
import os

# Path to extraction CSV
input_path = os.path.join("..", "extraction", "nco_500_with_description.csv")

# Output file will stay inside transform folder
output_path = "nco_500_embed.csv"

# Load CSV
df = pd.read_csv(input_path)

# Create embed_data column
df["embed_data"] = df.apply(
    lambda row: (
        f"The occupation {row['occupation_title']} "
        f"NCO 2015: {row['nco_2015']}, "
        f"NCO 2004: {row['nco_2004']} belongs to division {row['division']}, "
        f"subdivision {row['subdivision']}, "
        f"group {row['group']}, "
        f"and family {row['family']}. "
        f"Description: {row['description']}"
    ),
    axis=1
)

# Save inside transform folder
df.to_csv(output_path, index=False)

print(f"Saved {output_path}")
