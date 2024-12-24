from transformers import AutoModel, AutoTokenizer
import torch

class EmbeddingModel:
    def __init__(self):
        # Initialize the tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained('jinaai/jina-embeddings-v3', trust_remote_code=True)
        self.model = AutoModel.from_pretrained('jinaai/jina-embeddings-v3', trust_remote_code=True)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)  # Move the model to the GPU if available
    
    def embed_text(self, text):
        # Tokenize the input text
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        inputs = {key: value.to(self.device) for key, value in inputs.items()}  # Move inputs to the correct device

        # Get the embeddings from the model
        with torch.no_grad():  # Disable gradient calculations for faster inference
            outputs = self.model(**inputs)

        # Extract the embeddings (typically from the last hidden state or pooled output)
        embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()  # Example: mean pooling of last hidden state

        return embeddings

    def batch_embed(self, texts):
        # Encode multiple texts at once
        embeddings = []
        for text in texts:
            embeddings.append(self.embed_text(text))
        return embeddings
