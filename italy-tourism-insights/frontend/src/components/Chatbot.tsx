import React, { useState, useRef, useEffect } from 'react'
import axios from 'axios'

interface Message {
  id: string
  type: 'user' | 'assistant'
  content: string
  recommendations?: Recommendation[]
  timestamp: string
}

interface Recommendation {
  type: string
  icon: string
  name: string
  details: string
  description: string
  link?: string
  address?: string
  hours?: string
}

interface ChatbotProps {
  isOpen?: boolean
}

// Helper function to render markdown links as HTML
const renderMarkdownLinks = (text: string) => {
  const parts: (string | React.ReactNode)[] = []
  const regex = /\[([^\]]+)\]\(([^)]+)\)/g
  let lastIndex = 0
  let match

  while ((match = regex.exec(text)) !== null) {
    // Add text before the link
    if (match.index > lastIndex) {
      parts.push(text.substring(lastIndex, match.index))
    }
    
    // Add the link
    const linkText = match[1]
    const linkUrl = match[2]
    
    parts.push(
      <a
        key={`link-${match.index}`}
        href={linkUrl}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-600 hover:text-blue-800 hover:underline font-medium break-words"
      >
        {linkText}
      </a>
    )
    
    lastIndex = regex.lastIndex
  }
  
  // Add remaining text
  if (lastIndex < text.length) {
    parts.push(text.substring(lastIndex))
  }
  
  return parts.length > 0 ? parts : text
}

export const Chatbot: React.FC<ChatbotProps> = ({ isOpen = false }) => {
  const [language, setLanguage] = useState<'en' | 'it'>('en')
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'assistant',
      content: "👋 Welcome! I'm your AI Tourism Assistant powered by Groq. Ask me about hotels, restaurants, cultural sites, and activities in Italy!\n\n✅ **Unlimited requests** - No rate limits! Enjoy fast, unrestricted conversations.",
      timestamp: new Date().toISOString()
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [open, setOpen] = useState(isOpen)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim()) return

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post('http://localhost:8000/api/chat', {
        message: input,
        language: language
      })

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: response.data.response,
        recommendations: response.data.recommendations,
        timestamp: new Date().toISOString()
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: language === 'it' 
          ? '❌ Mi scusi, ho riscontrato un errore. Prova di nuovo.' 
          : '❌ Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="fixed bottom-6 right-6 bg-gradient-to-r from-blue-600 to-red-600 text-white rounded-full p-4 shadow-lg hover:shadow-xl transition z-40"
        title="Chat with tourism guide"
      >
        <span className="text-2xl">💬</span>
      </button>
    )
  }

  return (
    <div className="fixed bottom-6 right-6 w-96 bg-white rounded-lg shadow-2xl flex flex-col z-50 max-h-96">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-red-600 text-white p-4 rounded-t-lg">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h3 className="font-bold text-lg">🇮🇹 Tourism Assistant</h3>
            <p className="text-xs opacity-90">Your AI guide to Italian travel</p>
          </div>
          <button
            onClick={() => setOpen(false)}
            className="text-2xl hover:opacity-80"
          >
            ✕
          </button>
        </div>
        
        {/* Language Selector */}
        <div className="flex space-x-2 border-t border-blue-400 pt-3">
          <button
            onClick={() => setLanguage('en')}
            className={`flex-1 py-1 px-2 rounded text-sm font-medium transition ${
              language === 'en'
                ? 'bg-white text-blue-600'
                : 'bg-blue-500 text-white hover:bg-blue-400'
            }`}
          >
            English
          </button>
          <button
            onClick={() => setLanguage('it')}
            className={`flex-1 py-1 px-2 rounded text-sm font-medium transition ${
              language === 'it'
                ? 'bg-white text-red-600'
                : 'bg-red-500 text-white hover:bg-red-400'
            }`}
          >
            Italiano
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.map(message => (
          <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-sm rounded-lg p-3 ${
                message.type === 'user'
                  ? 'bg-blue-600 text-white rounded-br-none'
                  : 'bg-white text-gray-900 border border-gray-200 rounded-bl-none max-w-md'
              }`}
            >
              <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">
                {renderMarkdownLinks(message.content)}
              </p>

              {/* Recommendations */}
              {message.recommendations && message.recommendations.length > 0 && (
                <div className="mt-3 space-y-2">
                  {message.recommendations.map((rec, idx) => (
                    <div key={idx} className={`p-2 rounded text-xs border ${
                      message.type === 'user' 
                        ? 'bg-blue-500 border-blue-400' 
                        : 'bg-blue-50 border-blue-200'
                    }`}>
                      <p className={`font-semibold ${message.type === 'user' ? 'text-white' : 'text-blue-900'}`}>
                        {rec.icon} {rec.name}
                      </p>
                      <p className={message.type === 'user' ? 'text-blue-100' : 'text-gray-700'}>
                        {rec.details}
                      </p>
                      <p className={`mt-1 ${message.type === 'user' ? 'text-blue-100' : 'text-gray-600'}`}>
                        {rec.description}
                      </p>
                      {rec.address && (
                        <p className={`mt-1 text-xs ${message.type === 'user' ? 'text-blue-100' : 'text-gray-600'}`}>
                          📍 {rec.address}
                        </p>
                      )}
                      {rec.hours && (
                        <p className={`mt-1 text-xs ${message.type === 'user' ? 'text-blue-100' : 'text-gray-600'}`}>
                          🕐 {rec.hours}
                        </p>
                      )}
                      {rec.link && (
                        <a
                          href={rec.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className={`block mt-2 text-center py-1 rounded transition no-underline ${
                            message.type === 'user'
                              ? 'bg-white text-blue-600 hover:bg-gray-100'
                              : 'bg-blue-600 text-white hover:bg-blue-700'
                          }`}
                        >
                          {language === 'en' ? 'Visit Website' : 'Visita Sito'}
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 rounded-lg p-3 rounded-bl-none">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t p-3 bg-white rounded-b-lg">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyPress={e => e.key === 'Enter' && sendMessage()}
            placeholder="Ask about hotels, food, sites..."
            className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600"
            disabled={loading}
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 text-sm font-semibold disabled:opacity-50 transition"
          >
            Send
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          {language === 'en'
            ? '💡 Try: "Hotels in Rome" | ✅ Groq: 30k requests/month'
            : '💡 Prova: "Alberghi a Roma" | ✅ Groq: 30k richieste/mese'
          }
        </p>
      </div>
    </div>
  )
}
