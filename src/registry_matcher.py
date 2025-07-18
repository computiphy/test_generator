import json
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

# Load model once globally
model = SentenceTransformer("all-MiniLM-L6-v2")  # Fast and light

def load_registry(registry_path: str = "src/firmware_registry.json") -> list[dict]:
    with open(registry_path, "r", encoding="utf-8") as f:
        return json.load(f)

def match_step_to_function(step_text: str, top_k: int = 1, registry_path: str = "src/firmware_registry.json") -> list[str]:
    registry = load_registry(registry_path)

    # Combine tags and description for matching context
    candidates = [
        {
            "name": item["name"],
            "context": f"{item['description']} Tags: {' '.join(item['tags'])}",
            "example": item["examples"][0] if item["examples"] else f"{item['name']}()"
        }
        for item in registry
    ]

    # Encode inputs
    step_embedding = model.encode(step_text, convert_to_tensor=True)
    candidate_embeddings = model.encode([c["context"] for c in candidates], convert_to_tensor=True)

    # Compute cosine similarity
    scores = util.pytorch_cos_sim(step_embedding, candidate_embeddings)[0]

    # Rank results
    top_indices = scores.topk(k=top_k).indices

    matched_functions = []
    for idx in top_indices:
        c = candidates[idx]
        matched_functions.append(c["example"])

    return matched_functions
