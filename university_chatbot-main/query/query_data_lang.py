import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
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
"""



def query_rag_lang(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=10)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)
    # model llama

    model = ChatGroq(
        model="llama3-8b-8192",
        temperature=0,
        max_tokens=1024,
        timeout=None,
        max_retries=2,
        # stream=True,
        stop=None,
    )

    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text

