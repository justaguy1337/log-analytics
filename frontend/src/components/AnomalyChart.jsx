import React from 'react'
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const AnomalyChart = ({ data = [], title = 'Anomalies Over Time', type = 'line' }) => {
  // Generate mock data if not provided
  const chartData = data.length > 0 ? data : generateMockData()

  function generateMockData() {
    return Array.from({ length: 24 }, (_, i) => ({
      time: `${i}:00`,
      anomalies: Math.floor(Math.random() * 20),
      normal: Math.floor(Math.random() * 100),
    }))
  }

  const chartProps = {
    data: chartData,
    margin: { top: 10, right: 30, left: 0, bottom: 0 },
  }

  return (
    <div className="card">
      <h3 className="text-lg font-bold mb-6 flex items-center gap-2">
        <div className="w-1 h-6 bg-neon-green rounded"></div>
        {title}
      </h3>

      <ResponsiveContainer width="100%" height={300}>
        {type === 'area' ? (
          <AreaChart {...chartProps}>
            <defs>
              <linearGradient id="colorAnomalies" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#00ff88" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#00ff88" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#2d3748" />
            <XAxis dataKey="time" stroke="#718096" style={{ fontSize: '12px' }} />
            <YAxis stroke="#718096" style={{ fontSize: '12px' }} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1a1f3a',
                border: '1px solid #2d3748',
                borderRadius: '8px',
              }}
              labelStyle={{ color: '#00ff88' }}
            />
            <Area type="monotone" dataKey="anomalies" stroke="#00ff88" fillOpacity={1} fill="url(#colorAnomalies)" />
            <Legend />
          </AreaChart>
        ) : (
          <LineChart {...chartProps}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2d3748" />
            <XAxis dataKey="time" stroke="#718096" style={{ fontSize: '12px' }} />
            <YAxis stroke="#718096" style={{ fontSize: '12px' }} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1a1f3a',
                border: '1px solid #2d3748',
                borderRadius: '8px',
              }}
              labelStyle={{ color: '#00ff88' }}
            />
            <Legend />
            <Line type="monotone" dataKey="anomalies" stroke="#00ff88" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="normal" stroke="#00d4ff" strokeWidth={2} dot={false} />
          </LineChart>
        )}
      </ResponsiveContainer>
    </div>
  )
}

export default AnomalyChart
