from pathlib import Path

from langchain_anthropic import ChatAnthropic
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


POLICIES_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "policies"
)

policy_files = sorted(POLICIES_DIR.glob("*.txt"))

if not policy_files:
    raise RuntimeError(
        f"No .txt policy documents found in: {POLICIES_DIR}"
    )


# 1. SPLIT
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
)

chunks = []

for policy_file in policy_files:
    policy_text = policy_file.read_text(
        encoding="utf-8"
    )

    file_chunks = splitter.split_text(policy_text)

    chunks.extend(file_chunks)

# 2. EMBEDDINGS
embeddings = HuggingFaceEmbeddings(
    model_name=(
        "sentence-transformers/"
        "all-MiniLM-L6-v2"
    )
)


# 3. VECTOR STORE
vectorstore = Chroma.from_texts(
    texts=chunks,
    embedding=embeddings,
)


# 4. RETRIEVER
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 2,
    }
)


# 5. LLM
llm = ChatAnthropic(
    model="claude-haiku-4-5",
    max_tokens=200,
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


# Helper: convert retrieved Document objects into text
def format_docs(docs) -> str:
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


# 7. CHAIN
chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)


def answer(question: str) -> str:
    cleaned_question = question.strip()

    if not cleaned_question:
        raise ValueError(
            "Question cannot be empty."
        )

    return chain.invoke(cleaned_question)