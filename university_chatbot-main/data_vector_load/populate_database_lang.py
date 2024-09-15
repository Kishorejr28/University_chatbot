import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings 
from data_vector_load.get_embedding_function import get_embedding_function
from chromadb import PersistentClient

CHROMA_PATH = "chroma_lang"
DATA_PATH = "data"

embedding_function = get_embedding_function()

def load_documents():
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def add_to_chroma(chunks: list[Document]):
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=embedding_function,collection_name="document_collection"
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
    
    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No new documents to add")

def calculate_chunk_ids(chunks):
    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks

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


# Main function to load and process documents
def process_documents():
    try:
        delete_collection("document_collection", CHROMA_PATH)
        # Create (or update) the data store.
        documents = load_documents()
        chunks = split_documents(documents)
        add_to_chroma(chunks)
    except Exception as e:
        print(f"Error processing documents: {e}")
