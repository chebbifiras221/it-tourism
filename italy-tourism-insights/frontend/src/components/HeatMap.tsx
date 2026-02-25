import React from 'react'

interface HeatMapProps {
  title: string
  data: Array<{ region: string; value: number }>
  maxValue?: number
}

export const HeatMap: React.FC<HeatMapProps> = ({ title, data, maxValue }) => {
  const max = maxValue || Math.max(...data.map(d => d.value))
  
  const getColor = (value: number) => {
    const ratio = value / max
    if (ratio > 0.8) return 'bg-red-600'
    if (ratio > 0.6) return 'bg-orange-600'
    if (ratio > 0.4) return 'bg-yellow-600'
    if (ratio > 0.2) return 'bg-blue-600'
    return 'bg-blue-200'
  }

  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-6">{title}</h3>
      <div className="grid grid-cols-5 gap-4">
        {data.map((d) => (
          <div key={d.region} className="flex flex-col items-center">
            <div
              className={`w-full aspect-square rounded-lg ${getColor(d.value)} transition hover:shadow-lg cursor-pointer`}
              title={`${d.region}: ${d.value}`}
            />
            <span className="text-xs text-gray-600 mt-2 text-center font-medium">{d.region}</span>
            <span className="text-xs text-gray-500">{d.value.toLocaleString()}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
