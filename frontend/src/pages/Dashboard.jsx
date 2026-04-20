import React, { useState, useEffect } from 'react'
import { AlertCircle, CheckCircle, TrendingUp, Activity, Zap } from 'lucide-react'
import StatCard from '../components/StatCard'
import AnomalyChart from '../components/AnomalyChart'
import LiveLogStream from '../components/LiveLogStream'
import DatasetSelector from '../components/DatasetSelector'
import apiService from '../services/apiService'

const Dashboard = () => {
  const [selectedDataset, setSelectedDataset] = useState('hdfs')
  const [stats, setStats] = useState({
    totalLogs: 0,
    totalAnomalies: 0,
    anomalyRate: 0,
    processingTime: 0,
  })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const generateStats = () => {
      setStats({
        totalLogs: Math.floor(Math.random() * 1000000) + 10000,
        totalAnomalies: Math.floor(Math.random() * 5000) + 100,
        anomalyRate: (Math.random() * 5 + 0.5).toFixed(2),
        processingTime: Math.floor(Math.random() * 500) + 100,
      })
    }

    generateStats()
    const interval = setInterval(generateStats, 10000)
    return () => clearInterval(interval)
  }, [])

  const handleDatasetSelect = async (dataset) => {
    setSelectedDataset(dataset)
    setLoading(true)
    try {
      await apiService.processLogs(dataset)
    } catch (error) {
      console.error('Error processing logs:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-4xl font-bold">Dashboard</h1>
        <p className="text-gray-400">Monitor your distributed system logs in real-time</p>
      </div>

      {/* Dataset Selector */}
      <DatasetSelector onDatasetSelect={handleDatasetSelect} loading={loading} />

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon={Activity}
          title="Total Logs"
          value={stats.totalLogs.toLocaleString()}
          color="blue"
        />
        <StatCard
          icon={AlertCircle}
          title="Anomalies Detected"
          value={stats.totalAnomalies.toLocaleString()}
          color="red"
          change={12}
        />
        <StatCard
          icon={TrendingUp}
          title="Anomaly Rate"
          value={stats.anomalyRate}
          unit="%"
          color="purple"
        />
        <StatCard
          icon={Zap}
          title="Processing Speed"
          value={stats.processingTime}
          unit="ms"
          color="green"
          change={-5}
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <AnomalyChart type="area" title="Anomalies Detection Timeline" />
        </div>
        <div>
          <div className="card space-y-4">
            <h3 className="text-lg font-bold">System Status</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Backend</span>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-neon-green rounded-full animate-pulse"></div>
                  <span className="text-sm text-neon-green">Healthy</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Models</span>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-neon-green rounded-full animate-pulse"></div>
                  <span className="text-sm text-neon-green">Trained</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Data Pipeline</span>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
                  <span className="text-sm text-yellow-500">Processing</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Alerts</span>
                <span className="text-sm font-bold text-red-500">2 Active</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Live Stream */}
      <LiveLogStream />
    </div>
  )
}

export default Dashboard
