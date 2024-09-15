# Example FastAPI usage
from fastapi import FastAPI,APIRouter
from data_vector_load.populate_database_llama import initialize_index
from data_vector_load.populate_database_lang import process_documents
from query.query_data_lang import query_rag_lang
from query.query_data_llama import query_rag_llama
router = APIRouter()

@router.post("/load-data-llama/")
async def load_data_llama():
    index = initialize_index()
    return {"message": "Data loaded successfully!"}


@router.post("/load-data-lang/")
async def load_data_lang():
    process_documents()
    return {"message": "Documents processed successfully!"}


@router.post("/query-llama/")
async def query_llama(query:str):
    res = query_rag_llama(query)
    return res


@router.post("/query-lang/")
async def query_lang(query:str):
    res = query_rag_lang(query)
    return res
