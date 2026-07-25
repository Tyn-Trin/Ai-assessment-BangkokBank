"""จัดการ ChromaDB: ตัด chunk จาก knowledge_base.txt, embed, เก็บ/ค้นหาเวกเตอร์."""

import chromadb
from sentence_transformers import SentenceTransformer

import config

_model = SentenceTransformer(config.EMBEDDING_MODEL)
_client = chromadb.PersistentClient(path=config.CHROMA_DIR)


def _read_chunks() -> list[str]:
    """อ่าน knowledge_base.txt แล้วตัด chunk ตามย่อหน้า (บรรทัดว่างคั่น)."""
    with open(config.KNOWLEDGE_BASE_PATH, encoding="utf-8") as f:
        text = f.read()
    return [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]


def build_index() -> None:
    """สร้าง ChromaDB collection จาก knowledge_base.txt ถ้ายังไม่เคยสร้าง (idempotent)."""
    collection = _client.get_or_create_collection(config.COLLECTION_NAME)

    if collection.count() > 0:
        return

    chunks = _read_chunks()
    embeddings = _model.encode(chunks).tolist()
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(ids=ids, documents=chunks, embeddings=embeddings)


def search(query: str, top_k: int = config.TOP_K) -> list[str]:
    """ค้นหา chunk ที่ใกล้เคียงกับ query ที่สุดจาก ChromaDB."""
    collection = _client.get_collection(config.COLLECTION_NAME)
    query_embedding = _model.encode([query]).tolist()

    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    return results["documents"][0]


if __name__ == "__main__":
    build_index()
    print("ทดสอบค้นหา:", search("ลาป่วยได้กี่วัน?"))
