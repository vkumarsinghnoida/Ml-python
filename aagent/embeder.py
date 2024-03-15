from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS

embedding_function = OllamaEmbeddings(base_url="http://localhost:11434", model="nomic-embed-text")
persist_directory = "./ocagents"


loader = TextLoader("scraped_data.txt")
text = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
doc_splits = text_splitter.split_documents(text)
'''
vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma",
    embedding=embedding_function,
    persist_directory=persist_directory
)
vectorstore.persist()
'''
vectorsctore = FAISS.from_documents(doc_splits, embedding_function)
vectorstore.save_local("faiss_index")

#vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)
retriever = vectorstore.as_retriever()

#input_string = str(input("Enter quesrion "))
input_string = "basic ollama embedding rag usage "
context = retriever.get_relevant_documents(input_string)
print(context)

context = retriever.similarity_search(input_string)
print(context)


def query_database(query, vectorstore):
    # Convert the query to an embedding
    query_embedding = embedding_function._embed(query)

    # Query the vectorstore to find the most relevant chunks
    most_relevant_chunk_ids = vectorstore.search(query_embedding, search_type = 'similarity')

    # Fetch the corresponding text chunks
    related_chunks_text = []
    for chunk_id in most_relevant_chunk_ids:
        chunk_text = vectorstore.get_document_by_id(chunk_id)
        related_chunks_text.append(chunk_text)

    return related_chunks_text


'''
related_chunks_text = query_database(input_string, vectorstore)

for chunk_text in related_chunks_text:
    print(chunk_text)
'''
