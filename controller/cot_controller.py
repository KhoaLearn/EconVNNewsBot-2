import openai
import os
from dotenv import load_dotenv
from controller.rag_controller import RAGController  # RAGController để rerank articles

# Load environment variables from the .env file
load_dotenv()

class CoTController:
    def __init__(self):
        """
        Initialize CoTController with OpenAI API key.
        """
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key  # Set the API key for OpenAI globally

    def generate_cot(self, query: str) -> list:
        """
        Generate Chain-of-Thought (CoT) from the user's query.

        Args:
            query (str): The user's question or query.

        Returns:
            list: A list of thoughts (step-by-step reasoning).
        """
        prompt = f"""
        You are a reasoning assistant. Break down the user's question into a step-by-step reasoning process.
        Each step (thought) should be concise and focus on a single key aspect of the reasoning.

        Provide exactly 3 thoughts. Each thought should be independent and self-contained,
        suitable for embedding and querying external knowledge databases.

        Format should follow:
        Thought 1: concise reasoning about the first aspect
        
        Thought 2: concise reasoning about the second aspect
        
        Thought 3: concise reasoning about the third aspect

        Question: {query}
        """
        try:
            # Call OpenAI's ChatCompletion API
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a reasoning assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            # Extract the response content
            content = response['choices'][0]['message']['content']
            # Split the content into individual thoughts based on lines
            thoughts = [line.strip() for line in content.split("\n") if line.strip()]
            return thoughts
        except Exception as e:
            raise RuntimeError(f"Error generating CoT: {e}")
