from fastapi import APIRouter

from models.schemas import QueryRequest, QueryResponse
from services.agents import build_graph

router = APIRouter(prefix="/query", tags=["query"])

_graph = build_graph()


@router.post("", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    result = _graph.invoke({"query": request.query, "snippets": [], "final_answer": ""})
    return QueryResponse(**result)
