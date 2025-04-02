import json
import toml

# Load the JSON file
with open("gen-lang-client-0351263191-a3fba8bb8a30.json", "r") as f:
    data = json.load(f)

# Save as TOML
with open(".streamlit/gen-lang-client-0351263191-a3fba8bb8a30.toml", "w") as f:
    toml.dump(data, f)
