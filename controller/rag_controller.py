import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

class RAGController:
    def __init__(self, question_controller, embedding_model):
        """
        Khởi tạo RAGController.
        
        Args:
            question_controller (QuestionController): Đối tượng để truy vấn Pinecone.
            embedding_model (EmbeddingModel): Mô hình nhúng văn bản.
        """
        self.question_controller = question_controller
        self.embedding_model = embedding_model
        openai.api_key = os.getenv('OPENAI_API_KEY')  # Load OpenAI API key

    def retrieve_documents(self, thought, top_k=5):
        """
        Tìm kiếm tài liệu liên quan nhất cho một Thought từ Pinecone.

        Args:
            thought (str): Thought cần tìm kiếm tài liệu.
            top_k (int): Số lượng tài liệu tối đa cần lấy.

        Returns:
            list: Danh sách các tài liệu liên quan.
        """
        try:
            # Nhúng Thought để tạo vector
            thought_vector = self.embedding_model.embed_text(thought).flatten().tolist()

            # Truy vấn tài liệu liên quan từ Pinecone
            documents = self.question_controller.query_by_vector(input_vector=thought_vector, top_k=top_k)

            # Trả về tài liệu dưới dạng danh sách
            return [
                {
                    "title": doc.get("metadata", {}).get("title", "N/A"),
                    "content": doc.get("metadata", {}).get("content", "N/A"),
                    "url": doc.get("metadata", {}).get("url", "N/A"),
                    "published_date": doc.get("metadata", {}).get("published_date", "N/A"),
                }
                for doc in documents
            ]
        except Exception as e:
            raise RuntimeError(f"Error retrieving documents for Thought: {e}")

    def refine_thought(self, query, original_thought, related_documents):
        """
        Chỉnh sửa (refine) Thought dựa trên tài liệu liên quan.

        Args:
            query (str): Truy vấn gốc từ người dùng.
            original_thought (str): Thought ban đầu.
            related_documents (list): Danh sách các tài liệu liên quan.

        Returns:
            str: Thought đã chỉnh sửa (refined Thought).
        """
        try:
            # Chuẩn bị các tài liệu liên quan cho prompt
            docs_summary = "\n".join(
                [f"- Title: {doc['title']}\n Published Date: {doc['published_date']}\n Content: {doc['content'][:300]}..." for doc in related_documents]
            )

            # Prompt để refine Thought
            prompt = f"""
            User Query: {query}

            Original Thought: {original_thought}

            Related Documents:
            {docs_summary}

            Based on the related documents, refine the original Thought. 
            Ensure the refined Thought is accurate, concise, and aligns with the information provided.
            """
            # Gọi OpenAI API để refine Thought
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a reasoning assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7,
            )

            # Lấy Thought đã chỉnh sửa từ response
            refined_thought = response['choices'][0]['message']['content'].strip()
            return refined_thought
        except Exception as e:
            raise RuntimeError(f"Error refining Thought: {e}")

    def process_thought(self, query, thought, top_k=3):
        """
        Xử lý một Thought: Tìm kiếm tài liệu và refine Thought.

        Args:
            query (str): Câu hỏi ban đầu của người dùng.
            thought (str): Thought cần xử lý.
            top_k (int): Số lượng tài liệu tối đa để lấy.

        Returns:
            dict: Thought đã xử lý bao gồm bản gốc, tài liệu liên quan, và bản refined.
        """
        try:
            # Lấy tài liệu liên quan
            related_documents = self.retrieve_documents(thought, top_k=top_k)

            # Refine Thought dựa trên tài liệu
            refined_thought = self.refine_thought(query, thought, related_documents)

            return {
                "original_thought": thought,
                "related_documents": related_documents,
                "refined_thought": refined_thought,
            }
        except Exception as e:
            raise RuntimeError(f"Error processing Thought '{thought}': {e}")
