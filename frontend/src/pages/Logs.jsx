import React, { useState } from 'react'
import { Search, Download, Filter } from 'lucide-react'
import LogsViewer from '../components/LogsViewer'

const Logs = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [filterAnomalies, setFilterAnomalies] = useState('all')
  const [dateRange, setDateRange] = useState({ start: '', end: '' })

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-4xl font-bold">Logs Explorer</h1>
        <p className="text-gray-400">Search and filter processed logs</p>
      </div>

      {/* Filters */}
      <div className="card space-y-6">
        <div className="flex items-center gap-2 mb-4">
          <Filter size={20} className="text-neon-green" />
          <h3 className="font-bold">Filters</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Search */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Search Logs</label>
            <div className="relative">
              <Search size={18} className="absolute left-3 top-3 text-gray-500" />
              <input
                type="text"
                placeholder="Event ID, template, message..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="input pl-10 w-full"
              />
            </div>
          </div>

          {/* Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Status</label>
            <select
              value={filterAnomalies}
              onChange={(e) => setFilterAnomalies(e.target.value)}
              className="input w-full"
            >
              <option value="all">All Logs</option>
              <option value="anomalies">Anomalies Only</option>
              <option value="normal">Normal Logs</option>
            </select>
          </div>

          {/* Actions */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Actions</label>
            <button className="btn btn-secondary w-full flex items-center justify-center gap-2">
              <Download size={18} />
              Export Report
            </button>
          </div>
        </div>

        {/* Date Range */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">From</label>
            <input
              type="datetime-local"
              value={dateRange.start}
              onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
              className="input w-full"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">To</label>
            <input
              type="datetime-local"
              value={dateRange.end}
              onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
              className="input w-full"
            />
          </div>
        </div>
      </div>

      {/* Results Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card">
          <p className="text-sm text-gray-400 mb-1">Total Results</p>
          <p className="text-3xl font-bold text-neon-green">1,234</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-400 mb-1">Anomalies Found</p>
          <p className="text-3xl font-bold text-red-500">42</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-400 mb-1">Anomaly Rate</p>
          <p className="text-3xl font-bold text-yellow-500">3.4%</p>
        </div>
      </div>

      {/* Logs Table */}
      <LogsViewer />
    </div>
  )
}

export default Logs
