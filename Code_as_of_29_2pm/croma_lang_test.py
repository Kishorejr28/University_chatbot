import json
import csv
import chromadb
from langchain_chroma import Chroma
from data_vector_load.get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma_lang"
embedding_function = get_embedding_function()

def query_chroma_metadata(output_format='json'):
    try:
        # Initialize the Chroma client
        client = chromadb.Client()

        # Check if the collection exists
        collections = client.list_collections()
        print("Available collections:", collections)
        
        # Get the collection
        db = Chroma(
            persist_directory=CHROMA_PATH, embedding_function=embedding_function, collection_name="document_collection"
        )
        print(f"Collection '{db._collection_name}' retrieved.")
        
        # Retrieve all documents and metadata from the collection
        results = db.get()
        metadata_list = results.get('metadatas', [])  # Ensure this is a list
        documents = results.get('documents', [])  # Ensure this is a list
        
        if not metadata_list or not documents:
            print("No documents or metadata found in the collection.")
            return
        
        print(f"Metadata count: {len(metadata_list)}")
        print(f"Documents count: {len(documents)}")
        
        # Combine documents and metadata
        combined_list = []
        for metadata, doc in zip(metadata_list, documents):
            combined_list.append({
                "id": metadata.get("id", ""),
                "page": metadata.get("page", ""),
                "source": metadata.get("source", ""),
                "content": doc
            })
        
        # Choose how to output the file
        if output_format == 'json':
            # Save metadata and content to a JSON file
            with open('chroma_metadata.json', 'w') as json_file:
                json.dump(combined_list, json_file, indent=4)
            print("Metadata and content saved to chroma_metadata.json")
        elif output_format == 'csv':
            # Save metadata and content to a CSV file
            keys = combined_list[0].keys()  # Assuming all entries have the same keys
            with open('chroma_metadata.csv', 'w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=keys)
                writer.writeheader()
                writer.writerows(combined_list)
            print("Metadata and content saved to chroma_metadata.csv")
        else:
            print(f"Unsupported format: {output_format}")
    
    except Exception as e:
        print(f"Error querying Chroma metadata: {e}")

query_chroma_metadata(output_format='json')
