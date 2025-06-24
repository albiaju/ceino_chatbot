# 🧠 AI-Powered Chatbot with PDF Intelligence & Memory

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com/)

A sophisticated full-stack AI chatbot that seamlessly combines **conversational AI** with **document intelligence**. Chat naturally with persistent memory or upload PDFs to unlock intelligent document analysis—all powered by cutting-edge AI technologies.



---

## ✨ Features

### 🗣️ **Intelligent Conversations**
- **Persistent Memory**: Maintains context across conversations
- **Natural Language**: Powered by OpenAI GPT-4o for human-like interactions
- **Real-time Responses**: Instant AI-powered replies

### 📄 **Document Intelligence** 
- **PDF Upload & Analysis**: Extract insights from uploaded documents
- **Semantic Search**: FAISS-powered vector embeddings for precise content retrieval
- **Question Answering**: Ask specific questions about document content

### 🏗️ **Modern Architecture**
- **RESTful API**: FastAPI backend with automatic documentation
- **Responsive UI**: React frontend optimized for all devices
- **Scalable Design**: Modular architecture for easy expansion

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **AI Engine** | OpenAI GPT-4o | Natural language processing & generation |
| **Framework** | LangChain | AI agents, memory management, and tools |
| **Document Processing** | PyPDF2, RecursiveCharacterTextSplitter | PDF parsing and text chunking |
| **Vector Database** | FAISS | Semantic search and document retrieval |
| **Backend API** | FastAPI, Pydantic, Uvicorn | High-performance async API |
| **Frontend** | React, Axios | Interactive user interface |
| **Development** | Python 3.8+, Node.js | Development environment |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- OpenAI API key

### 1. Clone the Repository
```bash
git clone https://github.com/albiaju/ceino_chatbot.git
cd ceino_chatbot
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the `backend/` directory:
```env
OPENAI_API_KEY=your-openai-api-key-here
```

### 4. Start the Backend Server
```bash
uvicorn Task2:app --reload
```
🌐 **API Documentation**: http://localhost:8000/docs

### 5. Frontend Setup
```bash
# Open new terminal and navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```
🖥️ **Application**: http://localhost:3000

---

## 💡 Usage Examples

### Memory-Powered Conversations
```
User: "My name is Sarah and I'm a data scientist"
Bot: "Nice to meet you, Sarah! ..."

User: "What's my profession?"
Bot: "You're a data scientist, Sarah!"
```

### PDF Document Analysis
1. Upload a research paper or manual
2. Ask: "What are the key findings in section 3?"
3. Get precise, context-aware answers from your document

### Continuous Context
- No need to repeat information
- Builds on previous conversations
- Maintains topic coherence across sessions

---

## 📁 Project Structure

```
ceino_chatbot/
├── backend/
│   ├── Task1.py              # Core LangChain logic and memory management
│   ├── Task2.py              # FastAPI application and API endpoints
│   ├── requirements.txt      # Python dependencies
│   ├── uploaded_pdfs/        # PDF storage directory
│   └── .env                  # Environment variables (create this)
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API communication
│   │   └── ...
│   ├── package.json          # Node.js dependencies
│   └── public/
└── README.md
```

---

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat` | Send message and receive AI response |
| `POST` | `/upload-pdf` | Upload PDF document for analysis |
| `GET` | `/health` | Check API health status |
| `GET` | `/docs` | Interactive API documentation |

---




## 🌟 Roadmap & Future Enhancements

### Short Term
- [ ] **Text Highlighting**: Visual PDF text highlighting in frontend
- [ ] **Multi-PDF Support**: Handle multiple documents simultaneously
- [ ] **Export Conversations**: Download chat history as PDF/TXT

### Medium Term
- [ ] **Persistent Storage**: Redis/ChromaDB integration for permanent memory
- [ ] **User Authentication**: Personalized sessions and chat history
- [ ] **Advanced Analytics**: Conversation insights and usage metrics

### Long Term
- [ ] **Multi-Modal AI**: Image and voice input support
- [ ] **Plugin System**: Extensible tool integration
- [ ] **Cloud Deployment**: Docker containerization and cloud-ready setup

---

## 👥 Meet the Team

This project is brought to you by a dedicated team of AI engineers and developers:

### **Albi Aju**

- 💼 [LinkedIn](https://www.linkedin.com/in/albi-aju-249391296/)
- 🐙 [GitHub](https://github.com/albiaju)
- 🔧 Specializes in natural language interfaces and backend architecture

### **Jeswin James Binu**

- 💼 [LinkedIn](https://www.linkedin.com/in/jeswin-james-binu-b63aa02aa/)
- 🐙 [GitHub](https://github.com/jeswinjamesbinu2262084)
- 🔧 Focuses on AI model integration and frontend development

---

## 🙏 Acknowledgments

- OpenAI for GPT-4o API
- LangChain team for the excellent framework
- FastAPI and React communities
- Contributors and beta testers

---

<div align="center">



Built  by [Albi Aju](https://github.com/albiaju) & [Jeswin James Binu](https://github.com/jeswinjamesbinu2262084)

</div>
