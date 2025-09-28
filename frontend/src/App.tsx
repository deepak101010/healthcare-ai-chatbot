import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  severity?: string;
}

interface ApiResponse {
  advice: string;
  severity: string;
  timestamp: string;
}

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Add welcome message
    const welcomeMessage: Message = {
      id: 'welcome',
      text: 'Welcome to your AI Healthcare Assistant! \ud83c\udfe5\n\nI\'m here to help you understand your symptoms and provide professional medical guidance. Simply describe how you\'re feeling, and I\'ll offer personalized advice and recommendations.\n\n\u2022 24/7 availability\n\u2022 Evidence-based guidance\n\u2022 Instant response\n\nPlease note: This service provides general health information and should not replace consultation with qualified healthcare professionals.',
      isUser: false,
      timestamp: new Date(),
      severity: 'mild'
    };
    setMessages([welcomeMessage]);
  }, []);

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await axios.post<ApiResponse>(`${API_BASE_URL}/diagnose`, {
        symptoms: inputValue
      });

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.data.advice,
        isUser: false,
        timestamp: new Date(),
        severity: response.data.severity
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error. Please make sure the backend server is running and try again.',
        isUser: false,
        timestamp: new Date(),
        severity: 'serious'
      };
      setMessages(prev => [...prev, errorMessage]);
      console.error('API Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="App">
      <div className="chat-container">
        <div className="chat-header">
          <h1>🏥 AI Healthcare Assistant</h1>
          <p>Professional medical guidance at your fingertips • Available 24/7</p>
        </div>
        
        <div className="chat-messages">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.isUser ? 'user-message' : 'bot-message'} ${
                message.severity === 'serious' ? 'serious-message' : ''
              }`}
            >
              <div className="message-content">
                <div className="message-text">{message.text}</div>
                <div className="message-timestamp">
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="message bot-message">
              <div className="message-content">
                <div className="typing-indicator">
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
        
        <div className="chat-input">
          <div className="input-container">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Describe your symptoms in detail... (e.g., 'I have a persistent headache for 2 days')"
              disabled={isLoading}
              rows={1}
            />
            <button 
              onClick={sendMessage}
              disabled={!inputValue.trim() || isLoading}
              className="send-button"
            >
              Send
            </button>
          </div>
        </div>
        
        <div className="disclaimer">
          🛡️ Medical Disclaimer: This AI assistant provides general health information only. For serious symptoms, emergencies, or persistent conditions, please consult qualified healthcare professionals immediately.
        </div>
      </div>
    </div>
  );
}

export default App;
