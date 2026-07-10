from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L6-v2",
    device="cpu",
)

pairs = [
    (
        "How many people live in Berlin?",
        "Berlin had a population of 3,520,031 registered inhabitants.",
    ),
    (
        "How many people live in Berlin?",
        "Berlin is well known for its museums.",
    ),
]

scores = reranker.predict(pairs)

print("Scores:", scores)
print("Model device:", reranker.device)