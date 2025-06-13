import React, { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
  const [pdfFile, setPdfFile] = useState(null);
  const [filename, setFilename] = useState('');
  const [uploadStatus, setUploadStatus] = useState('');
  const [question, setQuestion] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(true);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatLog, loading]);

  const handleUpload = async () => {
    if (!pdfFile) {
      setUploadStatus('⚠️ Please choose a PDF');
      return;
    }
    setUploadStatus('Uploading...');
    const fd = new FormData();
    fd.append('file', pdfFile);

    try {
      const res = await fetch('http://localhost:8000/upload_pdf/', { method: 'POST', body: fd });
      const data = await res.json();
      if (res.ok) {
        setFilename(data.filename);
        setUploadStatus('✅ PDF uploaded');
      } else {
        throw new Error(data.error || 'Upload failed');
      }
    } catch (e) {
      setUploadStatus(`❌ ${e.message}`);
    }
  };

  const sendMessage = async () => {
    if (!question.trim()) return;
    const userMsg = { sender: 'user', text: question };
    setChatLog(prev => [...prev, userMsg]);
    setQuestion('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/chat_pdf/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename, query: question })
      });
      const data = await res.json();
      const botMsg = { sender: 'bot', text: data.answer };
      setChatLog(prev => [...prev, botMsg]);
    } catch {
      setChatLog(prev => [...prev, { sender: 'bot', text: 'Error fetching answer.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <button className="chat-toggle-btn" onClick={() => setIsChatOpen(o => !o)}>💬</button>
      <div className={`chat-wrapper ${isChatOpen ? 'open' : ''}`}>
        <div className="chat">
          <h2>PDF Chatbot</h2>

          {!filename ? (
            <div className="upload-panel">
              <input type="file" accept="application/pdf" onChange={e => setPdfFile(e.target.files[0])} />
              <button onClick={handleUpload}>Upload</button>
              {uploadStatus && <div className="upload-status">{uploadStatus}</div>}
            </div>
          ) : (
            <>
              <div className="chat-area">
                {chatLog.map((m, i) => (
                  <div key={i} className={`msg ${m.sender}`}>
                    <span>{m.text}</span>
                  </div>
                ))}
                {loading && <div className="msg bot"><em>Typing...</em></div>}
                <div ref={bottomRef} />
              </div>
              <div className="input-area">
                <input
                  value={question}
                  onChange={e => setQuestion(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && sendMessage()}
                  placeholder="Ask something..."
                />
                <button onClick={sendMessage}>Send</button>
              </div>
            </>
          )}
        </div>
      </div>
    </>
  );
}


export default App;

