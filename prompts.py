# prompts.py

# Template for the first query (no chat history)
FIRST_QUERY_PROMPT_TEMPLATE = """
                                ---------------------
                                {context}
                                ---------------------
                                Given the information from multiple sources and not prior knowledge, answer the query.
                                Query: {question}
                                Answer:
                    """


# Template for follow-up queries (with chat history)
FOLLOWUP_QUERY_PROMPT_TEMPLATE = """
                                ---------------------
                                {context}
                                ---------------------
                                Given the information from multiple sources and not prior knowledge, answer the query.
                                Query: {question}
                                Providing the chat history for improving the responce
                                Chat History:
                                {chat_history}
                                If the previous response to a similar question was inadequate, focus on correcting or improving the answer this time.
                                Answer:
                    """

# Template for generating queries based on the chat history (useful for follow-up queries)
QUERY_CREATION_PROMPT_TEMPLATE = """
                    Based on the chat history, review the Current Question: {current_question}. 
                    If the current question is clear and specific (e.g., "Tell me about data modeling"), do not modify or rephrase the question. 
                    Only rephrase when the question is unclear or references a previous question ambiguously.

                    strictly if above condition fails then only follow below command if its necessary, else you will be punished : 
                    
                    If the current question is vague or implies a continuation of a previous question (e.g., "Tell me more about it", "What else can you add?", "Can you explain further?"),
                    then generate a refined question using the context from the chat history.                    
                    Chat History:
                    {chat_history}
                    Strictly output the final question for further processing—no excess information or explanations.
                    
                    """


# More prompts can be added as needed for various situations.
