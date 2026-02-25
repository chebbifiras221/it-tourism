import React, { useState, useEffect } from 'react'
import { ChatPage } from './pages/ChatPage'
import './index.css'

function App() {
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate initial load
    setTimeout(() => setLoading(false), 300)
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-r from-blue-600 to-red-600">
        <div className="text-white text-center">
          <h1 className="text-5xl font-bold mb-4">🇮🇹</h1>
          <p className="text-2xl font-semibold mb-2">Italian Tourism Assistant</p>
          <p className="text-xl mb-8 opacity-90">Loading...</p>
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-white mx-auto"></div>
        </div>
      </div>
    )
  }

  return <ChatPage />
}

export default App
