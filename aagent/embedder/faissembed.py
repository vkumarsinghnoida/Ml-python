'''

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS

embedding_function = OllamaEmbeddings(base_url="http://localhost:11434", model="nomic-embed-text")
persist_directory = "./webscraper/wpages"


loader = TextLoader("scraped_data.txt")
text = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
doc_splits = text_splitter.split_documents(text)

vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma",
    embedding=embedding_function,
    persist_directory=persist_directory
)
vectorstore.persist()

vectorstore = FAISS.from_documents(doc_splits, embedding_function)
vectorstore.save_local("faiss_index")

vectorstore =  FAISS.load_local("faiss_index", embedding_function, allow_dangerous_deserialization=True)
#vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)
retriever = vectorstore.as_retriever()

#input_string = str(input("Enter quesrion "))
input_string = "basic ollama embedding rag usage "
context = retriever.get_relevant_documents(input_string)
print(context)
print( " jjf          \
      $)_++$ \
sjfbskfnnd   \
ejjf\
\
dnfn")
context = vectorstore.similarity_search(input_string)
print(context[0].page_content)

context = retriever.get_relevant_documents(input_string)
for a in context:
    print(a.page_content)


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


import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings

# Define the directory where your webscraped text documents are stored.
webscraped_dir = "/workspaces/Ml-python/aagent/webscraper/wpages/"
faiss_index_path = "faiss_index"
# Define the path to the file where processed file names are stored.
processed_files_path = "processed_files.txt"

# Load the list of processed files.
try:
    with open(processed_files_path, 'r') as file:
        processed_files = file.read().splitlines()
except FileNotFoundError:
    processed_files = []

# Initialize the text splitter and the embeddings.
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=3)
embeddings = OllamaEmbeddings(base_url="http://localhost:11434", model="nomic-embed-text")

# Load the FAISS index if it exists.
if os.path.exists(faiss_index_path):
    # Attempt to load the existing FAISS index with dangerous deserialization allowed.
    try:
        db = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
        print("Loaded existing FAISS index.")
    except Exception as e:
        print(f"Failed to load existing FAISS index: {e}")
        # Handle the exception as needed, e.g., create a new index.
else:
    # Create a new FAISS index with dangerous deserialization allowed.
    index = None # Placeholder for the index
    docstore = None # Placeholder for the docstore
    index_to_docstore_id = None # Placeholder for the mapping
    db = FAISS(embeddings, index, docstore, index_to_docstore_id)
    print("Created new FAISS index.")

# Check for new files in the webscraped directory.
for filename in os.listdir(webscraped_dir):
    if filename not in processed_files:
        # Load the new file.
        loader = TextLoader(os.path.join(webscraped_dir, filename))
        documents = loader.load()

        # Split the documents into chunks and embed them.
        docs = text_splitter.split_documents(documents)
        embeddings_list = embeddings.embed_documents(docs)

        # Add the embeddings to the FAISS index.
        db.add_documents(docs)

        # Update the list of processed files.
        processed_files.append(filename)
        with open(processed_files_path, 'a') as file:
            file.write(filename + '\n')
        print(f"Processed and added {filename} to the FAISS index.")

# Save the updated FAISS index.
db.save_local("faiss_index")

print("Finished processing new files.")

