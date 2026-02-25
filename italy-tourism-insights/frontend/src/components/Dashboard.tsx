import React from 'react'

export const Dashboard: React.FC = () => {
  return (
    <div className="space-y-8">
      <div className="bg-gradient-to-r from-blue-600 to-red-600 rounded-lg shadow-lg p-8 text-white">
        <h1 className="text-4xl font-bold mb-2">Italian Tourism Intelligence Dashboard</h1>
        <p className="text-lg opacity-90">Real-time analytics and ML forecasting for cultural tourism across Italy</p>
      </div>

      <div className="grid grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Total Visitors</p>
              <p className="text-3xl font-bold">45.2M</p>
            </div>
            <span className="text-4xl">👥</span>
          </div>
          <p className="text-green-600 text-sm mt-2">+12.5% YoY</p>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Regions Tracked</p>
              <p className="text-3xl font-bold">20</p>
            </div>
            <span className="text-4xl">🗺️</span>
          </div>
          <p className="text-gray-600 text-sm mt-2">All Italian regions</p>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Cultural Sites</p>
              <p className="text-3xl font-bold">234</p>
            </div>
            <span className="text-4xl">🏛️</span>
          </div>
          <p className="text-gray-600 text-sm mt-2">Heritage locations</p>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Satisfaction</p>
              <p className="text-3xl font-bold">4.7</p>
            </div>
            <span className="text-4xl">⭐</span>
          </div>
          <p className="text-gray-600 text-sm mt-2">Average rating</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Quick Links</h2>
          <ul className="space-y-3">
            <li><a href="#" className="text-blue-600 hover:text-blue-800 font-medium flex items-center"><span className="mr-2">📊</span>View Analytics Dashboard</a></li>
            <li><a href="#" className="text-blue-600 hover:text-blue-800 font-medium flex items-center"><span className="mr-2">🔮</span>30-Day Forecasts</a></li>
            <li><a href="#" className="text-blue-600 hover:text-blue-800 font-medium flex items-center"><span className="mr-2">🏛️</span>Explore Cultural Sites</a></li>
            <li><a href="#" className="text-blue-600 hover:text-blue-800 font-medium flex items-center"><span className="mr-2">📖</span>API Documentation</a></li>
            <li><a href="#" className="text-blue-600 hover:text-blue-800 font-medium flex items-center"><span className="mr-2">💬</span>Chat with Tourism Guide</a></li>
          </ul>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Recent Updates</h2>
          <ul className="space-y-3 text-sm">
            <li className="flex items-start space-x-3">
              <span className="text-green-600 mt-1">✓</span>
              <span>Daily forecasting models updated</span>
            </li>
            <li className="flex items-start space-x-3">
              <span className="text-green-600 mt-1">✓</span>
              <span>New anomaly detection system active</span>
            </li>
            <li className="flex items-start space-x-3">
              <span className="text-green-600 mt-1">✓</span>
              <span>Regional analytics fully synchronized</span>
            </li>
            <li className="flex items-start space-x-3">
              <span className="text-green-600 mt-1">✓</span>
              <span>🆕 AI Tourism Chatbot launched!</span>
            </li>
            <li className="flex items-start space-x-3">
              <span className="text-green-600 mt-1">✓</span>
              <span>ML model accuracy: 92%</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}
