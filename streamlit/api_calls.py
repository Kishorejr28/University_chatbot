# api_helpers.py

import requests
import streamlit as st

API_BASE_URL = "http://localhost:8080/chat_bot"  # Update this to match your FastAPI base URL

def query_lang_api(question, chat_id=None,model_choice = None):
    try:
        data = {"question": question}
        if chat_id:
            data["chat_id"] = chat_id
        if model_choice:  # Include model_choice if it is provided
            data["model_choice"] = model_choice
        response = requests.post(f"{API_BASE_URL}/query-lang/", json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.json()['detail']}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def load_data_api(uploaded_file):
    try:
        # Prepare the file data, including the original filename
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        
        # Send the file to both endpoints
        response_lang = requests.post(f"{API_BASE_URL}/load-data-lang/", files=files)
        response_llama = requests.post(f"{API_BASE_URL}/load-data-llama/", files=files)
        
        # Check responses and handle success or error
        if response_lang.status_code == 200 and response_llama.status_code == 200:
            response_json_llama = response_llama.json()
            response_json_lang = response_lang.json()
            
            if response_json_llama.get('message') and response_json_lang.get('message'):
                st.success("Documents processed successfully!")
        else:
            st.error(f"Error: {response_lang.json().get('detail', 'Unknown error')}")
            st.error(f"Error: {response_llama.json().get('detail', 'Unknown error')}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def get_llama_chat_history(n=3):
    response = requests.get(f"{API_BASE_URL}/recent-llama-chats/?n={n}")
    if response.status_code == 200:
        return response.json()  # Parse the JSON response
    else:
        st.error("Error fetching chat history")
        return None  # Explicitly return None or an empty list
    
def get_lang_chat_history(n=3):
    response = requests.get(f"{API_BASE_URL}/recent-lang-chats/?n={n}")
    if response.status_code == 200:
        return response.json()  # Parse the JSON response
    else:
        st.error("Error fetching chat history")
        return None  # Explicitly return None or an empty list
    


def query_llama_api(question, chat_id=None,model_choice = None):
    try:
        data = {"question": question}
        if chat_id:
            data["chat_id"] = chat_id
        if model_choice:  # Include model_choice if it is provided
            data["model_choice"] = model_choice
        response = requests.post(f"{API_BASE_URL}/query-llama/", json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.json()['detail']}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None