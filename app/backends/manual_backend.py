from pathlib import Path

import anthropic
import chromadb
from sentence_transformers import SentenceTransformer

from app.backends.base import RAGBackend
from app.config import settings


class ManualRAG(RAGBackend):
    def __init__(self) -> None:
        # Locate the policy documents folder
        policies_dir = (
            Path(__file__).resolve().parent.parent.parent
            / "data"
            / "policies"
        )

        policy_files = sorted(
            policies_dir.glob("*.txt")
        )

        if not policy_files:
            raise RuntimeError(
                "No .txt policy documents found in: "
                f"{policies_dir}"
            )

        # Create the persistent ChromaDB client and collection
        self.db = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = self.db.get_or_create_collection(
            name="policies"
        )

        # Load the embedding model
        self.model = SentenceTransformer(
            settings.embedding_model
        )

        # Create the Anthropic client
        self.client = anthropic.Anthropic(
            api_key=settings.anthropic_api_key
        )

        # Read all policy documents
        policy_documents = [
            policy_file.read_text(encoding="utf-8")
            for policy_file in policy_files
        ]

        # Chunk every document by blank lines
        chunks = []

        for policy_document in policy_documents:
            file_chunks = [
                chunk.strip()
                for chunk in policy_document.split("\n\n")
                if chunk.strip()
            ]

            chunks.extend(file_chunks)

        print("Policy Chunks:\n")

        for i, chunk in enumerate(chunks, start=1):
            print(f"{i}. {chunk}\n")

        # Store chunks in ChromaDB only once
        if self.collection.count() == 0:
            embeddings = self.model.encode(chunks)

            print(
                "Embedding shape:",
                embeddings.shape,
            )

            self.collection.add(
                documents=chunks,
                embeddings=embeddings.tolist(),
                ids=[
                    f"chunk_{i}"
                    for i in range(len(chunks))
                ],
            )

            print("Embedded and stored chunks.")
        else:
            print(
                "Chunks already stored — skipping embedding."
            )

    def answer(self, question: str) -> str:
        query = question.strip()

        if not query:
            raise ValueError(
                "Question cannot be empty."
            )

        # Embed the user query
        query_embedding = self.model.encode(query)

        # Retrieve top-k matching chunks from ChromaDB
        results = self.collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=settings.top_k,
        )

        retrieved = results["documents"][0]
        distances = results["distances"][0]

        print("\nQuery:", query)
        print("\nRetrieved Chunks:\n")

        for rank, (chunk, distance) in enumerate(
            zip(retrieved, distances),
            start=1,
        ):
            print(
                f"{rank}. Distance: {distance:.4f}"
            )
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
        message = self.client.messages.create(
            model=settings.llm_model,
            max_tokens=settings.max_tokens,
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

        return message.content[0].text