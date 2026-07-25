"""Custom tool ของ Data Retriever agent: ค้นหา snippet ที่เกี่ยวข้องกับ query จาก knowledge base."""

from services import vector_store


def search_knowledge_base(query: str) -> list[str]:
    """ค้นหา chunk ที่ใกล้เคียง query ที่สุดจาก ChromaDB คืน raw snippets เท่านั้น (ไม่สังเคราะห์คำตอบ)."""
    return vector_store.search(query)
