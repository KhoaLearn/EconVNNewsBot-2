import numpy as np
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os
import pinecone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class QuestionController:
    def __init__(self):
        # Initialize Pinecone using the new API
        self.api_key = os.getenv('PINECONE_API_KEY')
        self.index_name = os.getenv('PINECONE_INDEX_NAME')
        self.environment = os.getenv('PINECONE_ENVIRONMENT')
        self.host = os.getenv('PINECONE_HOST')
        self.region = os.getenv('PINECONE_REGION')

        # Correct Pinecone initialization (no PineconeGRPC)
        pinecone = Pinecone(api_key=self.api_key, 
                            environment=self.region)

        # Connect to the index
        self.index = pinecone.Index(self.index_name, host="https://vn-news-l3hau0c.svc.aped-4627-b74a.pinecone.io")

    
    def query_by_vector(self, input_vector, top_k=10, filter=None):
        """
        Query Pinecone using the input vector and filter.

        Args:
            input_vector (list): Vector đại diện của truy vấn.
            top_k (int): Số lượng kết quả mong muốn.
            filter (dict): Điều kiện lọc (nếu có).

        Returns:
            list: Danh sách kết quả trả về từ Pinecone.
        """
        try:
            result = self.index.query(
                vector=input_vector, 
                top_k=top_k, 
                include_metadata=True,
                filter=filter  
            )
            return result['matches']
        except Exception as e:
            raise RuntimeError(f"Error querying Pinecone: {e}")

    def query_for_thought(self, thought, embedding_model, top_k=10):
        """
        Xử lý Thought để nhúng và truy vấn Pinecone.

        Args:
            thought (str): Thought cần tìm kiếm tài liệu.
            embedding_model (EmbeddingModel): Mô hình nhúng văn bản.
            top_k (int): Số lượng kết quả mong muốn.

        Returns:
            list: Danh sách kết quả tài liệu liên quan.
        """
        try:
            # Embed the thought
            thought_vector = embedding_model.embed_text(thought).flatten().tolist()
            
            # Query Pinecone for related documents
            results = self.query_by_vector(input_vector=thought_vector, top_k=top_k)
            return results
        except Exception as e:
            raise RuntimeError(f"Error processing Thought '{thought}': {e}")