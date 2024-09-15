import os
import shutil
import streamlit as st
import requests

# URL of your FastAPI backend
base_url = "http://localhost:8080/chat_bot"

# Function to call FastAPI endpoints
def call_fastapi(endpoint, params=None):
    try:
        response = requests.post(f"{base_url}{endpoint}", params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

# Streamlit app
st.title("RAG Document Management")

# Initialize session state variables
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Upload file
uploaded_file = st.file_uploader("Upload a document (PDF)", type="pdf")

if uploaded_file is not None:
    # Define the path for the 'data' folder
    data_folder = "data"
    
    # Remove the 'data' folder if it exists and recreate it
    if os.path.exists(data_folder):
        shutil.rmtree(data_folder)  # Delete the folder and all its contents
    os.makedirs(data_folder)  # Recreate the folder
    
    # Define the path for the uploaded file using its original name
    file_name = uploaded_file.name  # Get the original file name
    file_path = os.path.join(data_folder, file_name)
    
    # Save the uploaded file to the 'data' folder with its original name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.write(f"Document '{file_name}' uploaded and saved successfully!")

# Button to trigger data loading
if st.button("Load Data"):
    if uploaded_file is not None:
        # Automatically trigger the API endpoints
        st.write("Triggering FastAPI endpoints...")

        llama_result = call_fastapi("/load-data-llama/")
        if llama_result:
            st.json(llama_result)

        process_result = call_fastapi("/load-data-lang/")
        if process_result:
            st.json(process_result)
        
        st.session_state.data_loaded = True
        st.success("Data loaded successfully!")
    else:
        st.error("Please upload a document before loading data.")

# Chat bot interface
if st.session_state.data_loaded:
    st.write("Select the framework for querying:")
    framework = st.selectbox("Framework", ["Llama Index", "Lang Chain"])

    # Chat interface
    st.write("Chat with the bot:")
    user_query = st.text_input("Enter your message:")

    if st.button("Send"):
        if user_query:
            query_params = {"query": user_query}
            if framework == "Llama Index":
                response = call_fastapi("/query-llama/", params=query_params)
                res = response["response"]
            elif framework == "Lang Chain":
                response = call_fastapi("/query-lang/", params=query_params)
                res = response["content"]
            if response:
                st.session_state.chat_history.append({"user": user_query, "bot": res})
        else:
            st.error("Please enter a message.")

    # Display chat history
    st.write("Chat History:")
    for entry in st.session_state.chat_history:
        st.write(f"**You:** {entry['user']}")
        st.write(f"**Bot:** {entry['bot']}")
    
    # Button to show chat history
    if st.button("Show Chat History"):
        st.write("Chat History:")
        for entry in st.session_state.chat_history:
            st.write(f"**You:** {entry['user']}")
            st.write(f"**Bot:** {entry['bot']}")
else:
    st.write("Please load the data first to enable chatting.")
