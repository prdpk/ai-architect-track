from sentence_transformers import SentenceTransformer
import anthropic
import chromadb

# Create the ChromaDB client and collection
db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_or_create_collection(name="policies")

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create the Anthropic client
client = anthropic.Anthropic()

# Retrieval configuration
TOP_K = 2

# One synthetic policy document
policy_document = """
Water damage from burst pipes is covered up to $10,000 with a $500 deductible.

Fire damage to the insured property is covered after a $1,000 deductible.

The policy does not cover flood damage caused by natural disasters.

Theft of personal belongings is covered up to $5,000 with proof of ownership.
"""

# Chunk the document by blank lines
chunks = [
    chunk.strip()
    for chunk in policy_document.split("\n\n")
    if chunk.strip()
]

print("Policy Chunks:\n")

for i, chunk in enumerate(chunks, start=1):
    print(f"{i}. {chunk}\n")

# Store chunks in ChromaDB only once
if collection.count() == 0:
    embeddings = model.encode(chunks)
    print("Embedding shape:", embeddings.shape)
    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),   # bring your own — .tolist() for Chroma
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )
    print("Embedded and stored chunks.")
else:
    print("Chunks already stored — skipping embedding.")

# User query
query = "Is theft covered?"

query_embedding = model.encode(query)

# Retrieve top-k matching chunks from ChromaDB
results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=2,
)
retrieved = results["documents"][0]
distances = results["distances"][0]

print("\nQuery:", query)
print("\nRetrieved Chunks:\n")

for rank, (chunk, distance) in enumerate(zip(retrieved, distances), start=1):
    print(f"{rank}. Distance: {distance:.4f}")
    print(f"   {chunk}\n")

# Build context from retrieved chunks
context = "\n".join(retrieved)

# Build the grounded prompt
prompt = f"""
Use ONLY the policy context below to answer the question.

If the answer is not in the context, say:
"I don't have that information."

Context:
{context}

Question:
{query}
"""

print("\n--- PROMPT SENT TO CLAUDE ---")
print(prompt)
print("-----------------------------\n")

# Call Claude
message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
)

print("Claude's Answer:")
print(message.content[0].text)

print("\nUsage:")
print(message.usage)