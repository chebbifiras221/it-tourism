import React, { useState, useRef, useEffect } from 'react'
import axios from 'axios'

interface Message {
  id: string
  type: 'user' | 'assistant'
  content: string
  recommendations?: Recommendation[]
  timestamp: string
  messageType?: 'greeting' | 'farewell' | 'rejection' | 'recommendation'
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

interface AnalyticsData {
  totalVisitors: string
  regions: number
  culturalSites: number
  satisfaction: number
  yoYChange: number
}

export const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [language, setLanguage] = useState<'en' | 'it'>('en')
  const [showAnalytics, setShowAnalytics] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Analytics data
  const analyticsData: AnalyticsData = {
    totalVisitors: '45.2M',
    regions: 20,
    culturalSites: 234,
    satisfaction: 4.7,
    yoYChange: 12.5
  }

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Send initial greeting on mount
  useEffect(() => {
    sendInitialGreeting()
  }, [language])

  const sendInitialGreeting = async () => {
    const greetingMessage = language === 'en' 
      ? "Hello! I'm ready to help you explore Italy!"
      : "Ciao! Sono pronto ad aiutarti a esplorare l'Italia!"
    
    try {
      const response = await axios.post('http://localhost:8000/api/chat', {
        message: greetingMessage
      })

      const assistantMessage: Message = {
        id: Date.now().toString(),
        type: 'assistant',
        content: response.data.response,
        recommendations: response.data.recommendations,
        timestamp: new Date().toISOString(),
        messageType: response.data.message_type
      }

      setMessages([assistantMessage])
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const sendMessage = async () => {
    if (!input.trim()) return

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
        timestamp: new Date().toISOString(),
        messageType: response.data.message_type
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: language === 'en'
          ? 'Sorry, I encountered an error. Please try again.'
          : 'Mi scusi, ho riscontrato un errore. Riprova più tardi.',
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const clearHistory = () => {
    setMessages([])
    sendInitialGreeting()
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-gray-900 text-white p-4 overflow-y-auto flex flex-col">
        <div className="mb-6">
          <button
            onClick={clearHistory}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition flex items-center justify-center space-x-2"
          >
            <span>➕</span>
            <span>{language === 'en' ? 'New Chat' : 'Nuova Chat'}</span>
          </button>
        </div>

        <div className="flex-1 space-y-3">
          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wide px-2">
            {language === 'en' ? 'Recent' : 'Recenti'}
          </h3>
          {messages.filter(m => m.type === 'user').slice(-5).map((msg, idx) => (
            <div
              key={idx}
              className="p-3 rounded-lg bg-gray-800 hover:bg-gray-700 cursor-pointer transition text-sm text-gray-200 truncate"
            >
              {msg.content.substring(0, 30)}...
            </div>
          ))}
        </div>

        {/* Sidebar Footer */}
        <div className="border-t border-gray-700 pt-4 space-y-3">
          <div>
            <label className="text-xs font-semibold text-gray-400 uppercase">{language === 'en' ? 'Language' : 'Lingua'}</label>
            <div className="flex space-x-2 mt-2">
              <button
                onClick={() => setLanguage('en')}
                className={`flex-1 py-2 px-3 rounded text-sm font-medium transition ${
                  language === 'en'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                }`}
              >
                🇺🇸 English
              </button>
              <button
                onClick={() => setLanguage('it')}
                className={`flex-1 py-2 px-3 rounded text-sm font-medium transition ${
                  language === 'it'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                }`}
              >
                🇮🇹 Italiano
              </button>
            </div>
          </div>

          <button
            onClick={() => setShowAnalytics(!showAnalytics)}
            className="w-full text-left text-sm text-gray-400 hover:text-gray-200 transition py-2"
          >
            {showAnalytics ? '👁️ Hide Analytics' : '👁️ Show Analytics'}
          </button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Top Bar */}
        <div className="bg-white border-b border-gray-200 px-8 py-4">
          <h1 className="text-2xl font-bold text-gray-900">🇮🇹 Italian Tourism Assistant</h1>
          <p className="text-gray-600 text-sm mt-1">
            {language === 'en'
              ? 'Your personal guide to Italy'
              : 'La tua guida personale dell\'Italia'}
          </p>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-8 space-y-6 bg-gradient-to-b from-gray-50 to-white">
          {messages.length === 0 ? (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <div className="text-6xl mb-4">🇮🇹</div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  {language === 'en' ? 'Welcome to Italy' : 'Benvenuto in Italia'}
                </h2>
                <p className="text-gray-600 max-w-md">
                  {language === 'en'
                    ? 'Ask me about hotels, restaurants, cultural sites, and things to do across Italy!'
                    : 'Chiedimi di hotel, ristoranti, siti culturali e cose da fare in tutta l\'Italia!'}
                </p>
              </div>
            </div>
          ) : (
            messages.map((message) => (
              <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`max-w-2xl ${
                    message.type === 'user'
                      ? 'bg-blue-600 text-white rounded-3xl rounded-tr-none'
                      : 'bg-white text-gray-900 rounded-3xl rounded-tl-none border border-gray-200 shadow-md'
                  } px-6 py-4`}
                >
                  <p className="text-base leading-relaxed whitespace-pre-wrap">{message.content}</p>

                  {/* Recommendations */}
                  {message.recommendations && message.recommendations.length > 0 && (
                    <div className="mt-6 space-y-3">
                      {message.recommendations.map((rec, idx) => (
                        <RecommendationCard key={idx} recommendation={rec} />
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))
          )}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-white text-gray-900 rounded-3xl rounded-tl-none border border-gray-200 px-6 py-4 shadow-md">
                <div className="flex space-x-2">
                  <div className="w-3 h-3 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-3 h-3 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                  <div className="w-3 h-3 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="bg-white border-t border-gray-200 p-6">
          <div className="max-w-4xl mx-auto">
            <div className="flex space-x-4">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
                placeholder={language === 'en'
                  ? "Ask about hotels, food, sites..."
                  : "Chiedi di hotel, cibo, siti..."}
                className="flex-1 border-2 border-gray-200 rounded-full px-6 py-3 text-lg focus:outline-none focus:border-blue-600 transition"
                disabled={loading}
              />
              <button
                onClick={sendMessage}
                disabled={loading || !input.trim()}
                className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-full px-8 py-3 font-semibold transition flex items-center space-x-2"
              >
                <span>{loading ? '...' : '→'}</span>
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-3 text-center">
              {language === 'en'
                ? 'Try: "Hotels in Rome" or "Best restaurants in Venice"'
                : 'Prova: "Hotel a Roma" oppure "Migliori ristoranti a Venezia"'}
            </p>
          </div>
        </div>
      </div>

      {/* Analytics Panel */}
      {showAnalytics && (
        <div className="w-80 bg-white border-l border-gray-200 p-6 overflow-y-auto">
          <h2 className="text-xl font-bold text-gray-900 mb-6">
            {language === 'en' ? '📊 Analytics' : '📊 Analitiche'}
          </h2>

          <div className="space-y-6">
            {/* Total Visitors */}
            <AnalyticsCard
              label={language === 'en' ? 'Total Visitors' : 'Visitatori Totali'}
              value={analyticsData.totalVisitors}
              icon="👥"
              description={language === 'en'
                ? 'Tourism across all Italian regions'
                : 'Turismo in tutte le regioni italiane'}
            />

            {/* Regions */}
            <AnalyticsCard
              label={language === 'en' ? 'Regions' : 'Regioni'}
              value={analyticsData.regions.toString()}
              icon="🗺️"
              description={language === 'en'
                ? 'All Italian regions tracked'
                : 'Tutte le regioni italiane monitorat'}
            />

            {/* Cultural Sites */}
            <AnalyticsCard
              label={language === 'en' ? 'Cultural Sites' : 'Siti Culturali'}
              value={analyticsData.culturalSites.toString()}
              icon="🏛️"
              description={language === 'en'
                ? 'Museums, monuments, heritage'
                : 'Musei, monumenti, patrimonio'}
            />

            {/* Satisfaction */}
            <AnalyticsCard
              label={language === 'en' ? 'Avg. Rating' : 'Valutazione Media'}
              value={analyticsData.satisfaction.toString()}
              icon="⭐"
              description={language === 'en'
                ? 'Visitor satisfaction score'
                : 'Punteggio di soddisfazione'}
            />

            {/* YoY Change */}
            <AnalyticsCard
              label={language === 'en' ? 'Year-over-Year' : 'Anno su Anno'}
              value={`+${analyticsData.yoYChange}%`}
              icon="📈"
              description={language === 'en'
                ? 'Growth in tourism'
                : 'Crescita del turismo'}
            />
          </div>
        </div>
      )}
    </div>
  )
}

interface RecommendationCardProps {
  recommendation: Recommendation
}

const RecommendationCard: React.FC<RecommendationCardProps> = ({ recommendation }) => {
  return (
    <a
      href={recommendation.link || '#'}
      target="_blank"
      rel="noopener noreferrer"
      className="block p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-200 hover:shadow-lg transition"
    >
      <div className="flex items-start space-x-4">
        <span className="text-3xl">{recommendation.icon}</span>
        <div className="flex-1">
          <h4 className="font-bold text-blue-900 text-lg">{recommendation.name}</h4>
          <p className="text-sm text-blue-700 font-medium">{recommendation.details}</p>
          <p className="text-sm text-gray-700 mt-2">{recommendation.description}</p>
          {recommendation.address && (
            <p className="text-xs text-gray-600 mt-2 flex items-center space-x-1">
              <span>📍</span>
              <span>{recommendation.address}</span>
            </p>
          )}
          {recommendation.hours && (
            <p className="text-xs text-gray-600 mt-1 flex items-center space-x-1">
              <span>🕐</span>
              <span>{recommendation.hours}</span>
            </p>
          )}
          {recommendation.link && (
            <p className="text-xs text-blue-600 font-semibold mt-3 flex items-center space-x-1">
              <span>🔗</span>
              <span>Visit Website</span>
            </p>
          )}
        </div>
      </div>
    </a>
  )
}

interface AnalyticsCardProps {
  label: string
  value: string
  icon: string
  description: string
}

const AnalyticsCard: React.FC<AnalyticsCardProps> = ({ label, value, icon, description }) => {
  return (
    <div className="p-4 bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg border border-gray-200">
      <div className="flex items-center justify-between mb-2">
        <span className="text-2xl">{icon}</span>
        <p className="text-sm text-gray-600">{label}</p>
      </div>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
      <p className="text-xs text-gray-600 mt-2">{description}</p>
    </div>
  )
}
