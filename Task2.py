from fastapi import FastAPI, File, UploadFile, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from Task1 import generate_pdf_qa_agent, chat_with_pdf_agent
import os

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
async def startup_event():
    print("\n✅ FastAPI server started!")
    print("🔗 API:  http://127.0.0.1:8000")
    print("📘 Docs: http://127.0.0.1:8000/docs\n")

# Chat request model
class ChatRequest(BaseModel):
    filename: str
    query: str

# Endpoint for PDF upload
@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        generate_pdf_qa_agent(file_path)
        return JSONResponse(content={"message": "PDF uploaded and agent initialized.", "filename": file.filename})
    except Exception as e:
        print(f"❌ Error: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Endpoint for querying PDF (boxed input in Swagger)
@app.post("/chat_pdf/")
async def chat_pdf(request: ChatRequest = Body(...)):
    try:
        answer = chat_with_pdf_agent(request.filename, request.query)
        return JSONResponse(content={"answer": answer})
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return JSONResponse(content={"answer": "Query failed"}, status_code=500)
