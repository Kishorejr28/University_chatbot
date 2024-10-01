import os
import shutil
import json
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_chroma import Chroma
from data_vector_load.get_embedding_function import get_embedding_function

# Constants for paths
CHROMA_PATH = "chroma_lang"
DATA_PATH = "data"
METADATA_FILE = "processed_files.json"

# Embedding function
embedding_function = get_embedding_function()

# Function to reset the Chroma database
def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

# Function to load a single PDF document
def load_single_document(file_path: str):
    document_loader = PyPDFLoader(file_path)
    return document_loader.load()

# Function to split documents into chunks
def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

# Function to calculate chunk IDs
def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id
        chunk.metadata["id"] = chunk_id

    return chunks

# Function to add documents to Chroma
def add_to_chroma(chunks: list[Document]):
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=embedding_function
    )
    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if new_chunks:
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No new documents to add")

# Function to read processed files from metadata
def read_processed_files():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            return set(json.load(f))
    return set()

# Function to write processed files to metadata
def write_processed_file(file_name):
    processed_files = read_processed_files()
    processed_files.add(file_name)
    with open(METADATA_FILE, 'w') as f:
        json.dump(list(processed_files), f)

# Function to clean up metadata by removing entries for files that no longer exist
def cleanup_metadata():
    processed_files = read_processed_files()
    actual_files = set(os.listdir(DATA_PATH))

    # Keep only files that exist in the actual folder
    valid_files = processed_files.intersection(actual_files)

    if valid_files != processed_files:
        print("Cleaning up metadata...")
        with open(METADATA_FILE, 'w') as f:
            json.dump(list(valid_files), f)
        print(f"Removed {processed_files - valid_files} from metadata.")

# Main function to load and process documents
def process_documents(reset_db: bool = False):
    if reset_db:
        print("✨ Clearing Database")
        clear_database()

    # Clean up metadata before processing
    cleanup_metadata()

    processed_files = read_processed_files()

    for file_name in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, file_name)
        
        if file_name.endswith('.pdf') and file_name not in processed_files:
            print(f"Processing file: {file_name}")
            
            documents = load_single_document(file_path)
            chunks = split_documents(documents)
            add_to_chroma(chunks)
            write_processed_file(file_name)
            print(f"✅ Successfully processed file: {file_name}")
        else:
            print(f"Skipping already processed file: {file_name}")
