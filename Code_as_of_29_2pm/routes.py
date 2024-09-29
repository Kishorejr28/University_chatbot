# Example FastAPI usage
from fastapi import APIRouter, UploadFile, File, Form,HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any,Optional
from enum import Enum
from data_vector_load.populate_database_llama import initialize_index
from data_vector_load.populate_database_lang import process_documents
from query.query_data_lang import query_rag_lang
from query.query_data_llama import query_rag_llama
from db_actions import create_chat_id, get_history_by_id, update_chat_history,get_last_n_chat_history,get_recent_lang_chats,get_recent_llama_chats
router = APIRouter()
import os

DATA_PATH = "data"

class ModelChoice(str, Enum):
    groq = "groq"
    openai = "openai"

class QueryRequest(BaseModel):
    question: str
    chat_id: Optional[str] = None
    model_choice: ModelChoice = ModelChoice.groq  # Default value set to "groq"

class QueryResponse(BaseModel):
    Response: Dict[str, Any]
    Content: str
    Sources: List[str]
    Chat_History: List[Dict[str, str]]

class ChatHistoryResponse(BaseModel):
    chat_id: str
    history: List[Dict[str, str]]


@router.post("/load-data-llama/")
async def load_data_llama():
    index = initialize_index()
    return {"message": "Data loaded successfully!"}

@router.post("/query-llama/")
async def query_llama(request: QueryRequest):
    try:
        print("requests =============\n",request)
        # If chat_id is provided, retrieve the history; otherwise, create a new chat session
        # Initialize the chat_id
        chat_id = request.chat_id
        print("requests =============\n",request)
        # If chat_id is provided, retrieve the history; otherwise, create a new chat session
        if chat_id:
            chat_history = get_history_by_id(chat_id)
            if chat_history is None:
                raise HTTPException(status_code=404, detail="Chat history not found")
        else:
            chat_id = create_chat_id()  # Create a new chat session
            chat_history = []
        
        # Call the query_rag_lang function with the question and chat history
        response_data = query_rag_llama(request.question, request.model_choice.value)
        print(response_data,"======60")
        update_chat_history(chat_id=chat_id, question=request.question, context=response_data['Response'], response = response_data['Bot_responce']
                            ,model_choice=response_data['model'],frame_work_used=response_data['frame_work'])
        # # Update chat history in the DB
        # Return the response along with the chat_id
        return {
            "Response": response_data['Response'],
            "Bot_responce": response_data['Bot_responce'],
            "Sources": response_data['Sources'],
            "Chat_ID": chat_id  # Return the chat_id to the client
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/load-data-lang/")
async def load_data_lang(
    reset_db: bool = Form(False),  # To handle the reset flag
    file: UploadFile = File(default=None)  # To handle uploaded file 
    ):
    # Save the uploaded file if provided and it does not already exist
    if file:
        file_path = os.path.join(DATA_PATH, file.filename)

        # Check if the file already exists
        if os.path.exists(file_path):
            print(f"File '{file.filename}' already exists. Skipping upload.")
        else:
            with open(file_path, "wb") as f:
                f.write(await file.read())
            print(f"File uploaded: {file.filename}")

    # Process the documents in the data folder
    process_documents(reset_db)
    
    return {"message": "Documents processed successfully!"}

@router.post("/query-lang/")
async def query_rag(request: QueryRequest):
    try:
        # Initialize the chat_id
        chat_id = request.chat_id
        print("requests =============\n",request)
        # If chat_id is provided, retrieve the history; otherwise, create a new chat session
        if chat_id:
            chat_history = get_history_by_id(chat_id)
            if chat_history is None:
                raise HTTPException(status_code=404, detail="Chat history not found")
        else:
            chat_id = create_chat_id()  # Create a new chat session
            chat_history = []

        
        # Call the query_rag_lang function with the question and chat history
        response_data, context_text = query_rag_lang(request.question, chat_history, request.model_choice.value)
        # Update chat history in the DB
        
        update_chat_history(chat_id=chat_id, question=request.question, context=context_text, response = response_data['Bot_responce']
                            ,model_choice=response_data['model'],frame_work_used=response_data['frame_work'])

        # Return the response along with the chat_id
        return {
            "Response": response_data['Response'],
            "Bot_responce": response_data['Bot_responce'],
            "Sources": response_data['Sources'],
            "Chat_ID": chat_id  # Return the chat_id to the client
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/last-chat-history/", response_model=List[ChatHistoryResponse])  # Use the new response model
async def last_chat_history(n: int = 3):  # Allow the user to specify how many threads to retrieve
    try:
        # Fetch the last n chat histories
        last_chats = get_last_n_chat_history(n)
        
        # Format the response
        formatted_chats = [
            {
                "chat_id": chat['chat_id'],
                "history": chat['history']
            }
            for chat in last_chats
        ]
        
        return formatted_chats  # Return the formatted response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Route to get the recent 'lang' chats
@router.get("/recent-lang-chats/", response_model=List[ChatHistoryResponse])
async def recent_lang_chats(n: int = 3):  # Allow the user to specify the number of chats to retrieve
    try:
        # Fetch the recent lang chats
        recent_chats = get_recent_lang_chats(limit=n)

        # Format the response
        formatted_chats = [
            {
                "chat_id": chat['chat_id'],
                "history": [
                    {
                        "Question": chat['Question'],
                        "Context": chat['Context'],
                        "Response": chat['Response'],
                        "model": chat['model'],
                        "frame_work": chat['frame_work']
                    }
                ]
            }
            for chat in recent_chats
        ]

        return formatted_chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# Route to get the recent 'llama' chats
@router.get("/recent-llama-chats/", response_model=List[ChatHistoryResponse])
async def recent_lang_chats(n: int = 3):  # Allow the user to specify the number of chats to retrieve
    try:
        # Fetch the recent llama chats
        recent_chats = get_recent_llama_chats(limit=n)

        # Format the response
        formatted_chats = [
            {
                "chat_id": chat['chat_id'],
                "history": [
                    {
                        "Question": chat['Question'],
                        "Context": chat['Context'],
                        "Response": chat['Response'],
                        "model": chat['model'],
                        "frame_work": chat['frame_work']
                    }
                ]
            }
            for chat in recent_chats
        ]

        return formatted_chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))