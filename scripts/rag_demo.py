from sentence_transformers import SentenceTransformer, util
import anthropic

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create the Anthropic client
client = anthropic.Anthropic()

# Synthetic insurance policy snippets
snippets = [
    "Water damage from burst pipes is covered up to $10,000 with a $500 deductible.",
    "Fire damage to the insured property is covered after a $1,000 deductible.",
    "The policy does not cover flood damage caused by natural disasters.",
    "Theft of personal belongings is covered up to $5,000 with proof of ownership."
]

# Generate embeddings for the snippets
embeddings = model.encode(snippets)

# Inspect the embeddings
print("Embedding shape:", embeddings.shape)
print("First 8 values of the first embedding:")
print(embeddings[0][:8])

# User query
#query = "Someone broke in and took my laptop"
query = "Is earthquake damage covered?"

# Embed the query using the same model
query_embedding = model.encode(query)

# Compute cosine similarity between the query and all snippets
scores = util.cos_sim(query_embedding, embeddings)[0]

# Pair each snippet with its similarity score
results = list(zip(snippets, scores))

# Sort by similarity score (highest first)
results.sort(key=lambda x: x[1], reverse=True)

# Print the ranked results
print("\nQuery:", query)
print("\nRanked Results:")

for rank, (snippet, score) in enumerate(results, start=1):
    print(f"{rank}. Score: {score:.4f}")
    print(f"   {snippet}\n")

# Step C: Retrieve the best matching snippet
best_snippet = results[0][0]

# Build a grounded prompt
prompt = f"""
Use ONLY the policy context below to answer the question.

If the answer is not in the context, say:
"I don't have that information."

Context:
{best_snippet}

Question:
{query}
"""

# PRINT THE PROMPT (for debugging / inspection)
print("\n--- PROMPT SENT TO CLAUDE ---")
print(prompt)
print("-----------------------------\n")

# Call Claude Haiku
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

# Print Claude's answer
print("Claude's Answer:")
print(message.content[0].text)

print("\nUsage:")
print(message.usage)