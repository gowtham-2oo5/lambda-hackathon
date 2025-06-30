import React, { useEffect, useState } from 'react';
import { useHistoryDashboard } from '../hooks/useHistoryDashboard';
import { ReadmeHistoryItem } from '@/types/dashboard';

const HistoryDashboard: React.FC = () => {
  const { 
    history, 
    loading, 
    error, 
    stats,
    fetchHistory, 
    deleteRecord, 
    isAuthenticated 
  } = useHistoryDashboard();

  const [selectedRecord, setSelectedRecord] = useState<ReadmeHistoryItem | null>(null);

  useEffect(() => {
    if (isAuthenticated()) {
      fetchHistory();
    }
  }, [isAuthenticated, fetchHistory]);

  const handleDelete = async (requestId: string): Promise<void> => {
    if (window.confirm('Are you sure you want to delete this record?')) {
      try {
        await deleteRecord(requestId);
      } catch (error) {
        console.error('Failed to delete record:', error);
      }
    }
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleString();
  };

  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'processing': return 'bg-yellow-100 text-yellow-800';
      case 'failed': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string): string => {
    switch (status) {
      case 'completed': return '✅';
      case 'processing': return '⏳';
      case 'failed': return '❌';
      default: return '❓';
    }
  };

  const calculateAvgProcessingTime = (): number => {
    const completedRecords = history.filter(record => 
      record.status === 'completed' && record.processingTime && record.processingTime > 0
    );
    
    if (completedRecords.length === 0) return 0;
    
    const totalTime = completedRecords.reduce((sum, record) => 
      sum + (record.processingTime || 0), 0
    );
    
    return totalTime / completedRecords.length;
  };

  if (!isAuthenticated()) {
    return (
      <div className="max-w-4xl mx-auto p-6 text-center">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-8">
          <h2 className="text-2xl font-bold text-blue-800 mb-4">
            🔐 Authentication Required
          </h2>
          <p className="text-blue-600 mb-4">
            Please sign in with Amazon Cognito to view your README generation history.
          </p>
          <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            Sign In
          </button>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto p-6 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Loading your README history...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h2 className="text-xl font-bold text-red-800 mb-2">Error Loading History</h2>
          <p className="text-red-600">{error}</p>
          <button 
            onClick={fetchHistory}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const avgProcessingTime = calculateAvgProcessingTime();

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          📊 README Generation History
        </h1>
        <p className="text-gray-600">
          Here's your README generation activity and statistics.
        </p>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-blue-50 p-6 rounded-lg">
          <div className="text-2xl font-bold text-blue-600">{stats.total}</div>
          <div className="text-sm text-blue-800 font-medium">Total Generated</div>
        </div>
        
        <div className="bg-green-50 p-6 rounded-lg">
          <div className="text-2xl font-bold text-green-600">{stats.completed}</div>
          <div className="text-sm text-green-800 font-medium">Completed</div>
        </div>
        
        <div className="bg-yellow-50 p-6 rounded-lg">
          <div className="text-2xl font-bold text-yellow-600">{stats.processing}</div>
          <div className="text-sm text-yellow-800 font-medium">Processing</div>
        </div>
        
        <div className="bg-purple-50 p-6 rounded-lg">
          <div className="text-2xl font-bold text-purple-600">
            {avgProcessingTime > 0 ? `${Math.round(avgProcessingTime)}s` : 'N/A'}
          </div>
          <div className="text-sm text-purple-800 font-medium">Avg Time</div>
        </div>
      </div>

      {/* History Table */}
      {history.length === 0 ? (
        <div className="bg-gray-50 rounded-lg p-12 text-center">
          <div className="text-6xl mb-4">📝</div>
          <h3 className="text-xl font-semibold text-gray-800 mb-2">No READMEs Generated Yet</h3>
          <p className="text-gray-600 mb-6">
            Start by generating your first README from a GitHub repository!
          </p>
          <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            Generate README
          </button>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="px-6 py-4 bg-gray-50 border-b">
            <h2 className="text-lg font-semibold text-gray-800">Recent Activity</h2>
          </div>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Repository
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Created
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Processing Time
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Project Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {history.map((record) => (
                  <tr key={record.requestId} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {record.repoName}
                        </div>
                        <div className="text-sm text-gray-500 truncate max-w-xs">
                          {record.repoUrl}
                        </div>
                      </div>
                    </td>
                    
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(record.status)}`}>
                        <span className="mr-1">{getStatusIcon(record.status)}</span>
                        {record.status}
                      </span>
                    </td>
                    
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatDate(record.createdAt)}
                    </td>
                    
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {record.processingTime && record.processingTime > 0 ? `${Math.round(record.processingTime)}s` : 'N/A'}
                    </td>
                    
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div className="max-w-32 truncate" title={record.projectType}>
                        {record.projectType || 'N/A'}
                      </div>
                    </td>
                    
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                      {record.readmeS3Url && (
                        <a
                          href={record.readmeS3Url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-900"
                        >
                          View
                        </a>
                      )}
                      
                      <button
                        onClick={() => setSelectedRecord(record)}
                        className="text-gray-600 hover:text-gray-900"
                      >
                        Details
                      </button>
                      
                      <button
                        onClick={() => handleDelete(record.requestId)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Record Details Modal */}
      {selectedRecord && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-96 overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold">Record Details</h3>
                <button
                  onClick={() => setSelectedRecord(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
              
              <div className="space-y-3 text-sm">
                <div>
                  <span className="font-medium">Request ID:</span> {selectedRecord.requestId}
                </div>
                <div>
                  <span className="font-medium">Repository:</span> {selectedRecord.repoUrl}
                </div>
                <div>
                  <span className="font-medium">Status:</span> 
                  <span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(selectedRecord.status)}`}>
                    {selectedRecord.status}
                  </span>
                </div>
                <div>
                  <span className="font-medium">Created:</span> {formatDate(selectedRecord.createdAt)}
                </div>
                {selectedRecord.completedAt && (
                  <div>
                    <span className="font-medium">Completed:</span> {formatDate(selectedRecord.completedAt)}
                  </div>
                )}
                {selectedRecord.projectType && (
                  <div>
                    <span className="font-medium">Project Type:</span> {selectedRecord.projectType}
                  </div>
                )}
                {selectedRecord.primaryLanguage && (
                  <div>
                    <span className="font-medium">Primary Language:</span> {selectedRecord.primaryLanguage}
                  </div>
                )}
                {selectedRecord.frameworks && selectedRecord.frameworks.length > 0 && (
                  <div>
                    <span className="font-medium">Frameworks:</span> {selectedRecord.frameworks.join(', ')}
                  </div>
                )}
                {selectedRecord.processingTime && (
                  <div>
                    <span className="font-medium">Processing Time:</span> {Math.round(selectedRecord.processingTime)}s
                  </div>
                )}
                {selectedRecord.executionArn && (
                  <div>
                    <span className="font-medium">Execution ARN:</span>
                    <div className="text-xs text-gray-600 break-all">{selectedRecord.executionArn}</div>
                  </div>
                )}
                {selectedRecord.readmeS3Url && (
                  <div>
                    <span className="font-medium">README URL:</span>
                    <div className="text-xs">
                      <a 
                        href={selectedRecord.readmeS3Url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800 break-all"
                      >
                        {selectedRecord.readmeS3Url}
                      </a>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default HistoryDashboard;
