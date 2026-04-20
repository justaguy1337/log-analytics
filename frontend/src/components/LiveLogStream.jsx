import React, { useState, useEffect, useRef } from 'react'
import { Activity, AlertCircle } from 'lucide-react'

const LiveLogStream = ({ maxLogs = 50 }) => {
  const [logs, setLogs] = useState([])
  const [isStreaming, setIsStreaming] = useState(true)
  const logEndRef = useRef(null)
  const containerRef = useRef(null)

  useEffect(() => {
    if (!isStreaming) return

    const interval = setInterval(() => {
      const newLog = {
        id: Date.now(),
        timestamp: new Date().toLocaleTimeString(),
        event_id: Math.floor(Math.random() * 100),
        message: generateRandomMessage(),
        anomaly_score: Math.random(),
        is_anomaly: Math.random() > 0.9,
      }

      setLogs((prev) => [newLog, ...prev.slice(0, maxLogs - 1)])
    }, 500 + Math.random() * 500)

    return () => clearInterval(interval)
  }, [isStreaming, maxLogs])

  // Auto-scroll disabled to allow manual scrolling
  // Uncomment below if you want auto-scroll to bottom
  // useEffect(() => {
  //   logEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  // }, [logs])

  function generateRandomMessage() {
    const messages = [
      'Block received from datanode',
      'Pipeline setup successful',
      'Packet acknowledged',
      'Connection established',
      'Data written to disk',
      'Replica updated',
      'Heartbeat received',
      'Block validation passed',
      'Cache refreshed',
      'Connection timeout',
    ]
    return messages[Math.floor(Math.random() * messages.length)]
  }

  const scrollToBottom = () => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight
    }
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-bold flex items-center gap-2">
          <Activity className="text-neon-green animate-pulse" size={24} />
          Live Log Stream
        </h3>
        <div className="flex gap-2">
          <button
            onClick={scrollToBottom}
            className="btn btn-secondary text-sm"
            title="Scroll to latest logs"
          >
            ↓ Latest
          </button>
          <button
            onClick={() => setIsStreaming(!isStreaming)}
            className={`btn text-sm ${isStreaming ? 'btn-secondary' : 'btn-primary'}`}
          >
            {isStreaming ? 'Pause' : 'Resume'}
          </button>
        </div>
      </div>

      <div ref={containerRef} className="space-y-2 max-h-96 overflow-y-auto bg-dark-bg rounded-lg p-4">
        {logs.length === 0 ? (
          <p className="text-gray-500 text-center py-8">Waiting for logs...</p>
        ) : (
          logs.map((log) => (
            <div
              key={log.id}
              className={`flex items-center gap-4 p-3 rounded-lg border transition-all duration-200 ${
                log.is_anomaly
                  ? 'border-red-500/50 bg-red-500/5'
                  : 'border-dark-border bg-dark-surface hover:border-neon-green/30'
              }`}
            >
              <div className="flex-shrink-0 w-8 h-8 flex items-center justify-center">
                {log.is_anomaly ? (
                  <AlertCircle className="text-red-500" size={18} />
                ) : (
                  <div className="w-2 h-2 bg-neon-green rounded-full"></div>
                )}
              </div>

              <div className="flex-1 min-w-0">
                <p className="text-sm font-mono text-gray-300 truncate">
                  <span className="text-neon-green">[E{log.event_id.toString().padStart(3, '0')}]</span>{' '}
                  {log.message}
                </p>
                <p className="text-xs text-gray-500">{log.timestamp}</p>
              </div>

              <div className="flex-shrink-0 text-right">
                <p className={`text-sm font-semibold ${log.is_anomaly ? 'text-red-500' : 'text-neon-green'}`}>
                  {(log.anomaly_score * 100).toFixed(1)}%
                </p>
              </div>
            </div>
          ))
        )}
        <div ref={logEndRef} />
      </div>
    </div>
  )
}

export default LiveLogStream
