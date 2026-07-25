"""Entry point: auto-build ChromaDB index ถ้ายังไม่มี แล้วรัน query ตัวอย่างผ่าน LangGraph."""

import os

import config
from services import vector_store
from services.agents import build_graph

SAMPLE_QUERIES = [
    "พนักงานลาป่วยได้กี่วันต่อปี?",
    "นโยบายการเดินทางไปต่างประเทศเป็นยังไง?",
    "ทำงานล่วงเวลาได้ค่าตอบแทนไหม?",
]


def main() -> None:
    if not os.path.exists(config.CHROMA_DIR):
        print("ยังไม่มี chroma_db/ กำลัง build index...")
        vector_store.build_index()

    graph = build_graph()

    for query in SAMPLE_QUERIES:
        print(f"\n{'=' * 60}")
        print(f"คำถาม: {query}")
        print("=" * 60)

        result = graph.invoke({"query": query, "snippets": [], "final_answer": ""})

        print(f"\nคำตอบ:\n{result['final_answer']}")


if __name__ == "__main__":
    main()
