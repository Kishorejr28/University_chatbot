import argparse
import chromadb
from llama_index.core import VectorStoreIndex,Settings,PromptTemplate
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI 
from prompts import FOLLOWUP_QUERY_PROMPT_TEMPLATE, FIRST_QUERY_PROMPT_TEMPLATE, QUERY_CREATION_PROMPT_TEMPLATE  # Importing prompt templates

load_dotenv()

CHROMA_PATH = "chroma_llama"


# Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
# llm = Groq(model="llama3-8b-8192")
# Settings.llm = llm


# Set the embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name="nomic-ai/nomic-embed-text-v1",trust_remote_code=True)


def query_rag_llama(query_text: str, model_choice: str = "groq"):
    # Select the model based on the input
    if model_choice == "groq":
        llm = Groq(model="llama3-8b-8192")
    elif model_choice == "openai":
        llm = OpenAI(model="gpt-4")
    else:
        raise ValueError("Invalid model choice. Use 'groq' or 'openai'.")
    Settings.llm = llm


    # Prepare the Chroma database
    db = chromadb.PersistentClient(path=CHROMA_PATH)
    chroma_collection = db.get_or_create_collection("document_collection")

    # Assign Chroma as the vector store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Load the index from stored vectors
    index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

    # Search for results based on the refined query
    query_engine = index.as_query_engine(similarity_top_k=10)
    results = query_engine.query(query_text)
    response_data = {
        'Response': "",
        'Bot_responce': results.response,
        'Sources': results.metadata,
        'model': model_choice,
        'frame_work': "llama"
    }
    return   response_data 
  
