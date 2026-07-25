from typing import TypedDict

from pydantic import BaseModel


class GraphState(TypedDict):
    """State ที่ไหลผ่านทั้ง 2 node ใน LangGraph (Data Retriever -> Report Generator)."""

    query: str
    snippets: list[str]
    final_answer: str


class QueryRequest(BaseModel):
    """Request body ของ POST /query."""

    query: str


class QueryResponse(BaseModel):
    """Response body ของ POST /query."""

    query: str
    snippets: list[str]
    final_answer: str
