import anthropic

from sentence_transformers import SentenceTransformer, CrossEncoder, util

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load cross-encoder reranker
# NOTE: The L6 variant returned NaN scores in this local environment.
# The L12 variant produces finite scores and is used here.
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L12-v2")

# Create Anthropic client for LLM-as-judge
client = anthropic.Anthropic()

# Number of candidates retrieved before reranking
TOP_K = 2


def judge_answerability(question, context):
    """
    Ask Claude whether the retrieved context contains enough
    information to answer the question.

    Returns either "YES" or "NO".
    """

    judge_prompt = f"""
You are evaluating whether retrieved policy context contains enough
information to answer a user's question.

Question:
{question}

Retrieved context:
{context}

Rules:
- Return YES only if the context directly contains enough information
  to answer the question.
- Return NO if the context is unrelated, incomplete, or only discusses
  a different type of damage.
- Do not answer the user's question.
- Respond with only YES or NO.
"""

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=10,
        messages=[
            {
                "role": "user",
                "content": judge_prompt,
            }
        ],
    )

    judgement = message.content[0].text.strip().upper()

    if judgement not in {"YES", "NO"}:
        raise ValueError(
            f"Unexpected judge response: {judgement!r}"
        )

    return judgement


# Synthetic policy document
policy_document = """
Water damage from burst pipes is covered up to $10,000 with a $500 deductible. Claims must be reported within 30 days. Damage caused by poor maintenance or negligence is not covered.

Fire damage to the insured property is covered after a $1,000 deductible. Coverage includes structural repairs, smoke damage, and debris removal. Temporary accommodation expenses are also covered.

Flood damage caused by natural disasters is not covered under this policy. Water entering through open windows during a storm is assessed separately.

Theft of personal belongings is covered up to $5,000 with proof of ownership. Receipts, photographs, or police reports may be required. Cash, collectibles, and jewelry have separate coverage limits.
"""

# Split the policy into structure-aware paragraph chunks
chunks = [
    paragraph.strip()
    for paragraph in policy_document.split("\n\n")
    if paragraph.strip()
]

print("Chunks:\n")

for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i}:")
    print(chunk)
    print()

# Embed chunks once
chunk_embeddings = model.encode(chunks)

# Golden test set
# None means the question is unanswerable from the policy document
test_set = [
    ("Someone stole my phone.", "theft"),
    ("My home was damaged by flames and smoke.", "fire"),
    ("A pipe burst inside my kitchen.", "water"),
    ("My basement became waterlogged during a storm.", "flood"),
    ("Is earthquake damage covered?", None),
]

hits = 0

print("\n===== Retrieval and Answerability Evaluation =====\n")

for question, expected in test_set:

    # Embed the query
    query_embedding = model.encode(question)

    # Compute cosine similarity between query and chunks
    scores = util.cos_sim(
        query_embedding,
        chunk_embeddings,
    )[0]

    # Rank all chunks using cosine similarity
    ranked = sorted(
        zip(chunks, scores),
        key=lambda x: float(x[1]),
        reverse=True,
    )

    # Retrieve the top candidates
    top_chunks = ranked[:TOP_K]

    # Build question-chunk pairs for the CrossEncoder
    pairs = [
        (question, chunk)
        for chunk, _ in top_chunks
    ]

    # Re-score candidates using the CrossEncoder
    rerank_scores = reranker.predict(pairs)

    # Combine each chunk with its cosine and reranker scores,
    # then sort using the reranker score
    reranked = sorted(
        [
            (
                chunk,
                float(cosine_score),
                float(rerank_score),
            )
            for (chunk, cosine_score), rerank_score
            in zip(top_chunks, rerank_scores)
        ],
        key=lambda x: x[2],
        reverse=True,
    )

    # Best candidate after CrossEncoder reranking
    best_chunk = reranked[0][0]

    # Separate LLM call judges whether the best chunk
    # contains enough information to answer the question
    judge_result = judge_answerability(
        question,
        best_chunk,
    )

    if expected is None:
        # Golden set says this question is unanswerable,
        # so the judge should return NO
        found = judge_result == "NO"
    else:
        # Two conditions must pass:
        # 1. The reranker placed the expected chunk first.
        # 2. The judge says the chunk can answer the question.
        correct_chunk = (
            expected.lower() in best_chunk.lower()
        )

        found = (
            correct_chunk
            and judge_result == "YES"
        )

    if found:
        hits += 1
        status = "✓"
    else:
        status = "✗"

    print(f"{status} {question}")
    print(f"   Expected topic: {expected}")
    print(f"   LLM judge: {judge_result}")

    for rank, (
        chunk,
        cosine_score,
        rerank_score,
    ) in enumerate(reranked, start=1):

        print(
            f"   Rank {rank} | "
            f"Cosine: {cosine_score:.4f} | "
            f"Rerank: {rerank_score:.4f}"
        )
        print(f"   {chunk}")
        print()

hit_rate = hits / len(test_set)

print("=" * 50)
print(f"Hits     : {hits}/{len(test_set)}")
print(f"Hit Rate : {hit_rate:.2%}")