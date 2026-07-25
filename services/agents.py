"""นิยาม 2 agent nodes (Data Retriever, Report Generator) และประกอบเป็น LangGraph StateGraph."""

from langchain_anthropic import ChatAnthropic
from langgraph.graph import END, START, StateGraph

import config
from models.schemas import GraphState
from services.retriever_tool import search_knowledge_base

_llm = ChatAnthropic(model=config.CLAUDE_MODEL, api_key=config.ANTHROPIC_API_KEY)

_REPORT_GENERATOR_SYSTEM_PROMPT = """\
คุณคือนักเขียนสรุปนโยบายบริษัท หน้าที่ของคุณคือนำ snippet ที่ได้รับมาสังเคราะห์เป็นคำตอบเดียว
ที่ตอบคำถามของ user ให้ครบถ้วน อ่านง่าย จัดรูปแบบดี และไม่ซ้ำซ้อนกัน
ห้ามใส่ข้อมูลที่ไม่มีอยู่ใน snippet ถ้า snippet ไม่มีข้อมูลที่เกี่ยวข้อง ให้บอกตามตรงว่าไม่พบข้อมูล
"""


def data_retriever_node(state: GraphState) -> GraphState:
    """เรียก search_knowledge_base tool ตรงๆ คืน raw snippets เข้า state (ไม่มี LLM เกี่ยวข้อง)."""
    snippets = search_knowledge_base(state["query"])
    return {**state, "snippets": snippets}


def report_generator_node(state: GraphState) -> GraphState:
    """ส่ง query + snippets ให้ Claude สังเคราะห์เป็นคำตอบสุดท้าย."""
    snippets_text = "\n\n".join(state["snippets"])
    user_message = f"คำถาม: {state['query']}\n\nข้อมูลที่เกี่ยวข้อง:\n{snippets_text}"

    response = _llm.invoke(
        [
            ("system", _REPORT_GENERATOR_SYSTEM_PROMPT),
            ("human", user_message),
        ]
    )
    return {**state, "final_answer": response.content}


def build_graph():
    """ประกอบ StateGraph: Data Retriever -> Report Generator แล้ว compile."""
    graph = StateGraph(GraphState)
    graph.add_node("data_retriever", data_retriever_node)
    graph.add_node("report_generator", report_generator_node)

    graph.add_edge(START, "data_retriever")
    graph.add_edge("data_retriever", "report_generator")
    graph.add_edge("report_generator", END)

    return graph.compile()
