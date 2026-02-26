import os
from pinecone import Pinecone
from src.core.config import config
from langchain_openai import OpenAIEmbeddings

class PineconeService:
    def __init__(self):
        self.api_key = os.getenv("PINECONE_API_KEY", "dummy_key")
        self.enabled = config.integrations.pinecone.enabled
        self.index_name = config.integrations.pinecone.index_name
        
        if self.enabled and self.api_key != "dummy_key":
            self.pc = Pinecone(api_key=self.api_key)
            self.index = self.pc.Index(self.index_name)
            self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY", "dummy_key"))
        else:
            self.pc = None
            self.index = None
            self.embeddings = None

    def query_similar_incidents(self, error_message: str, top_k: int = 5):
        if not self.enabled or not self.index:
            return [] # Returns empty if not configured securely
        
        vector = self.embeddings.embed_query(error_message)
        results = self.index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )
        return results.get("matches", [])

pinecone_service = PineconeService()
