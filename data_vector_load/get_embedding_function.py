from transformers import AutoModel, AutoTokenizer

class HuggingFaceEmbedding:
    def __init__(self, model_name):
        self.model = AutoModel.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def embed(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
        outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :]
        return embeddings.detach().numpy()[0].tolist()  

    def embed_documents(self, texts):
        return [self.embed(text) for text in texts]
    
    def embed_query(self, text):
        return self.embed(text)

def get_embedding_function():
    return HuggingFaceEmbedding("sentence-transformers/all-MiniLM-L6-v2")



# DistilBERT: 512
# BERT: 512
# Longformer: 4096
# MiniLM: 512
# Sentence-BERT: 512
# USE (Universal Sentence Encoder): 512