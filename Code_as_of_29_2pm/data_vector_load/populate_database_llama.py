from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.llms.groq import Groq
from dotenv import load_dotenv
load_dotenv()
# Constants for paths
CHROMA_PATH = "chroma_llama"
DATA_PATH = "data"
import os
from chromadb import PersistentClient

# Helper function to load a single document
def load_single_document(file_path: str):
    # Use SimpleDirectoryReader to load data from a single file
    return SimpleDirectoryReader(input_files=[file_path]).load_data()


def delete_collection(collection_name: str, chroma_path: str = CHROMA_PATH):
    try:
        # Initialize the PersistentClient with the path to the Chroma database
        chroma_client = PersistentClient(path=chroma_path)
        # Delete the collection
        try:
            chroma_client.delete_collection(collection_name)
            print(f"Collection {collection_name} deleted successfully.")
        except:
            print("collection is not there")
    except Exception as e:
        raise Exception(f"Unable to delete collection: {e}")


# Function to initialize the index and load data
def initialize_index(chroma_path: str = CHROMA_PATH, data_path: str = DATA_PATH, model_name: str = "nomic-ai/nomic-embed-text-v1"):

    Settings.embed_model = HuggingFaceEmbedding(model_name=model_name,trust_remote_code=True)

    chroma_client = chromadb.PersistentClient(path=chroma_path)
    chroma_collection = chroma_client.get_or_create_collection("document_collection")

    # Set up vector store and storage context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Load and process PDF files one by one
    processed_files = set()  # Keep track of already processed files

    # Iterate over each file in the data directory
    for file_name in os.listdir(data_path):
        file_path = os.path.join(data_path, file_name)

        # Check if the file is a PDF and has not been processed yet
        if file_name.endswith('.pdf') and file_name not in processed_files:
            print(f"Processing file: {file_name}")

            # Load the document
            documents = load_single_document(file_path)

            # Create index from the loaded document
            index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

            # Optionally, you can persist the index if needed
            # index.save("index_path")

            print(f"✅ Successfully processed file: {file_name}")

            # Add file to the processed list to avoid reprocessing
            processed_files.add(file_name)
        else:
            print(f"Skipping already processed file: {file_name}")

    return index
