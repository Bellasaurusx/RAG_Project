import pickle
from sentence_transformers import SentenceTransformer

# Load the saved chunks
with open("chunks.pkl", "rb") as file:
    chunks = pickle.load(file)

print(f"Total Chunks Loaded: {len(chunks)}")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Generating embeddings...")

# Generate embeddings
embeddings = {i: model.encode(chunk) for i, chunk in enumerate(chunks)}

# Save embeddings to a file
with open("embeddings.pkl", "wb") as file:
    pickle.dump(embeddings, file)

print("✅ Embeddings saved as embeddings.pkl")
