import React, { useState, useEffect } from 'react';
import { 
  FileSpreadsheet, 
  MessageSquare, 
  BarChart3, 
  Settings, 
  Upload, 
  Download,
  Undo2,
  Redo2,
  Save,
  Play,
  Sparkles,
  Folder,
  AlertCircle,
  CheckCircle,
  Loader2
} from 'lucide-react';
import { useStore } from './store/useStore';
import { api } from './services/api';
import './App.css';

// Import components
import { FileExplorer } from './components/FileExplorer';
import { ExcelViewer } from './components/ExcelViewer';
import { AIChat } from './components/AIChat';
import { ChartPanel } from './components/ChartPanel';
import { TemplateGallery } from './components/TemplateGallery';
import { OperationHistory } from './components/OperationHistory';
import { SettingsPanel } from './components/SettingsPanel';
import { Toast } from './components/Toast';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedFile, setSelectedFile] = useState(null);
  const [systemStatus, setSystemStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  
  const { toasts, addToast, removeToast } = useStore();

  // Load system status on mount
  useEffect(() => {
    loadSystemStatus();
    const interval = setInterval(loadSystemStatus, 30000); // Every 30s
    return () => clearInterval(interval);
  }, []);

  const loadSystemStatus = async () => {
    try {
      const status = await api.getStatus();
      setSystemStatus(status);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load system status:', error);
      addToast({
        type: 'error',
        message: 'Failed to connect to backend',
        duration: 5000
      });
      setLoading(false);
    }
  };

  const handleFileUpload = async (files) => {
    for (const file of files) {
      try {
        await api.uploadFile(file);
        addToast({
          type: 'success',
          message: `${file.name} uploaded successfully`,
          duration: 3000
        });
      } catch (error) {
        addToast({
          type: 'error',
          message: `Failed to upload ${file.name}`,
          duration: 5000
        });
      }
    }
  };

  const renderSystemStatus = () => {
    if (!systemStatus) return null;

    const ollamaStatus = systemStatus.ollama?.connected;
    const modelCount = systemStatus.ollama?.available_models?.length || 0;

    return (
      <div className="status-bar">
        <div className="status-item">
          {ollamaStatus ? (
            <CheckCircle className="status-icon success" size={16} />
          ) : (
            <AlertCircle className="status-icon warning" size={16} />
          )}
          <span className="status-text">
            Ollama: {ollamaStatus ? `Active (${modelCount} models)` : 'Disconnected'}
          </span>
        </div>
        
        <div className="status-item">
          <FileSpreadsheet className="status-icon" size={16} />
          <span className="status-text">
            {systemStatus.excel?.files_count || 0} files
          </span>
        </div>

        {systemStatus.ollama?.current_model && (
          <div className="status-item">
            <Sparkles className="status-icon" size={16} />
            <span className="status-text">
              {systemStatus.ollama.current_model}
            </span>
          </div>
        )}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="loading-screen">
        <Loader2 className="spinner" size={48} />
        <h2>Loading Ollama Excel Studio...</h2>
      </div>
    );
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-left">
          <FileSpreadsheet className="app-icon" size={32} />
          <h1 className="app-title">Ollama Excel Studio</h1>
          <span className="version-badge">v5.0</span>
        </div>
        
        <div className="header-center">
          {renderSystemStatus()}
        </div>

        <div className="header-right">
          <button className="icon-button" title="Settings">
            <Settings size={20} />
          </button>
        </div>
      </header>

      {/* Main Content */}
      <div className="app-content">
        {/* Sidebar */}
        <aside className="sidebar">
          <nav className="sidebar-nav">
            <button
              className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`}
              onClick={() => setActiveTab('dashboard')}
            >
              <Folder size={20} />
              <span>Dashboard</span>
            </button>

            <button
              className={`nav-item ${activeTab === 'excel' ? 'active' : ''}`}
              onClick={() => setActiveTab('excel')}
              disabled={!selectedFile}
            >
              <FileSpreadsheet size={20} />
              <span>Excel Editor</span>
            </button>

            <button
              className={`nav-item ${activeTab === 'chat' ? 'active' : ''}`}
              onClick={() => setActiveTab('chat')}
            >
              <MessageSquare size={20} />
              <span>AI Assistant</span>
            </button>

            <button
              className={`nav-item ${activeTab === 'charts' ? 'active' : ''}`}
              onClick={() => setActiveTab('charts')}
            >
              <BarChart3 size={20} />
              <span>Visualizations</span>
            </button>

            <button
              className={`nav-item ${activeTab === 'templates' ? 'active' : ''}`}
              onClick={() => setActiveTab('templates')}
            >
              <Sparkles size={20} />
              <span>Templates</span>
            </button>

            <button
              className={`nav-item ${activeTab === 'history' ? 'active' : ''}`}
              onClick={() => setActiveTab('history')}
            >
              <Undo2 size={20} />
              <span>History</span>
            </button>
          </nav>
        </aside>

        {/* Main Panel */}
        <main className="main-panel">
          {activeTab === 'dashboard' && (
            <div className="dashboard">
              <div className="dashboard-header">
                <h2>Files & Quick Actions</h2>
                <label className="upload-button">
                  <Upload size={20} />
                  <span>Upload Files</span>
                  <input
                    type="file"
                    multiple
                    accept=".xlsx,.xls,.csv"
                    onChange={(e) => handleFileUpload(Array.from(e.target.files))}
                    style={{ display: 'none' }}
                  />
                </label>
              </div>

              <div className="dashboard-grid">
                <div className="dashboard-section files-section">
                  <FileExplorer 
                    onSelectFile={setSelectedFile}
                    selectedFile={selectedFile}
                  />
                </div>

                <div className="dashboard-section quick-actions">
                  <h3>Quick Actions</h3>
                  <div className="action-grid">
                    <button className="action-card">
                      <FileSpreadsheet size={24} />
                      <span>New File</span>
                    </button>
                    <button className="action-card">
                      <Upload size={24} />
                      <span>Import CSV</span>
                    </button>
                    <button className="action-card">
                      <Sparkles size={24} />
                      <span>Templates</span>
                    </button>
                    <button className="action-card">
                      <Play size={24} />
                      <span>Batch Ops</span>
                    </button>
                  </div>
                </div>

                <div className="dashboard-section ai-preview">
                  <h3>AI Assistant</h3>
                  <div className="ai-preview-content">
                    <MessageSquare size={48} className="ai-icon" />
                    <p>Ask me anything about your Excel files!</p>
                    <button 
                      className="primary-button"
                      onClick={() => setActiveTab('chat')}
                    >
                      Start Chatting
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'excel' && selectedFile && (
            <ExcelViewer 
              filename={selectedFile}
              onUpdate={() => {/* Refresh */}}
            />
          )}

          {activeTab === 'chat' && (
            <AIChat 
              currentFile={selectedFile}
              onFileAction={(action, filename) => {
                if (action === 'open') {
                  setSelectedFile(filename);
                  setActiveTab('excel');
                }
              }}
            />
          )}

          {activeTab === 'charts' && (
            <ChartPanel 
              filename={selectedFile}
            />
          )}

          {activeTab === 'templates' && (
            <TemplateGallery 
              onApplyTemplate={(template, filename) => {
                addToast({
                  type: 'success',
                  message: `Applied template: ${template}`,
                  duration: 3000
                });
              }}
            />
          )}

          {activeTab === 'history' && (
            <OperationHistory 
              filename={selectedFile}
              onRestore={(operationId) => {
                addToast({
                  type: 'success',
                  message: 'Operation restored',
                  duration: 3000
                });
              }}
            />
          )}
        </main>
      </div>

      {/* Toast Notifications */}
      <div className="toast-container">
        {toasts.map(toast => (
          <Toast
            key={toast.id}
            {...toast}
            onClose={() => removeToast(toast.id)}
          />
        ))}
      </div>
    </div>
  );
}

export default App;
