import argparse
import chromadb
from llama_index.core import VectorStoreIndex,Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = "chroma_llama"


Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = Groq(model="llama3-8b-8192")
Settings.llm = llm


def query_rag_llama(query_text: str):
    # Prepare the DB.
    db = chromadb.PersistentClient(path=CHROMA_PATH)  # Make sure this is correctly used.
    # get collection
    chroma_collection = db.get_or_create_collection("document_collection")

    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)


    # load your index from stored vectors
    index = VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context)
    
    query_engine = index.as_query_engine(similarity_top_k = 10)
    response = query_engine.query(query_text)
    print(response)

    
    # prompt = prompt_template.format(context=context_text, question=query_text)
    return response


