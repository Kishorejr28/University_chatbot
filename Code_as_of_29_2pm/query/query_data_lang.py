import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from data_vector_load.get_embedding_function import get_embedding_function
from prompts import FOLLOWUP_QUERY_PROMPT_TEMPLATE, FIRST_QUERY_PROMPT_TEMPLATE, QUERY_CREATION_PROMPT_TEMPLATE
from dotenv import load_dotenv
import os
load_dotenv()

# os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")

CHROMA_PATH = "chroma_lang"

def generate_followup_query(query_text: str,chat_history: list):
    # Format the chat history for the prompt
    formatted_chat_history1 = "\n".join([f"Previous Question : {entry['Question']}\n" for entry in chat_history][-2:])

    # Use the prompt template to generate a follow-up question based on chat history
    prompt_template = ChatPromptTemplate.from_template(QUERY_CREATION_PROMPT_TEMPLATE)
    prompt = prompt_template.format(chat_history=formatted_chat_history1,current_question=query_text )

    # Model llama
    model = ChatGroq(
        model="llama3-8b-8192",
        temperature=0,
        max_tokens=3000,
        timeout=None,
        max_retries=4,
    )

    followup_query = model.invoke(prompt)

    return followup_query.content  # This is the generated follow-up question



def query_rag_lang(query_text: str, chat_history: list = None, model_choice: str = "groq"):
    # Check if the query is a generic follow-up like "tell me more"
    if chat_history and query_text.lower():
        # Generate a more specific follow-up query based on chat history
        query_text = generate_followup_query(chat_history=chat_history,query_text=query_text)
        print("query_text:--------------\n",query_text)
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB with the refined query.
    results = db.similarity_search_with_score(query_text, k=10)

    # Extract the current context from the search results
    current_context = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    # print("current_context:--------------\n",current_context)
    # Choose the appropriate prompt based on whether there is chat history
    if chat_history:
        formatted_chat_history = "\n".join([f"Previous Question: {entry['Question']}\n Previous Bot Response: {entry['Response']}" for entry in chat_history][-1:])
        prompt_template = ChatPromptTemplate.from_template(FOLLOWUP_QUERY_PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=current_context, question=query_text, chat_history=formatted_chat_history)
    else:
        prompt_template = ChatPromptTemplate.from_template(FIRST_QUERY_PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=current_context, question=query_text)

    
    # Select the model based on the input
    if model_choice == "groq":
        model = ChatGroq(
            model="llama3-8b-8192",
            temperature=0,
            max_tokens=3000,
            timeout=None,
            max_retries=4,
        )
    elif model_choice == "openai":
        model = ChatOpenAI(
            model="gpt-4",
            temperature=0,
            max_tokens=3000,
            timeout=None,
            max_retries=4,
        )
    else:
        raise ValueError("Invalid model choice. Use 'groq' or 'openai'.")

    # Invoke the model to get the response
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]

    # Prepare the response structure
    response_data = {
        'Response': response_text.response_metadata,
        'Bot_responce': response_text.content,
        'Sources': sources,
        'model': model_choice,
        'frame_work': "lang"
    }
    # print("Bot_responce:", response_text.content)
    return response_data, current_context  # Return context as well
