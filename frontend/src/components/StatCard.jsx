import React from 'react'

const StatCard = ({ icon: Icon, title, value, unit = '', change = null, color = 'green' }) => {
  const colorClasses = {
    green: 'text-neon-green',
    blue: 'text-neon-blue',
    purple: 'text-neon-purple',
    red: 'text-red-500',
  }

  const bgGradients = {
    green: 'from-neon-green/10 to-transparent',
    blue: 'from-neon-blue/10 to-transparent',
    purple: 'from-neon-purple/10 to-transparent',
    red: 'from-red-500/10 to-transparent',
  }

  return (
    <div className={`card bg-gradient-to-br ${bgGradients[color]} border-l-4`}>
      <div className="flex items-start justify-between mb-4">
        <div className={`p-3 rounded-lg bg-dark-border ${colorClasses[color]}`}>
          <Icon size={24} />
        </div>
        {change && (
          <span className={`text-sm font-semibold ${change > 0 ? 'text-neon-green' : 'text-red-500'}`}>
            {change > 0 ? '+' : ''}{change}%
          </span>
        )}
      </div>

      <h3 className="text-gray-400 text-sm font-medium mb-1">{title}</h3>
      <p className={`text-3xl font-bold ${colorClasses[color]}`}>
        {value}
        {unit && <span className="text-lg ml-1">{unit}</span>}
      </p>
    </div>
  )
}

export default StatCard
