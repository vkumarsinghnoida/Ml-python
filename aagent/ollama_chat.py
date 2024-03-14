#!/root/miniconda3/envs/aagent/bin/python3

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_community import embeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.text_splitter import CharacterTextSplitter

model_local = ChatOllama(model="dolphin-phi")
persist_directory="./hacker"

# 1. Split data into chunks
urls = [
    "https://ollama.com/",
    "https://ollama.com/blog/windows-preview",
    "https://ollama.com/blog/openai-compatibility",
    "https://github.com/pytorch/examples",
]
docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
doc_splits = text_splitter.split_documents(docs_list)

'''
loader = PyPDFLoader("hack.pdf")
doc_splits = loader.load_and_split()
'''
embedding_function = embeddings.OllamaEmbeddings(base_url="http://localhost:11434", model='all-minilm')

# 2. Convert documents to Embeddings and store them
vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma",
    embedding=embedding_function,
    persist_directory=persist_directory
)
vectorstore.persist()


# embedding_function = embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text')


'''
# Load the database from the specified directory with the embedding function
vectorstore = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding_function
)
'''

retriever = vectorstore.as_retriever()

# 3. Before RAG
print("Before RAG\n")
before_rag_template = "{topic}"
before_rag_prompt = ChatPromptTemplate.from_template(before_rag_template)
before_rag_chain = before_rag_prompt | model_local | StrOutputParser()
ques = str(input("Enter question - "))
print(before_rag_chain.invoke({"topic": ques}))

# 4. After RAG
print("\n########\nAfter RAG\n")
after_rag_template = """Answer the question based only on the following context:
{context}
Question: {question}
"""
after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
after_rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | after_rag_prompt
    | model_local
    | StrOutputParser()
)
print(after_rag_chain.invoke(ques))
