from sentence_transformers import SentenceTransformer, util

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def chunk_text(text, chunk_size=40, overlap=10):
    """Split text into overlapping chunks."""
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


# Synthetic policy document
policy_document = """
Water damage from burst pipes is covered up to $10,000 with a $500 deductible. Claims must be reported within 30 days. Damage caused by poor maintenance or negligence is not covered.

Fire damage to the insured property is covered after a $1,000 deductible. Coverage includes structural repairs, smoke damage, and debris removal. Temporary accommodation expenses are also covered.

Flood damage caused by natural disasters is not covered under this policy. Water entering through open windows during a storm is assessed separately.

Theft of personal belongings is covered up to $5,000 with proof of ownership. Receipts, photographs, or police reports may be required. Cash, collectibles, and jewelry have separate coverage limits.
"""

# Experiment with these values
CHUNK_SIZE = 40
OVERLAP = 10
TOP_K = 2
SIMILARITY_THRESHOLD = 0.45

# Create chunks
chunks = chunk_text(policy_document, CHUNK_SIZE, OVERLAP)

print("Chunks:\n")
for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i}:")
    print(chunk)
    print()

# Embed chunks once
chunk_embeddings = model.encode(chunks)

# Golden test set
test_set = [
    ("Someone stole my phone.", "theft"),
    ("My home was damaged by flames and smoke.", "fire"),
    ("A pipe burst inside my kitchen.", "water"),
    ("My basement became waterlogged during a storm.", "flood"),
    ("Is earthquake damage covered?", None),
]

hits = 0

print("\n===== Retrieval Evaluation =====\n")

for question, expected in test_set:

    # Embed query
    query_embedding = model.encode(question)

    # Compute cosine similarity
    scores = util.cos_sim(query_embedding, chunk_embeddings)[0]

    # Rank chunks
    ranked = sorted(
        zip(chunks, scores),
        key=lambda x: float(x[1]),
        reverse=True,
    )

    top_chunks = ranked[:TOP_K]

    # Get the highest similarity score
    best_score = float(top_chunks[0][1])

    if expected is None:
        # For an unanswerable question, pass only when
        # the best score is below the threshold
        found = best_score < SIMILARITY_THRESHOLD
    else:
        # For an answerable question, check whether the expected
        # keyword appears in any top-k retrieved chunk
        found = any(
            expected.lower() in chunk.lower()
            for chunk, _ in top_chunks
        )

    if found:
        hits += 1
        status = "✓"
    else:
        status = "✗"

    print(f"{status} {question}")

    if expected is None:
        print(
            f"   Unanswerable check: best score "
            f"{best_score:.4f}, threshold {SIMILARITY_THRESHOLD}"
        )

    for chunk, score in top_chunks:
        print(f"   Score: {float(score):.4f}")
        print(f"   {chunk}")
        print()

hit_rate = hits / len(test_set)

print("=" * 40)
print(f"Hits     : {hits}/{len(test_set)}")
print(f"Hit Rate : {hit_rate:.2%}")