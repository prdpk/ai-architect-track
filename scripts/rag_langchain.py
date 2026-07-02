from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Synthetic policy document
policy_document = """
Water damage from burst pipes is covered up to $10,000 with a $500 deductible.
The policy covers accidental pipe failures occurring inside the insured property.
Damage caused by gradual leaks, poor maintenance, or negligence is not covered.
Claims must be reported within 30 days of discovering the damage.

Fire damage to the insured property is covered after a $1,000 deductible.
Coverage includes structural repairs, smoke damage, and debris removal.
Damage caused intentionally by the policyholder is excluded.
Temporary accommodation expenses may also be reimbursed while repairs are underway.

Flood damage caused by natural disasters is not covered under this policy.
Customers must purchase a separate flood insurance policy for protection.
Surface water, storm surge, and overflowing rivers are all considered flood events.
Water entering through open windows during a storm is assessed separately.

Theft of personal belongings is covered up to $5,000 with proof of ownership.
Receipts, photographs, or police reports may be required to support the claim.
Cash, collectibles, and jewelry have separate coverage limits.
The insurer may request additional documentation before approving payment.
"""

# 1. SPLIT (replaces your chunking logic)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)
chunks = splitter.split_text(policy_document)

print("\nChunks:")
for i, c in enumerate(chunks, 1):
    print(f"{i}. {c}\n")

# 2. EMBEDDINGS (same MiniLM model you used manually)
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# 3. VECTOR STORE (replaces Chroma add + manual storage)
vectorstore = Chroma.from_texts(
    texts=chunks,
    embedding=embeddings
)

# 4. RETRIEVER (replaces cosine similarity + top-k logic)
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)

# 5. LLM (replaces Anthropic client call)
llm = ChatAnthropic(
    model="claude-haiku-4-5",
    max_tokens=200
)

# 6. PROMPT (replaces your f-string prompt)
prompt = ChatPromptTemplate.from_template(
    """Use ONLY the policy context below to answer the question.

If the answer is not in the context, say: "I don't have that information."

Context:
{context}

Question: {question}
"""
)

# helper: convert docs → text
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 7. CHAIN (full orchestration: retrieve → format → prompt → LLM)
chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# Run query
query = "Is theft covered?"
answer = chain.invoke(query)

print("\n--- FINAL ANSWER ---")
print(answer)