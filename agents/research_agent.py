# agents/research_agent.py

import os
import logging
from tools.arxiv_search import search_arxiv
from tools.hf_datasets import find_dataset
from config import VECTOR_STORE_PATH, VECTOR_EMBED_MODEL, NOVELTY_THRESH
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer

# 🧠 Custom wrapper to replace deprecated HuggingFaceEmbeddings
class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        return self.model.encode(texts, show_progress_bar=False).tolist()

    def embed_query(self, text):
        return self.model.encode(text, show_progress_bar=False).tolist()

class ResearchAgent:
    def __init__(self):
        self.embeddings = SentenceTransformerEmbeddings(VECTOR_EMBED_MODEL)
        if os.path.exists(VECTOR_STORE_PATH):
            self.vector_store = FAISS.load_local(
                VECTOR_STORE_PATH, self.embeddings, allow_dangerous_deserialization=True
            )
        else:
            self.vector_store = None

    def run(self, topic: str):
        logging.info(f"🔍 Researching topic: {topic}")
        try:
            topic = topic.strip()
            if not topic:
                raise ValueError("No research topic provided.")

            # Check for novelty using FAISS
            if self.vector_store:
                similar = self.vector_store.similarity_search(topic, k=1)
                if similar and similar[0].metadata.get("score", 0) > NOVELTY_THRESH:
                    topic = f"Novel variant of {topic}"
                    logging.info(f"🧬 Refined topic for novelty: {topic}")

            papers = search_arxiv(topic)
            dataset = find_dataset(topic)

            # Save topic to vector store
            if papers or dataset:
                if self.vector_store is None:
                    self.vector_store = FAISS.from_texts([topic], self.embeddings)
                else:
                    self.vector_store.add_texts([topic], [{"score": 0}])
                self.vector_store.save_local(VECTOR_STORE_PATH)

            logging.info(f"📄 Found {len(papers)} papers and dataset: {dataset.get('name', 'None')}")
            return papers, dataset

        except Exception as e:
            logging.error(f"❌ ResearchAgent failed: {e}")
            return [], {}
