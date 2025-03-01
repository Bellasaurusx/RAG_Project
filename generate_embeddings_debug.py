import os
import pickle
from sentence_transformers import SentenceTransformer

# ✅ Load Chunks
if os.path.exists("chunks.pkl"):
    print("\n🔹 Loading chunks.pkl...")
    with open("chunks.pkl", "rb") as file:
        chunks = pickle.load(file)
    print(f"✅ Total Chunks Loaded: {len(chunks)}")
else:
    print("\n❌ ERROR: chunks.pkl not found. Run the chunking step first.")
    exit()

# ✅ Load Embedding Model
print("\n🔹 Loading SentenceTransformer model...")
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"\n❌ ERROR: Could not load model: {e}")
    exit()

# ✅ Generate Embeddings
print("\n🔹 Generating embeddings (this may take a few minutes)...")
try:
    embeddings = {i: model.encode(chunk) for i, chunk in enumerate(chunks)}
    print("✅ Embeddings generated successfully!")
except Exception as e:
    print(f"\n❌ ERROR: Failed to generate embeddings: {e}")
    exit()

# ✅ Save Embeddings
print("\n🔹 Saving embeddings to embeddings.pkl...")
try:
    with open("embeddings.pkl", "wb") as file:
        pickle.dump(embeddings, file)
    print("✅ Embeddings saved as embeddings.pkl!")
except Exception as e:
    print(f"\n❌ ERROR: Failed to save embeddings: {e}")
    exit()
