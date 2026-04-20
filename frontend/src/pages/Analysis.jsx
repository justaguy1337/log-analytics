import React, { useState } from 'react'
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { TrendingUp, Zap, Target } from 'lucide-react'
import StatCard from '../components/StatCard'

const Analysis = () => {
  const [selectedModel, setSelectedModel] = useState('hybrid')

  const confusionMatrixData = [
    { label: 'True Negatives', value: 8952, color: '#00ff88' },
    { label: 'False Positives', value: 312, color: '#fbbf24' },
    { label: 'False Negatives', value: 142, color: '#f87171' },
    { label: 'True Positives', value: 594, color: '#60a5fa' },
  ]

  const modelComparison = [
    {
      name: 'LSTM',
      precision: 85,
      recall: 82,
      f1: 83.4,
    },
    {
      name: 'Isolation Forest',
      precision: 78,
      recall: 88,
      f1: 82.7,
    },
    {
      name: 'Hybrid',
      precision: 88,
      recall: 86,
      f1: 87.0,
    },
  ]

  const roc_curveData = [
    { fpr: 0, tpr: 0 },
    { fpr: 5, tpr: 75 },
    { fpr: 10, tpr: 88 },
    { fpr: 15, tpr: 92 },
    { fpr: 20, tpr: 94 },
    { fpr: 30, tpr: 96 },
    { fpr: 50, tpr: 98 },
    { fpr: 100, tpr: 100 },
  ]

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-4xl font-bold">Model Analysis</h1>
        <p className="text-gray-400">Deep dive into model performance and insights</p>
      </div>

      {/* Model Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard
          icon={TrendingUp}
          title="Precision"
          value={87.8}
          unit="%"
          color="green"
        />
        <StatCard
          icon={Target}
          title="Recall"
          value={85.9}
          unit="%"
          color="blue"
        />
        <StatCard
          icon={Zap}
          title="F1-Score"
          value={86.8}
          unit="%"
          color="purple"
        />
      </div>

      {/* Model Comparison */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-bold mb-6">Model Performance Comparison</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={modelComparison}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2d3748" />
              <XAxis dataKey="name" stroke="#718096" style={{ fontSize: '12px' }} />
              <YAxis stroke="#718096" style={{ fontSize: '12px' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1a1f3a',
                  border: '1px solid #2d3748',
                  borderRadius: '8px',
                }}
              />
              <Legend />
              <Bar dataKey="precision" fill="#00ff88" />
              <Bar dataKey="recall" fill="#00d4ff" />
              <Bar dataKey="f1" fill="#8b5cf6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3 className="text-lg font-bold mb-6">Confusion Matrix (HDFS)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={confusionMatrixData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ label, value }) => `${label}: ${value}`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {confusionMatrixData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1a1f3a',
                  border: '1px solid #2d3748',
                  borderRadius: '8px',
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* ROC Curve */}
      <div className="card">
        <h3 className="text-lg font-bold mb-6">ROC Curve (AUC = 0.92)</h3>
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={roc_curveData} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2d3748" />
            <XAxis
              dataKey="fpr"
              label={{ value: 'False Positive Rate (%)', position: 'insideBottomRight', offset: -5 }}
              stroke="#718096"
              style={{ fontSize: '12px' }}
            />
            <YAxis
              label={{ value: 'True Positive Rate (%)', angle: -90, position: 'insideLeft' }}
              stroke="#718096"
              style={{ fontSize: '12px' }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1a1f3a',
                border: '1px solid #2d3748',
                borderRadius: '8px',
              }}
            />
            <Bar dataKey="tpr" fill="#00ff88" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Model Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-bold mb-4">LSTM Model</h3>
          <div className="space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Architecture</span>
              <span className="font-semibold">2-layer, 128 hidden</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Vocabulary Size</span>
              <span className="font-semibold">2,847 events</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Sequence Length</span>
              <span className="font-semibold">50 events</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Training Loss</span>
              <span className="font-semibold">0.0428</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Validation Accuracy</span>
              <span className="text-neon-green font-semibold">94.2%</span>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-bold mb-4">Isolation Forest Model</h3>
          <div className="space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Trees</span>
              <span className="font-semibold">100</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Features</span>
              <span className="font-semibold">6 statistical features</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Contamination Rate</span>
              <span className="font-semibold">10%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Training Samples</span>
              <span className="font-semibold">11,175</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Anomaly Detection Rate</span>
              <span className="text-neon-green font-semibold">88.5%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Feature Importance */}
      <div className="card">
        <h3 className="text-lg font-bold mb-6">Feature Importance (Isolation Forest)</h3>
        <div className="space-y-4">
          {[
            { name: 'Unique Event Count', importance: 92 },
            { name: 'Event Frequency Variance', importance: 85 },
            { name: 'Average Event ID', importance: 76 },
            { name: 'Event Sequence Length', importance: 68 },
            { name: 'Max Event ID', importance: 54 },
            { name: 'Min Event ID', importance: 42 },
          ].map((feature, idx) => (
            <div key={idx}>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium">{feature.name}</span>
                <span className="text-sm font-semibold text-neon-green">{feature.importance}%</span>
              </div>
              <div className="w-full bg-dark-bg rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-neon-green to-neon-blue h-2 rounded-full"
                  style={{ width: `${feature.importance}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Analysis
