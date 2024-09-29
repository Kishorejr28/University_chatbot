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
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{API_BASE_URL}/load-data-lang/", files=files)
        
        if response.status_code == 200:
            st.success("Data loaded successfully!")
        else:
            st.error(f"Error: {response.json()['detail']}")
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