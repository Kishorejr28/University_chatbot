# prompts.py

# prompts.py

# Template for the welcome message
WELCOME_PROMPT_TEMPLATE = """
                    Welcome to SaRaH! How can I assist you today?
                    """

# Template for the first query (no chat history)
FIRST_QUERY_PROMPT_TEMPLATE = """
                    You are an expert assistant. Answer the user's question strictly based on the provided context. 
                    Do not rely on any external knowledge or assumptions outside of the given context.

                    {context}

                    ---

                    Answer the following question based solely on the above context: {question}

                    If the context does not provide enough information to answer the question, respond with "Currently, I don't have information about that. But, let me check for you using Llama 3 or OpenAI GPT-4."

                    Do not include any restatements of the context. Just give a final answer.

                    Final Answer: 
                    """



# Template for follow-up queries (with chat history)
FOLLOWUP_QUERY_PROMPT_TEMPLATE = """
                    Thank you for your patience! Let's find the best answer for you. Answer the question based strictly on the following context. If the context is insufficient or unclear, provide the most relevant response using the available information.

                    {context}

                    ---

                    Now, answer the user's current question based on the context above: {question}

                    ---

                    To ensure the best possible response, consider the following chat history for added clarification:
                    Chat History:
                    {chat_history}

                    If the previous response to a similar question was inadequate, focus on correcting or improving the answer this time.
                    If there isn't enough information, respond with "I currently don't have that information, but let me search for you using Llama 3 or OpenAI GPT-4."
                    Do not include any explanations or restatements of the context.
                    """


# Template for generating queries based on the chat history (useful for follow-up queries)
QUERY_CREATION_PROMPT_TEMPLATE = """
                    Based on the chat history, review the Current Question: {current_question}. 
                    If the current question is clear and specific (e.g., "Tell me about data modeling"), do not modify or rephrase the question. 
                    Only rephrase when the question is unclear or references a previous question ambiguously.

                    Strictly follow the conditions above. 

                    If the current question is vague or implies a continuation of a previous question (e.g., "Tell me more about it", "What else can you add?", "Can you explain further?"),
                    then generate a refined question using the context from the chat history.                    
                    Chat History:
                    {chat_history}
                    Strictly output the final question for further processing—no excess information or explanations.
                    
                    """
