import React from 'react'
import { Activity, BarChart3, Database, Settings, TrendingUp } from 'lucide-react'

const Sidebar = ({ active, onNavigate }) => {
  const items = [
    { id: 'dashboard', label: 'Dashboard', icon: Activity },
    { id: 'datasets', label: 'Datasets', icon: Database },
    { id: 'analysis', label: 'Analysis', icon: BarChart3 },
    { id: 'logs', label: 'Logs', icon: TrendingUp },
    { id: 'settings', label: 'Settings', icon: Settings },
  ]

  return (
    <aside className="w-64 bg-dark-surface border-r border-dark-border h-screen sticky top-0 flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-dark-border">
        <h1 className="text-2xl font-bold bg-gradient-to-r from-neon-green to-neon-blue bg-clip-text text-transparent">
          LOGLY
        </h1>
        <p className="text-xs text-gray-400 mt-1">Log Analytics Platform</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {items.map((item) => {
          const Icon = item.icon
          const isActive = active === item.id

          return (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                isActive
                  ? 'bg-neon-green text-black font-semibold'
                  : 'text-gray-300 hover:bg-dark-border hover:text-neon-green'
              }`}
            >
              <Icon size={20} />
              <span>{item.label}</span>
            </button>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-dark-border">
        <p className="text-xs text-gray-500 text-center">v1.0.0</p>
      </div>
    </aside>
  )
}

export default Sidebar
