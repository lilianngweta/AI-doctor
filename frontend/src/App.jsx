import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = 'http://localhost:8001'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [systemStatus, setSystemStatus] = useState(null)
  const [initializing, setInitializing] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    checkSystemStatus()
  }, [])

  const checkSystemStatus = async () => {
    try {
      const response = await axios.get(`${API_URL}/status`)
      setSystemStatus(response.data)
      
      if (!response.data.index_loaded) {
        const welcomeMessage = {
          type: 'system',
          content: 'Welcome to AI Doctor! The system needs to be initialized. Click "Initialize System" to load the medical knowledge base.',
          timestamp: new Date()
        }
        setMessages([welcomeMessage])
      } else {
        const welcomeMessage = {
          type: 'assistant',
          content: 'Hello! I\'m your AI wellness advisor. I can help answer questions about various health conditions and symptoms. How can I assist you today?',
          timestamp: new Date()
        }
        setMessages([welcomeMessage])
      }
    } catch (error) {
      console.error('Error checking system status:', error)
      const errorMessage = {
        type: 'error',
        content: 'Could not connect to the backend server. Please make sure it\'s running on port 8000.',
        timestamp: new Date()
      }
      setMessages([errorMessage])
    }
  }

  const initializeSystem = async () => {
    setInitializing(true)
    const systemMessage = {
      type: 'system',
      content: 'Initializing system with medical knowledge from Wikidoc... This may take a few minutes.',
      timestamp: new Date()
    }
    setMessages(prev => [...prev, systemMessage])

    try {
      await axios.post(`${API_URL}/initialize?max_samples=1000`)
      
      const successMessage = {
        type: 'system',
        content: 'System initialized successfully! You can now ask me about health and wellness topics.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, successMessage])
      
      await checkSystemStatus()
    } catch (error) {
      console.error('Error initializing system:', error)
      const errorMessage = {
        type: 'error',
        content: 'Failed to initialize system. Please check the backend logs.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setInitializing(false)
    }
  }

  const sendMessage = async (e) => {
    e.preventDefault()
    
    if (!input.trim()) return
    
    if (!systemStatus?.index_loaded) {
      const warningMessage = {
        type: 'error',
        content: 'Please initialize the system first.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, warningMessage])
      return
    }

    const userMessage = {
      type: 'user',
      content: input,
      timestamp: new Date()
    }
    
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post(`${API_URL}/query`, {
        question: input
      })

      const assistantMessage = {
        type: 'assistant',
        content: response.data.answer,
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage = {
        type: 'error',
        content: error.response?.data?.detail || 'An error occurred while processing your question.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="chat-container">
        <div className="chat-header">
          <div className="header-content">
            <h1>🏥 AI Doctor</h1>
            <p>Your AI-Powered Wellness Advisor</p>
          </div>
          <div className="header-actions">
            {systemStatus && !systemStatus.index_loaded && (
              <button 
                className="init-button"
                onClick={initializeSystem}
                disabled={initializing}
              >
                {initializing ? 'Initializing...' : 'Initialize System'}
              </button>
            )}
            <div className={`status-indicator ${systemStatus?.index_loaded ? 'online' : 'offline'}`}>
              {systemStatus?.index_loaded ? 'Ready' : 'Not Ready'}
            </div>
          </div>
        </div>

        <div className="messages-container">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.type}`}>
              <div className="message-content">
                {message.type === 'user' && <div className="message-label">You</div>}
                {message.type === 'assistant' && <div className="message-label">AI Doctor</div>}
                {message.type === 'system' && <div className="message-label">System</div>}
                {message.type === 'error' && <div className="message-label">Error</div>}
                <div className="message-text">{message.content}</div>
              </div>
            </div>
          ))}
          {loading && (
            <div className="message assistant">
              <div className="message-content">
                <div className="message-label">AI Doctor</div>
                <div className="message-text typing">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form className="input-container" onSubmit={sendMessage}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about symptoms, conditions, or wellness advice..."
            disabled={loading || !systemStatus?.index_loaded}
          />
          <button 
            type="submit" 
            disabled={loading || !input.trim() || !systemStatus?.index_loaded}
          >
            Send
          </button>
        </form>

        <div className="disclaimer">
          <p>⚠️ <strong>Disclaimer:</strong> This AI provides general wellness information only. Always consult a healthcare professional for medical advice.</p>
        </div>
      </div>
    </div>
  )
}

export default App
