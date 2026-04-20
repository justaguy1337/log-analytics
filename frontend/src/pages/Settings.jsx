import React, { useState } from 'react'
import { Settings as SettingsIcon, Save, RefreshCw } from 'lucide-react'

const Settings = () => {
  const [settings, setSettings] = useState({
    anomalyThreshold: 0.5,
    sequenceLength: 50,
    batchSize: 32,
    lstmWeight: 0.5,
    ifWeight: 0.5,
    autoRefresh: true,
    refreshInterval: 10,
  })

  const [saved, setSaved] = useState(false)

  const handleChange = (key, value) => {
    setSettings({ ...settings, [key]: value })
    setSaved(false)
  }

  const handleSave = () => {
    // TODO: Save to backend
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-4xl font-bold">Settings</h1>
        <p className="text-gray-400">Configure anomaly detection and platform behavior</p>
      </div>

      {/* Settings Form */}
      <div className="max-w-2xl space-y-6">
        {/* Anomaly Detection Settings */}
        <div className="card">
          <h3 className="text-lg font-bold mb-6 flex items-center gap-2">
            <SettingsIcon size={24} className="text-neon-green" />
            Anomaly Detection
          </h3>

          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Anomaly Threshold
              </label>
              <div className="flex items-center gap-4">
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={settings.anomalyThreshold}
                  onChange={(e) => handleChange('anomalyThreshold', parseFloat(e.target.value))}
                  className="flex-1"
                />
                <span className="text-lg font-bold text-neon-green w-16 text-right">
                  {settings.anomalyThreshold.toFixed(1)}
                </span>
              </div>
              <p className="text-xs text-gray-500 mt-2">
                Higher values report fewer anomalies
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Sequence Length
              </label>
              <input
                type="number"
                min="10"
                max="200"
                value={settings.sequenceLength}
                onChange={(e) => handleChange('sequenceLength', parseInt(e.target.value))}
                className="input w-full"
              />
              <p className="text-xs text-gray-500 mt-2">
                Number of log events to process as one sequence
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Batch Size
              </label>
              <input
                type="number"
                min="1"
                max="256"
                value={settings.batchSize}
                onChange={(e) => handleChange('batchSize', parseInt(e.target.value))}
                className="input w-full"
              />
            </div>
          </div>
        </div>

        {/* Model Weights */}
        <div className="card">
          <h3 className="text-lg font-bold mb-6">Model Combination Weights</h3>

          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                LSTM Weight: {settings.lstmWeight.toFixed(2)}
              </label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={settings.lstmWeight}
                onChange={(e) => handleChange('lstmWeight', parseFloat(e.target.value))}
                className="w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Isolation Forest Weight: {settings.ifWeight.toFixed(2)}
              </label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={settings.ifWeight}
                onChange={(e) => handleChange('ifWeight', parseFloat(e.target.value))}
                className="w-full"
              />
            </div>

            <div className="p-3 bg-dark-bg rounded text-sm text-gray-300">
              ⚠️ Make sure both weights add up to approximately 1.0 for best results
            </div>
          </div>
        </div>

        {/* UI Settings */}
        <div className="card">
          <h3 className="text-lg font-bold mb-6">Interface</h3>

          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-dark-bg rounded">
              <div>
                <p className="font-medium">Auto-refresh Dashboard</p>
                <p className="text-xs text-gray-500 mt-1">Automatically update statistics</p>
              </div>
              <input
                type="checkbox"
                checked={settings.autoRefresh}
                onChange={(e) => handleChange('autoRefresh', e.target.checked)}
                className="w-5 h-5 cursor-pointer accent-neon-green"
              />
            </div>

            {settings.autoRefresh && (
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Refresh Interval (seconds)
                </label>
                <input
                  type="number"
                  min="5"
                  max="300"
                  value={settings.refreshInterval}
                  onChange={(e) => handleChange('refreshInterval', parseInt(e.target.value))}
                  className="input w-full"
                />
              </div>
            )}
          </div>
        </div>

        {/* Save Button */}
        <div className="flex gap-3">
          <button onClick={handleSave} className="btn btn-primary flex items-center gap-2">
            <Save size={18} />
            Save Settings
          </button>
          <button className="btn btn-secondary flex items-center gap-2">
            <RefreshCw size={18} />
            Reset to Default
          </button>
        </div>

        {saved && (
          <div className="p-4 bg-neon-green/10 border border-neon-green rounded-lg flex items-center gap-2 text-neon-green">
            <span>✓</span>
            <span>Settings saved successfully</span>
          </div>
        )}
      </div>
    </div>
  )
}

export default Settings
