import React, { useState, useEffect } from 'react'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Analysis from './pages/Analysis'
import Logs from './pages/Logs'
import Settings from './pages/Settings'
import apiService from './services/apiService'

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [isHealthy, setIsHealthy] = useState(false)

  useEffect(() => {
    // Check API health on mount
    checkApiHealth()
    const healthInterval = setInterval(checkApiHealth, 30000) // Check every 30s
    return () => clearInterval(healthInterval)
  }, [])

  const checkApiHealth = async () => {
    try {
      await apiService.health()
      setIsHealthy(true)
    } catch (error) {
      console.warn('Backend API is not available:', error)
      setIsHealthy(false)
    }
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />
      case 'datasets':
        return <Dashboard />
      case 'analysis':
        return <Analysis />
      case 'logs':
        return <Logs />
      case 'settings':
        return <Settings />
      default:
        return <Dashboard />
    }
  }

  return (
    <div className="flex h-screen bg-dark-bg text-white overflow-hidden">
      {/* Sidebar */}
      <Sidebar active={currentPage} onNavigate={setCurrentPage} />

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <div className="p-8">
          {/* API Health Indicator */}
          {!isHealthy && (
            <div className="mb-6 p-4 bg-red-500/10 border border-red-500 rounded-lg flex items-center gap-3 text-red-400">
              <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
              <span className="text-sm font-medium">Backend API is not available. Features may be limited.</span>
            </div>
          )}

          {/* Page Content */}
          {renderPage()}
        </div>
      </main>
    </div>
  )
}

export default App
