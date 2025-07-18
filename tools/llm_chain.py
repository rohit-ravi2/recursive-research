# tools/llm_chain.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv

load_dotenv()

SYSTEM = "You are an expert AI research assistant. Think critically and explain thoroughly."

# ✅ Define LLM
llm = ChatOllama(
    model="mistral",  # or your chosen model
    temperature=0.7,
)

# ✅ Create prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    ("user", "{input}")
])

# ✅ Compose pipeline
llm_chain = prompt.pipe(llm)
