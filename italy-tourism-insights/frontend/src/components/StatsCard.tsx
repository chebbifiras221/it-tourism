import React from 'react'

interface StatCardProps {
  label: string
  value: string | number
  subtext?: string
  icon?: string
  trend?: number
  color?: 'blue' | 'red' | 'green' | 'yellow'
}

const colorClasses = {
  blue: 'bg-blue-50 border-blue-200 text-blue-900',
  red: 'bg-red-50 border-red-200 text-red-900',
  green: 'bg-green-50 border-green-200 text-green-900',
  yellow: 'bg-yellow-50 border-yellow-200 text-yellow-900',
}

export const StatsCard: React.FC<StatCardProps> = ({
  label,
  value,
  subtext,
  icon = '📊',
  trend,
  color = 'blue'
}) => {
  return (
    <div className={`card border-l-4 ${colorClasses[color]}`}>
      <div className="flex items-center justify-between mb-4">
        <div className="text-4xl">{icon}</div>
        {trend !== undefined && (
          <div className={`text-sm font-semibold ${trend > 0 ? 'text-green-600' : 'text-red-600'}`}>
            {trend > 0 ? '+' : ''}{trend}%
          </div>
        )}
      </div>
      <h3 className="text-gray-600 text-sm font-medium mb-1">{label}</h3>
      <p className="text-2xl font-bold mb-2">{value}</p>
      {subtext && <p className="text-xs text-gray-500">{subtext}</p>}
    </div>
  )
}
