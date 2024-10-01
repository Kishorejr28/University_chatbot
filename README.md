# SaRaH - University Chatbot

## Project Overview

This project involves developing a sophisticated educational chatbot tailored for university needs. It leverages state-of-the-art language models, including LLaMA 3 (8B) and OpenAI's GPT 4 models, with a focus on retrieving relevant information from various university-related documents. The goal is to provide quick, reliable responses to students' queries by referencing course materials, eBooks, lecture notes, and other resources.

The system architecture integrates **Chroma DB** for vector storage, **RAG (Retrieval-Augmented Generation)** for document retrieval, and **LLaMA 3** for language understanding and response generation. This chatbot allows students to retrieve specific information directly from indexed documents, enhancing their learning experience.

## Key Features

- **Vector-Based Search**: Document embeddings are created using Hugging Face models (e.g., `all-MiniLM-L6-v2`), allowing the chatbot to find the most relevant sections of documents.
- **LLaMA 3 Integration**: The chatbot uses the LLaMA 3 model to interpret the user's questions and generate contextually accurate responses.
- **Retrieval-Augmented Generation (RAG)**: Queries are processed using a retrieval-augmented approach, pulling relevant information from indexed documents stored in **Chroma DB**.
- **Scalability**: The chatbot supports indexing large datasets, enabling efficient query handling over a vast range of university-related materials.

## Project Structure

- **Backend Architecture**:
  - **Server Infrastructure**: Built to handle scalable interactions with Chroma DB and LLaMA 3 for efficient processing.
  - **Database**: Vectorized document embeddings are stored in Chroma DB for fast retrieval.
  - **API Integration**: Exposes endpoints to interact with the chatbot interface.

- **Frontend Architecture**:
  - **Streamlined Interface**: Provides an intuitive user interface for students to input queries and receive responses.
  - **Frontend-Backend Interaction**: Seamlessly connects the UI with the backend through an API, ensuring fast responses.

- **Switching Mechanism**:
  - **Model Switching**: Capable of toggling between LLaMA 3 and OpenAI models for performance optimization.
  - **Framework Switching**: Supports transitions between various frameworks depending on the query complexity and response generation requirements.

## Technologies Used

- **Chroma DB**: For storing and retrieving vectorized document embeddings.
- **LLaMA 3 (8B)**: Core language model used for natural language understanding.
- **Hugging Face Embedding**: Used to generate vector embeddings for document searches.
- **Python**: Primary language for the backend.
- **VS Code**: Development environment.

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kishorejr28/university_chatbot.git
   cd university_chatbot
   ```

2. **Install Dependencies**:
   Set up a Python virtual environment and install required libraries:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the Project**:
   Start the backend server:
   ```bash
   python app.py
   ```
   **Run frontend**:
   Start streamlit "
   ```bash
   cd streamlit
   streamlit run app.py
   ```
   
5. **Access the Chatbot**:
   The chatbot can be accessed through the frontend interface or an API.

## Evaluation and Performance Metrics

- **Accuracy of Retrieval**: Benchmarked using MMLU and AGIEval for assessing the chatbot's ability to retrieve accurate responses.
- **Response Latency**: Monitored to ensure fast response times, especially when dealing with large documents.
- **User Feedback**: Collected to evaluate the chatbot's effectiveness in providing relevant answers.


## License

This project is licensed under the MIT License.

---

This `README.md` provides an overview of your chatbot project, explaining its functionality, architecture, setup instructions, and the technologies used. You can update it with additional project details as needed.
