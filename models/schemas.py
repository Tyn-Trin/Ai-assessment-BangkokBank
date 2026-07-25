from typing import TypedDict


class GraphState(TypedDict):
    """State ที่ไหลผ่านทั้ง 2 node ใน LangGraph (Data Retriever -> Report Generator)."""

    query: str
    snippets: list[str]
    final_answer: str
