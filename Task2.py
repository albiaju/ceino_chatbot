from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
import time

from Task1 import PDFChatHandler, handle_general_question

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pdf_chat_handler: Optional[PDFChatHandler] = None

UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Max 10 MB allowed.")

    timestamp = int(time.time())
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(contents)

    global pdf_chat_handler
    try:
        pdf_chat_handler = PDFChatHandler(file_path)
        return {"message": f"✅ PDF uploaded and saved as '{filename}'."}
    except Exception as e:
        return {"error": f"❌ Failed to process PDF: {str(e)}"}

@app.post("/ask")
async def ask_question(question: str = Form(...)):
    global pdf_chat_handler
    try:
        if pdf_chat_handler:
            answer = pdf_chat_handler.ask(question)
        else:
            answer = handle_general_question(question)
        return {"question": question, "answer": answer}
    except Exception as e:
        return {"error": str(e)}
