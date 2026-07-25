# RAG Policy Assistant

ระบบ Agentic RAG (Retrieval-Augmented Generation) ที่ตอบคำถามเกี่ยวกับนโยบายบริษัท (ภาษาไทย) โดยอัตโนมัติ

ทำงานโดยแปลงคำถามและเอกสารนโยบายให้เป็นเวกเตอร์ด้วยโมเดล `paraphrase-multilingual-MiniLM-L12-v2` (sentence-transformers) เพื่อค้นหาข้อความดิบ (raw snippets) ที่เกี่ยวข้องที่สุดจาก ChromaDB จากนั้นส่งข้อความดิบเหล่านั้นให้ Claude (LLM) สรุปแปลงออกมาเป็นคำตอบที่อ่านง่าย

จัดลำดับการทำงานทั้งหมด (ค้นหา → สรุปคำตอบ) ด้วย **LangGraph** โดยแยกเป็น 2 agent ที่ทำงานต่อกันเป็นลำดับ (multi-agent orchestration): Data Retriever agent ค้นหาข้อมูลอย่างเดียว ไม่ตอบคำถามเอง และ Report Generator agent สังเคราะห์คำตอบจากข้อมูลที่ได้รับมาเท่านั้น

## Flow การทำงาน

### 1. Encode (Build Index) — ทำครั้งเดียวตอนเริ่มระบบ

อ่านเอกสารนโยบายทั้งหมด ตัดเป็น chunk ตามย่อหน้า แปลงแต่ละ chunk เป็นเวกเตอร์ด้วยโมเดล embedding แล้วเก็บลง ChromaDB ไว้ล่วงหน้า ขั้นตอนนี้ไม่มี LLM เข้ามาเกี่ยวข้อง เป็นการเตรียมข้อมูลให้พร้อมค้นหาเท่านั้น

<!-- แปะรูป sequence diagram flow ที่ 1 (encode) ตรงนี้ -->

### 2. Query — ทำงานทุกครั้งที่มีคำถามเข้ามา

แปลงคำถามของ user เป็นเวกเตอร์ด้วยโมเดลตัวเดียวกับตอน encode แล้วนำไปเทียบกับเวกเตอร์ที่เก็บไว้ใน ChromaDB เพื่อหา chunk ที่ใกล้เคียงที่สุด จากนั้นส่งข้อความดิบเหล่านั้นให้ Claude สังเคราะห์เป็นคำตอบสุดท้ายพร้อมแสดงแหล่งอ้างอิงกลับไปให้ user

<!-- แปะรูป sequence diagram flow ที่ 2 (query) ตรงนี้ -->

## Screenshot

<!-- แปะรูปหน้าจอการรันจริงตรงนี้ (หน้าเว็บถาม-ตอบ, แหล่งอ้างอิง, คลังนโยบาย) -->

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

### รันแบบ CLI

```bash
python main.py
```

รันตัวอย่างคำถามให้ทันที พร้อม auto-build ChromaDB index ในการรันครั้งแรก

### รันแบบเว็บ

```bash
uvicorn api:app --reload --port 8000
```

เปิด `http://localhost:8000` ถามคำถามผ่านหน้าเว็บ, ดูแหล่งอ้างอิง, และดูคลังนโยบายทั้งหมดได้


