import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from data_vector_load.get_embedding_function import get_embedding_function
from dotenv import load_dotenv
import os
load_dotenv()

# os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")

CHROMA_PATH = "chroma_lang"

PROMPT_TEMPLATE = """
                    Answer the question based only on the following context:

                    {context}

                    ---

                    Answer the question based on the above context: {question}

                    ---

                    Chat History:
                    {chat_history}
                    """



def query_rag_lang(query_text: str, chat_history: list):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=10)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    
    # Format chat history for the prompt
    formatted_chat_history = "\n".join([f"Q: {entry['Question']}\nA: {entry['Response']}" for entry in chat_history])

    print(formatted_chat_history,"formatted_chat_history")
    # Create the prompt with context and chat history
    prompt = prompt_template.format(context=context_text, question=query_text, chat_history=formatted_chat_history)

    # Model llama
    model = ChatGroq(
        model="llama3-8b-8192",
        temperature=0,
        max_tokens=3000,
        timeout=None,
        max_retries=4,
    )

    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]

    # Prepare the response structure
    response_data = {
        'Response': response_text.response_metadata,
        'Bot_responce': response_text.content,
        'Sources': sources
    }

    return response_data, context_text  # Return context as well
