# RAG Assistant

ระบบ Agentic RAG (Retrieval-Augmented Generation) ที่ตอบคำถามเกี่ยวกับนโยบายบริษัท (ภาษาไทย) โดยอัตโนมัติ

ทำงานโดยแปลงคำถามและเอกสารนโยบายให้เป็นเวกเตอร์ด้วยโมเดล `paraphrase-multilingual-MiniLM-L12-v2` (sentence-transformers) เพื่อค้นหาข้อความดิบ (raw snippets) ที่เกี่ยวข้องที่สุดจาก ChromaDB จากนั้นส่งข้อความดิบเหล่านั้นให้ Claude (LLM) สรุปแปลงออกมาเป็นคำตอบที่อ่านง่าย

จัดลำดับการทำงานทั้งหมด (ค้นหา → สรุปคำตอบ) ด้วย **LangGraph** โดยแยกเป็น 2 agent ที่ทำงานต่อกันเป็นลำดับ (multi-agent orchestration): Data Retriever agent ค้นหาข้อมูลอย่างเดียว ไม่ตอบคำถามเอง และ Report Generator agent สังเคราะห์คำตอบจากข้อมูลที่ได้รับมาเท่านั้น

## Screenshot

ตัวอย่างคำถามที่ไม่ใช่แค่ดึง Raw ดิบมาแต่มีการส่งให้ Ai agent ทำการคิดประมวลคำตอบออกมาด้วย

<img width="1920" height="919" alt="image" src="https://github.com/user-attachments/assets/6d8584a3-efac-4980-bb87-68f031067d31" />

<img width="646" height="912" alt="image" src="https://github.com/user-attachments/assets/d9ac3abf-103e-4792-bb89-56a7bd79bab6" />


## Flow การทำงาน

### 1. Encode (Build Index) — ทำครั้งเดียวตอนเริ่มระบบ

อ่านเอกสารนโยบายทั้งหมด ตัดเป็น chunk ตามย่อหน้า แปลงแต่ละ chunk เป็นเวกเตอร์ด้วยโมเดล embedding แล้วเก็บลง ChromaDB ไว้ล่วงหน้า ขั้นตอนนี้ไม่มี LLM เข้ามาเกี่ยวข้อง เป็นการเตรียมข้อมูลให้พร้อมค้นหาเท่านั้น

<img width="5895" height="3070" alt="Rag-BangkokBank-2026-07-25-135113" src="https://github.com/user-attachments/assets/b2976e0a-1397-4bd8-959e-bc07f74c3454" />


### 2. Query — ทำงานทุกครั้งที่มีคำถามเข้ามา

แปลงคำถามของ user เป็นเวกเตอร์ด้วยโมเดลตัวเดียวกับตอน encode แล้วนำไปเทียบกับเวกเตอร์ที่เก็บไว้ใน ChromaDB เพื่อหา chunk ที่ใกล้เคียงที่สุด จากนั้นส่งข้อความดิบเหล่านั้นให้ Claude สังเคราะห์เป็นคำตอบสุดท้ายพร้อมแสดงแหล่งอ้างอิงกลับไปให้ user

<img width="8192" height="3029" alt="Chat Ai-2026-07-25-134907" src="https://github.com/user-attachments/assets/c4ea650c-0d75-485e-9812-95f77e818ac3" />




## Tech Stack

| ส่วน | ใช้ |
|---|---|
| Orchestration | LangGraph |
| LLM | Claude (`claude-haiku-4-5` ผ่าน `langchain-anthropic`) |
| Embedding | `paraphrase-multilingual-MiniLM-L12-v2` (`sentence-transformers`) |
| Vector store | ChromaDB |
| Backend | FastAPI |
| Frontend | HTML / CSS / JavaScript (ไม่มี framework, ไม่มี build step) |

## วิธีใช้งาน

### ติดตั้ง

```bash
pip install -r requirements.txt
cp .env.example .env   # แล้วใส่ ANTHROPIC_API_KEY จริงของคุณ
```


### รันแบบเว็บ

```bash
uvicorn api:app --reload --port 8000
```

เปิด `http://localhost:8000` ถามคำถามผ่านหน้าเว็บ, ดูแหล่งอ้างอิง, และดูคลังนโยบายทั้งหมดได้


