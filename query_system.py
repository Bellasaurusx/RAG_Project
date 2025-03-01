import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# ✅ Load Chunks
print("\n🔹 Loading text chunks...")
with open("chunks.pkl", "rb") as file:
    chunks = pickle.load(file)
print(f"✅ Loaded {len(chunks)} chunks!")

# ✅ Load Embeddings
print("\n🔹 Loading embeddings...")
with open("embeddings.pkl", "rb") as file:
    embeddings = pickle.load(file)
print(f"✅ Loaded {len(embeddings)} embeddings!")

# ✅ Load SentenceTransformer Model
print("\n🔹 Loading SentenceTransformer model for querying...")
query_model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Load HuggingFace Model
print("\n🔹 Loading HuggingFace model for response generation...")
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
print("✅ Model loaded successfully!")

# ✅ Function to Retrieve the Most Relevant Chunks
def retrieve_relevant_chunks(query, top_n=7):
    query_embedding = query_model.encode([query])
    chunk_ids = list(embeddings.keys())
    chunk_embeddings = np.array([embeddings[i] for i in chunk_ids])

    # Compute cosine similarity
    similarities = cosine_similarity(query_embedding, chunk_embeddings)[0]
    
    # Get top N most similar chunks
    top_indices = np.argsort(similarities)[::-1][:top_n]
    top_chunks = [chunks[chunk_ids[i]] for i in top_indices]

    print("\n🔹 Retrieved Top Relevant Chunks:")
    for i, chunk in enumerate(top_chunks, 1):
        print(f"{i}. {chunk[:200]}...")  # Show first 200 chars

    return top_chunks

# ✅ Function to Generate a Response
def generate_response(query):
    print("\n🔹 Retrieving relevant chunks...")
    relevant_chunks = retrieve_relevant_chunks(query)

    # Build a structured input prompt
    context = "\n".join(relevant_chunks)
    input_text = (
        f"Please provide a detailed and informative answer.\n\n"
        f"Use the following context to answer the question.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        f"Answer:"
    )

    print("\n🔹 Generating response...")
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs, max_length=150)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response


# ✅ Interactive Testing
if __name__ == "__main__":
    while True:
        query = input("\n❓ Enter a question (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break
        response = generate_response(query)
        print("\n💬 Response:", response)
