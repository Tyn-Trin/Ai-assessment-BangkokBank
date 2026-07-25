import os

from dotenv import load_dotenv

load_dotenv()

# --- LLM (Report Generator agent) ---
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-haiku-4-5"

if not ANTHROPIC_API_KEY:
    raise RuntimeError("ANTHROPIC_API_KEY is not set — check your .env file")

# --- Retrieval (Data Retriever agent) ---
KNOWLEDGE_BASE_PATH = "knowledge_base.txt"
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "company_policy"
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
TOP_K = 4  # จำนวน chunk ที่ดึงกลับมาต่อ 1 คำถาม
