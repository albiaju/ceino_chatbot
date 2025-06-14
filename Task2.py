from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Task1 import pdf_qa_system
import os
import shutil
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PDF Chat Assistant API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_DIR = "uploaded_pdfs"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
os.makedirs(UPLOAD_DIR, exist_ok=True)


class ChatRequest(BaseModel):
    filename: str
    query: str
    temperature: Optional[float] = 0.7


@app.post("/upload", response_model=dict)
async def upload_pdf(file: UploadFile = File(...)):
    """Handle PDF file upload and validation"""
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            logger.warning(f"Invalid file type attempted: {file.filename}")
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )

        # Validate file size
        file_size = 0
        temp_path = os.path.join(UPLOAD_DIR, f"temp_{file.filename}")

        with open(temp_path, "wb") as buffer:
            while content := await file.read(8192):  # 8KB chunks
                file_size += len(content)
                if file_size > MAX_FILE_SIZE:
                    os.remove(temp_path)
                    raise HTTPException(
                        status_code=413,
                        detail=f"File too large. Max size is {MAX_FILE_SIZE // (1024 * 1024)}MB"
                    )
                buffer.write(content)

        # Finalize upload
        final_path = os.path.join(UPLOAD_DIR, file.filename)
        os.rename(temp_path, final_path)

        logger.info(f"Successfully uploaded: {file.filename}")
        return {
            "filename": file.filename,
            "status": "success",
            "size": file_size
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"File upload failed: {str(e)}"
        )


@app.post("/chat", response_model=dict)
async def chat_with_pdf(request: ChatRequest):
    """Process chat queries about uploaded PDFs"""
    try:
        pdf_path = os.path.join(UPLOAD_DIR, request.filename)

        # Validate PDF exists
        if not os.path.exists(pdf_path):
            raise HTTPException(
                status_code=404,
                detail="PDF not found. Please upload first."
            )

        # Validate query
        if not request.query.strip():
            raise HTTPException(
                status_code=400,
                detail="Query cannot be empty"
            )

        logger.info(f"Processing query for {request.filename}: {request.query}")
        answer = pdf_qa_system.process_query(pdf_path, request.query)

        return {
            "answer": answer,
            "filename": request.filename
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing your query: {str(e)}"
        )


@app.get("/health", response_model=dict)
async def health_check():
    """Service health check"""
    return {
        "status": "healthy",
        "service": "PDF Chat Assistant",
        "upload_dir": UPLOAD_DIR
    }