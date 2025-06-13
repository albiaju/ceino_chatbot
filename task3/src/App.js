import React, { useState } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);

  const sendMessage = async () => {
    if (!question.trim()) return;

    const userMessage = { sender: 'user', text: question };
    setChatLog((prevLog) => [...prevLog, userMessage]);
    setQuestion('');
    setLoading(true);

    try {
      const response = await fetch(`http://127.0.0.1:8000/chat/${encodeURIComponent(question)}`);
      const data = await response.json();

      setTimeout(() => {
        const botMessage = { sender: 'bot', text: data.answer };
        setChatLog((prevLog) => [...prevLog, botMessage]);
        setLoading(false);
      }, 1500);
    } catch (error) {
      console.error('Error:', error);
      setChatLog((prevLog) => [...prevLog, { sender: 'bot', text: 'Sorry, something went wrong.' }]);
      setLoading(false);
    }
  };

  return (
    <>
      <button className="chat-toggle-btn" onClick={() => setIsChatOpen(!isChatOpen)}>
        💬
      </button>

      <div className={`chat-container-wrapper ${isChatOpen ? 'open' : ''}`}>
        <div className="chat-container">
          <h1>Chatbot</h1>

          <div className="chat-box">
            {chatLog.map((msg, index) => (
              <div className={`chat-msg ${msg.sender}`} key={index}>
                {msg.sender === 'bot' && (
                  <img className="chat-avatar" src="https://img.icons8.com/?size=100&id=WZolzyWpK1CQ&format=png&color=000000" alt="Bot" />
                )}
                <div className="chat-text">{msg.text}</div>
                {msg.sender === 'user' && (
                  <img className="chat-avatar" src="https://img.icons8.com/?size=100&id=7820&format=png&color=000000" alt="User" />
                )}
              </div>
            ))}
            {loading && (
              <div className="chat-msg bot">
                <img className="chat-avatar" src="https://img.icons8.com/?size=100&id=WZolzyWpK1CQ&format=png&color=000000" alt="Bot" />
                <div className="chat-text"><em>Typing...</em></div>
              </div>
            )}
          </div>

          <div className="chat-input">
            <input
              type="text"
              placeholder="Ask something..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            />
            <button onClick={sendMessage}>Send</button>
          </div>
        </div>
      </div>
    </>
  );
}


export default App;