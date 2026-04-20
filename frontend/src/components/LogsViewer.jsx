import React, { useState } from 'react'
import { ChevronLeft, ChevronRight, AlertCircle } from 'lucide-react'

const LogsViewer = ({ logs = [], loading = false }) => {
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 20

  // Generate mock data if not provided
  const mockLogs = logs.length > 0 ? logs : generateMockLogs()

  function generateMockLogs() {
    return Array.from({ length: 100 }, (_, i) => ({
      id: i,
      timestamp: new Date(Date.now() - i * 60000).toLocaleString(),
      event_id: Math.floor(Math.random() * 100),
      template: `Event template ${Math.floor(Math.random() * 50)}`,
      anomaly_flag: Math.random() > 0.95 ? 1 : 0,
      anomaly_score: Math.random(),
    }))
  }

  const totalPages = Math.ceil(mockLogs.length / itemsPerPage)
  const startIdx = (currentPage - 1) * itemsPerPage
  const endIdx = startIdx + itemsPerPage
  const currentLogs = mockLogs.slice(startIdx, endIdx)

  return (
    <div className="card">
      <h3 className="text-lg font-bold mb-6">Logs Viewer</h3>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-dark-border">
              <th className="px-4 py-3 text-left font-semibold text-gray-400">Timestamp</th>
              <th className="px-4 py-3 text-left font-semibold text-gray-400">Event ID</th>
              <th className="px-4 py-3 text-left font-semibold text-gray-400">Template</th>
              <th className="px-4 py-3 text-center font-semibold text-gray-400">Score</th>
              <th className="px-4 py-3 text-center font-semibold text-gray-400">Status</th>
            </tr>
          </thead>
          <tbody>
            {currentLogs.map((log) => (
              <tr
                key={log.id}
                className={`border-b border-dark-border hover:bg-dark-surface transition-colors ${
                  log.anomaly_flag ? 'bg-red-500/5' : ''
                }`}
              >
                <td className="px-4 py-3 text-gray-300 font-mono text-xs">{log.timestamp}</td>
                <td className="px-4 py-3">
                  <span className="bg-dark-border px-2 py-1 rounded text-neon-green font-semibold">
                    E{log.event_id.toString().padStart(3, '0')}
                  </span>
                </td>
                <td className="px-4 py-3 text-gray-400 truncate max-w-xs">{log.template}</td>
                <td className="px-4 py-3 text-center">
                  <span
                    className={`font-semibold ${
                      log.anomaly_score > 0.7 ? 'text-red-500' : 'text-neon-green'
                    }`}
                  >
                    {(log.anomaly_score * 100).toFixed(1)}%
                  </span>
                </td>
                <td className="px-4 py-3 text-center">
                  {log.anomaly_flag ? (
                    <span className="flex items-center justify-center gap-1">
                      <AlertCircle size={16} className="text-red-500" />
                      <span className="text-red-500 font-semibold">Anomaly</span>
                    </span>
                  ) : (
                    <span className="text-neon-green font-semibold">Normal</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="flex items-center justify-between mt-6 pt-4 border-t border-dark-border">
        <p className="text-sm text-gray-400">
          Page {currentPage} of {totalPages} ({mockLogs.length} total logs)
        </p>

        <div className="flex gap-2">
          <button
            onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
            disabled={currentPage === 1}
            className="btn btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronLeft size={18} />
          </button>

          <div className="flex items-center gap-2 px-4">
            {Array.from({ length: Math.min(5, totalPages) }).map((_, i) => {
              const pageNum = i + 1
              return (
                <button
                  key={pageNum}
                  onClick={() => setCurrentPage(pageNum)}
                  className={`w-8 h-8 rounded flex items-center justify-center font-semibold transition-all ${
                    currentPage === pageNum
                      ? 'bg-neon-green text-black'
                      : 'bg-dark-border text-gray-300 hover:bg-dark-border/50'
                  }`}
                >
                  {pageNum}
                </button>
              )
            })}
          </div>

          <button
            onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
            disabled={currentPage === totalPages}
            className="btn btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronRight size={18} />
          </button>
        </div>
      </div>
    </div>
  )
}

export default LogsViewer
