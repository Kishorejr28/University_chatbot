from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.llms.groq import Groq
from dotenv import load_dotenv
import os
import shutil
load_dotenv()
# Constants for paths
CHROMA_PATH = "chroma_llama"
DATA_PATH = "data"

from chromadb import PersistentClient

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
def initialize_index(chroma_path: str = CHROMA_PATH, data_path: str = DATA_PATH, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", groq_model: str = "llama3-8b-8192"):
    # Set the embedding model and LLM
    delete_collection("document_collection", chroma_path)
    Settings.embed_model = HuggingFaceEmbedding(model_name=model_name)
    llm = Groq(model=groq_model)
    Settings.llm = llm
    # Settings.chunk_size = 1024
    # Settings.chunk_overlap = 20
    # Initialize Chroma client and collection
    chroma_client = chromadb.PersistentClient(path=chroma_path)
    chroma_collection = chroma_client.get_or_create_collection("document_collection")

    # Load documents from directory
    documents = SimpleDirectoryReader(data_path).load_data()

    # Set up vector store and storage context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Create the index from documents
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

    return index
