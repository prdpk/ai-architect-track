import logging
from pathlib import Path

import anthropic
import chromadb
from sentence_transformers import SentenceTransformer

from app.backends.base import RAGBackend
from app.config import settings

logger = logging.getLogger(__name__)


class ManualRAG(RAGBackend):
    def __init__(self) -> None:
        logger.info("Initializing Manual RAG backend")

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
            logger.error(
                "No .txt policy documents found in: %s",
                policies_dir,
            )
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

        logger.info(
            "Loaded %d chunks from %d policy files",
            len(chunks),
            len(policy_files),
        )
        logger.debug(
            "Chunks:\n%s",
            "\n".join(
                f"{i}. {chunk}"
                for i, chunk in enumerate(chunks, start=1)
            ),
        )

        # Store chunks in ChromaDB only once
        if self.collection.count() == 0:
            embeddings = self.model.encode(chunks)

            logger.debug(
                "Embedding shape: %s",
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

            logger.info("Embedded and stored chunks")
        else:
            logger.info(
                "Chunks already stored — skipping embedding"
            )

    def answer(self, question: str) -> str:
        query = question.strip()

        if not query:
            logger.warning("Received an empty question")
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

        logger.debug("Query: %s", query)
        logger.debug(
            "Retrieved chunks:\n%s",
            "\n".join(
                f"{rank}. Distance: {distance:.4f} | {chunk}"
                for rank, (chunk, distance) in enumerate(
                    zip(retrieved, distances),
                    start=1,
                )
            ),
        )

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

        logger.debug("Prompt sent to Claude:\n%s", prompt)

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

        answer_text = message.content[0].text

        logger.debug("Claude's answer: %s", answer_text)
        logger.debug("Usage: %s", message.usage)

        return answer_text
