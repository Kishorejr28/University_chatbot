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


# Function to get all processed file names from Chroma
def get_processed_files_from_chroma(chroma_client, collection_name="document_collection"):
    try:
        # Get the collection from Chroma
        collection = chroma_client.get_collection(collection_name)

        # Query the collection for all documents and retrieve the file names from the metadata
        results = collection.get(include=["metadatas"])  # Get only metadata
        processed_files = set()
        for item in results['metadatas']:
            processed_files.add(item['file_name'])  # Assuming you store 'file_name' in metadata
        return processed_files
    except Exception as e:
        print(f"Error retrieving processed files from Chroma: {e}")
        return set()



def initialize_index(chroma_path: str = CHROMA_PATH, data_path: str = DATA_PATH, model_name: str = "nomic-ai/nomic-embed-text-v1"):

    Settings.embed_model = HuggingFaceEmbedding(model_name=model_name, trust_remote_code=True)

    chroma_client = chromadb.PersistentClient(path=chroma_path)
    chroma_collection = chroma_client.get_or_create_collection("document_collection")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Get the list of already processed files from Chroma
    processed_files = get_processed_files_from_chroma(chroma_client)

    index = None  # Initialize the index variable

    # Iterate over each file in the data directory
    for file_name in os.listdir(data_path):
        file_path = os.path.join(data_path, file_name)

        # Check if the file is a PDF and has not been processed yet
        if file_name.endswith('.pdf') and file_name not in processed_files:
            print(f"Processing file: {file_name}")

            # Load the document
            documents = load_single_document(file_path)

            # Create index from the loaded document and store metadata (file name)
            index = VectorStoreIndex.from_documents(
                documents, 
                storage_context=storage_context,
                metadata={"file_name": file_name}  # Store the file name in metadata
            )

            print(f"✅ Successfully processed file: {file_name}")
        else:
            print(f"Skipping already processed file: {file_name}")

    if index is None:
        print("No new files processed.")
    return index