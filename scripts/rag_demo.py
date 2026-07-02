from sentence_transformers import SentenceTransformer, util
import anthropic

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create the Anthropic client
client = anthropic.Anthropic()

# Number of snippets to retrieve
TOP_K = 2

# Similarity threshold (heuristic)
SIMILARITY_THRESHOLD = 0.30

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
#best_snippet = results[0][0]

# Retrieve the top-k matches
top_results = results[:TOP_K]

print(f"Top {TOP_K} Retrieved Snippets:\n")

for rank, (snippet, score) in enumerate(top_results, start=1):
    print(f"{rank}. Score: {float(score):.4f}")
    print(f"   {snippet}\n")

best_score = float(top_results[0][1])

# Only call Claude if the best match is above the threshold
if best_score < SIMILARITY_THRESHOLD:
    print(
        f"No relevant policy found "
        f"(best score = {best_score:.4f} < {SIMILARITY_THRESHOLD})"
    )
else:
    # Combine the top-k snippets into a single context
    context = "\n".join(
        snippet for snippet, _ in top_results
    )

# Build a grounded prompt
    prompt = f"""
Use ONLY the policy context below to answer the question.

If the answer is not in the context, say:
"I don't have that information."

Context:
{context}

Question:
{query}
"""

    # Print the prompt
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