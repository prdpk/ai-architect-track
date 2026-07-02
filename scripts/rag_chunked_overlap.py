from sentence_transformers import SentenceTransformer
import anthropic
import chromadb
import shutil
import os

# -----------------------------
# Configuration
# -----------------------------
TOP_K = 2
CHUNK_SIZE = 40
OVERLAP = 10

DB_PATH = "./chroma_db"

# Uncomment the next 3 lines whenever you change the source document
# so Chroma rebuilds the embeddings.
if os.path.exists(DB_PATH):
    shutil.rmtree(DB_PATH)

# -----------------------------
# Create clients
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")
client = anthropic.Anthropic()

db = chromadb.PersistentClient(path=DB_PATH)
collection = db.get_or_create_collection(name="policies")

# -----------------------------
# Longer synthetic policy
# -----------------------------
policy_document = """
Water damage from burst pipes is covered up to $10,000 with a $500 deductible.
The policy covers accidental pipe failures occurring inside the insured property.
Damage caused by gradual leaks, poor maintenance, or negligence is not covered.
Claims must be reported within 30 days of discovering the damage.

Fire damage to the insured property is covered after a $1,000 deductible.
Coverage includes structural repairs, smoke damage, and debris removal.
Damage caused intentionally by the policyholder is excluded.
Temporary accommodation expenses may also be reimbursed while repairs are underway.

Flood damage caused by natural disasters is not covered under this policy.
Customers must purchase a separate flood insurance policy for protection.
Surface water, storm surge, and overflowing rivers are all considered flood events.
Water entering through open windows during a storm is assessed separately.

Theft of personal belongings is covered up to $5,000 with proof of ownership.
Receipts, photographs, or police reports may be required to support the claim.
Cash, collectibles, and jewelry have separate coverage limits.
The insurer may request additional documentation before approving payment.
"""

# -----------------------------
# Chunking function
# -----------------------------
def chunk_text(text, chunk_size, overlap):
  
    if overlap >= chunk_size:
          raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


chunks = chunk_text(policy_document, CHUNK_SIZE, OVERLAP)

print("\nGenerated Chunks\n")

for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i}")
    print(chunk)
    print("-" * 70)

# -----------------------------
# Generate embeddings ourselves
# -----------------------------
embeddings = model.encode(chunks).tolist()

print(f"\nEmbedding shape: ({len(embeddings)}, {len(embeddings[0])})")

# -----------------------------
# Store in Chroma
# -----------------------------
collection.add(
    ids=[f"chunk_{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings,
)

print("\nChunks embedded and stored in ChromaDB.")

# -----------------------------
# User query
# -----------------------------
query = "Is theft covered?"

query_embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=TOP_K,
)

documents = results["documents"][0]
distances = results["distances"][0]

print("\nRetrieved Chunks\n")

for rank, (doc, distance) in enumerate(zip(documents, distances), start=1):
    print(f"{rank}. Distance: {distance:.4f}")
    print(doc)
    print()

# -----------------------------
# Build context
# -----------------------------
context = "\n\n".join(documents)

prompt = f"""
Use ONLY the policy context below to answer the question.

If the answer is not present in the context, respond exactly with:

I don't have that information.

Context:
{context}

Question:
{query}
"""

print("\nPrompt sent to Claude\n")
print(prompt)

# -----------------------------
# Claude
# -----------------------------
message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=150,
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
)

print("\nClaude's Answer\n")
print(message.content[0].text)

print("\nUsage")
print(message.usage)