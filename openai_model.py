import openai
import os

class OpenAIChatModel:
    def __init__(self, model="gpt-4", temperature=0, max_tokens=3000, timeout=None, max_retries=4):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.max_retries = max_retries

        # Load OpenAI API key from environment variables
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        openai.api_key = self.api_key

    def invoke(self, prompt):
        # Define a method to invoke the OpenAI API with retries
        for _ in range(self.max_retries):
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                return response.choices[0].message['content']
            except Exception as e:
                print(f"Error during OpenAI API call: {e}")
                continue  # Retry in case of failure
        raise Exception("OpenAI API call failed after retries")

