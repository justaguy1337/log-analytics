import React, { useState } from 'react'
import { Database, Loader } from 'lucide-react'

const DatasetSelector = ({ datasets = [], onDatasetSelect, loading = false }) => {
  const [selectedDataset, setSelectedDataset] = useState(null)

  const datasetInfo = {
    hdfs: {
      name: 'HDFS v1',
      description: 'Hadoop Distributed File System logs',
      samples: '11,175 sequences',
      color: 'from-blue-600 to-cyan-500',
    },
    bgl: {
      name: 'BGL',
      description: 'Blue Gene/L supercomputer logs',
      samples: '4,747,963 events',
      color: 'from-purple-600 to-pink-500',
    },
    openstack: {
      name: 'OpenStack',
      description: 'OpenStack cloud computing logs',
      samples: '207,266 events',
      color: 'from-orange-600 to-red-500',
    },
  }

  const handleSelect = (dataset) => {
    setSelectedDataset(dataset)
    onDatasetSelect(dataset)
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
          <Database className="text-neon-green" size={28} />
          Available Datasets
        </h2>
        <p className="text-gray-400">Select a dataset to analyze</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {['hdfs', 'bgl', 'openstack'].map((dataset) => {
          const info = datasetInfo[dataset]
          const isSelected = selectedDataset === dataset

          return (
            <button
              key={dataset}
              onClick={() => handleSelect(dataset)}
              disabled={loading}
              className={`card-hover card transform transition-all duration-300 ${
                isSelected ? 'ring-2 ring-neon-green scale-105' : ''
              } hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              <div className={`inline-block p-3 rounded-lg bg-gradient-to-r ${info.color} mb-4`}>
                <Database className="text-white" size={24} />
              </div>

              <h3 className="text-lg font-bold mb-1">{info.name}</h3>
              <p className="text-sm text-gray-400 mb-3">{info.description}</p>

              <div className="flex items-center justify-between">
                <span className="text-xs text-neon-green font-semibold">{info.samples}</span>
                {isSelected && (
                  <span className="text-xs bg-neon-green text-black px-2 py-1 rounded font-semibold">
                    Selected
                  </span>
                )}
              </div>
            </button>
          )
        })}
      </div>

      {loading && (
        <div className="flex items-center gap-2 text-neon-green">
          <Loader size={20} className="animate-spin" />
          <span>Loading dataset...</span>
        </div>
      )}
    </div>
  )
}

export default DatasetSelector
