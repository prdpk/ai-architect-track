from pathlib import Path

from langchain_anthropic import ChatAnthropic
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.backends.base import RAGBackend
from app.config import settings


class LangChainRAG(RAGBackend):
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

        # 1. SPLIT
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

        chunks = []

        for policy_file in policy_files:
            policy_text = policy_file.read_text(
                encoding="utf-8"
            )

            file_chunks = splitter.split_text(
                policy_text
            )

            chunks.extend(file_chunks)

        print("\nPolicy Chunks:")

        for i, chunk in enumerate(
            chunks,
            start=1,
        ):
            print(f"{i}. {chunk}\n")

        # 2. EMBEDDINGS
        embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model
        )

        # 3. VECTOR STORE
        vectorstore = Chroma.from_texts(
            texts=chunks,
            embedding=embeddings,
        )

        # 4. RETRIEVER
        retriever = vectorstore.as_retriever(
            search_kwargs={
                "k": settings.top_k,
            }
        )

        # 5. LLM
        llm = ChatAnthropic(
            model=settings.llm_model,
            max_tokens=settings.max_tokens,
            api_key=settings.anthropic_api_key,
        )

        # 6. PROMPT
        prompt = ChatPromptTemplate.from_template(
            """
              Use ONLY the policy context below to answer the question.

              If the answer is not in the context, say:
              "I don't have that information."

              Context:
              {context}

              Question:
              {question}
            """.strip()
        )

        # 7. CHAIN
        self.chain = (
            {
                "context": retriever | self.format_docs,
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
            | StrOutputParser()
        )

    # Helper: convert retrieved Document objects into text
    @staticmethod
    def format_docs(docs) -> str:
        return "\n\n".join(
            doc.page_content
            for doc in docs
        )

    def answer(self, question: str) -> str:
        cleaned_question = question.strip()

        if not cleaned_question:
            raise ValueError(
                "Question cannot be empty."
            )

        return self.chain.invoke(
            cleaned_question
        )