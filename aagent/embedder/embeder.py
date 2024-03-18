import uuid
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
import chromadb

# Define the directory where your webscraped text documents are stored.
webscraped_dir = "/workspaces/Ml-python/aagent/webscraper/wpages/"
chroma_db_path = "./chroma_db" # Path to save the Chroma database
processed_files_path = "processed_files.txt"
collection_name = "webscraped_documents" # Name of the collection in Chroma

# Load the list of processed files.
try:
    with open(processed_files_path, 'r') as file:
        processed_files = file.read().splitlines()
except FileNotFoundError:
    processed_files = []

# Initialize the text splitter and the embeddings.
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=3)
embeddings = OllamaEmbeddings(base_url="http://localhost:11434", model="nomic-embed-text")

# Initialize the Chroma persistent client and get or create the collection
persistent_client = chromadb.PersistentClient()
collection = persistent_client.get_or_create_collection(collection_name)

# Check for new files in the webscraped directory.
for filename in os.listdir(webscraped_dir):
    if filename not in processed_files:
        # Load the new file.
        loader = TextLoader(os.path.join(webscraped_dir, filename))
        documents = loader.load()

        # Split the documents into chunks and embed them.
        docs = text_splitter.split_documents(documents)
#        embeddings_list = embeddings.embed_documents(docs)

        unique_id = str(uuid.uuid4())
        unique_filename = f"{filename}_{unique_id}" 

        # Prepare the data for adding to the collection
        ids = [unique_filename] * len(docs) # Assuming each document is uniquely identified by the filename
        metadatas = [{"source": filename} for _ in docs] # Optional metadata
        documents_content = [doc.page_content for doc in docs]
 #       embeddings_content = [embedding.tolist() for embedding in embeddings_list] # Convert embeddings to list for storage
        ids = [str(i) for i in range(1, len(documents_content) + 1)]
        # Add the documents and their embeddings to the Chroma collection.
  #      collection.add(ids=ids, metadatas=metadatas, documents=documents_content, embeddings=embeddings_content)
        collection.add(ids=ids, metadatas=metadatas, documents=documents_content)

        # Update the list of processed files.
        processed_files.append(filename)
        with open(processed_files_path, 'a') as file:
            file.write(filename + '\n')
        print(f"Processed and added {filename} to the Chroma collection.")

print("Finished processing new files and adding to Chroma collection.")
langchain_chroma = Chroma(
    client=persistent_client,
    collection_name=collection_name,
    embedding_function=embeddings,
)
