import pandas as pd
import requests

# Constants
API_BASE_URL = "http://localhost:8080/chat_bot"  # Update this to match your FastAPI base URL
file_name = "SaRaH_Chatbot_evaluation_questions"
EXCEL_FILE = file_name +".xlsx"  # Path to your input Excel file
OUTPUT_FILE = file_name+"llama_groq_results.xlsx"  # Path to save the output Excel file

# Function to read questions from Excel
def read_questions_from_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        return f"Error reading Excel file: {str(e)}"
        

# Function to send each question to the API
def query_lang_api(question, chat_id=None, model_choice=None):
    try:
        data = {"question": question}
        if chat_id:
            data["chat_id"] = chat_id
        if model_choice:
            data["model_choice"] = model_choice
        response = requests.post(f"{API_BASE_URL}/query-llama/", json=data)
        if response.status_code == 200:
            return response.json()      
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Function to iterate over questions, send to API, and save results to Excel
def process_questions_and_save_results():
    # Read input Excel file
    df = pd.read_excel(EXCEL_FILE)
            

    # Prepare new columns for storing API responses
    df['Response'] = ''
    df['Bot_responce'] = ''
    df['Sources'] = ''
    df['Chat_ID'] = ''

    # Iterate over the questions
    for index, row in df.iterrows():
        question = row['Questions']
        
        # Fetch response from API
        api_response = query_lang_api(question,model_choice='groq')
        
        # If API response is valid, store results in the dataframe
        if api_response:
            df.at[index, 'Response'] = api_response.get('Response', '')
            df.at[index, 'Bot_responce'] = api_response.get('Bot_responce', '')
            df.at[index, 'Sources'] = ', '.join(api_response.get('Sources', []))  # Assuming Sources is a list
            df.at[index, 'Chat_ID'] = api_response.get('Chat_ID', '')

    # Save results to a new Excel file
    try:
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"Results saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error saving to Excel: {str(e)}")

# Execute the function
if __name__ == "__main__":
    process_questions_and_save_results()
