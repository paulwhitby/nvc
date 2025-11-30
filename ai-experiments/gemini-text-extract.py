import os
import getpass
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Set your API Key securely
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyCho6VKFwpzrSI69vbknDTZNqXsVgJXjpI"  
    # getpass.getpass("Enter your Google API Key: ")

from langchain_community.document_loaders import PyPDFLoader

# Replace 'your_document.pdf' with the path to your actual PDF file
pdf_path = "pdfs/mg10.pdf"

loader = PyPDFLoader(pdf_path)
docs = loader.load()

print(f"Loaded {len(docs)} pages from the PDF.")

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Size of each chunk in characters
    chunk_overlap=200 # Overlap ensures context isn't lost at the cut point
)

splits = text_splitter.split_documents(docs)

print(f"Split document into {len(splits)} chunks.")


from langchain_community.vectorstores import FAISS

# Initialize Google's embedding model
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Create the vector store locally
vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)

# Create a retriever interface
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0, # 0 means strictly factual, 1 means creative
    max_tokens=None,
    timeout=None,
)


from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Define the instructions for the LLM
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Create the chain that combines documents into a prompt
question_answer_chain = create_stuff_documents_chain(llm, prompt)

# Create the final retrieval chain
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


query = """As a plant ecologist, what are the main conclusions of this document? 
Describe the succession pathways from the source community, 
including the communities successed to and the drivers of succession."""

response = rag_chain.invoke({"input": query})

print("--- Answer ---")
print(response["answer"])

# Optional: Print the sources used to generate the answer
print("\n--- Sources ---")
for doc in response["context"]:
    print(f"Page {doc.metadata['page']}: {doc.page_content[:50]}...")


