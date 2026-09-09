import React, { useState, useEffect } from 'react';
import { Upload, File, Trash2, RefreshCw, X } from 'lucide-react';
import axios from 'axios';
import './DocumentManager.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function DocumentManager({ onClose }) {
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/documents`);
      setDocuments(response.data.documents);
    } catch (error) {
      console.error('Error loading documents:', error);
      alert('Error loading documents. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.pdf')) {
      alert('Please upload only PDF files');
      return;
    }

    const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
    console.log(`Uploading ${file.name} (${fileSizeMB} MB)...`);

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const startTime = Date.now();
      
      await axios.post(`${API_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(percentCompleted);
          console.log(`Upload progress: ${percentCompleted}%`);
        },
      });
      
      const endTime = Date.now();
      const duration = ((endTime - startTime) / 1000).toFixed(1);
      
      alert(`Document uploaded and processed successfully in ${duration} seconds!`);
      loadDocuments();
    } catch (error) {
      console.error('Error uploading document:', error);
      alert(error.response?.data?.detail || 'Error uploading document');
    } finally {
      setUploading(false);
      setUploadProgress(0);
      e.target.value = '';
    }
  };

  const handleDelete = async (filename) => {
    if (!window.confirm(`Are you sure you want to delete ${filename}?`)) {
      return;
    }

    try {
      await axios.delete(`${API_URL}/documents/${filename}`);
      alert('Document deleted successfully!');
      loadDocuments();
    } catch (error) {
      console.error('Error deleting document:', error);
      alert('Error deleting document');
    }
  };

  const handleRefresh = async () => {
    try {
      setLoading(true);
      await axios.post(`${API_URL}/refresh`);
      alert('Knowledge base refreshed successfully!');
      loadDocuments();
    } catch (error) {
      console.error('Error refreshing knowledge base:', error);
      alert('Error refreshing knowledge base');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="document-manager">
      <div className="manager-header">
        <h2>Document Manager</h2>
        <button className="close-button" onClick={onClose}>
          <X size={24} />
        </button>
      </div>

      <div className="manager-actions">
        <label className="upload-button">
          <Upload size={20} />
          <span>
            {uploading 
              ? `Uploading... ${uploadProgress}%` 
              : 'Upload PDF'}
          </span>
          <input
            type="file"
            accept=".pdf"
            onChange={handleUpload}
            disabled={uploading}
            style={{ display: 'none' }}
          />
        </label>
        
        {uploading && (
          <div className="upload-progress-bar">
            <div 
              className="upload-progress-fill" 
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
        )}

        <button className="refresh-button" onClick={handleRefresh} disabled={loading}>
          <RefreshCw size={20} className={loading ? 'spinning' : ''} />
          <span>Refresh Index</span>
        </button>
      </div>

      <div className="documents-list">
        {loading ? (
          <div className="loading-docs">Loading documents...</div>
        ) : documents.length === 0 ? (
          <div className="empty-state">
            <File size={48} />
            <p>No documents uploaded yet</p>
            <p className="empty-hint">Upload PDF files containing your exam materials</p>
          </div>
        ) : (
          documents.map((doc, index) => (
            <div key={index} className="document-item">
              <File size={24} className="doc-icon" />
              <span className="doc-name">{doc}</span>
              <button
                className="delete-button"
                onClick={() => handleDelete(doc)}
                title="Delete document"
              >
                <Trash2 size={18} />
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default DocumentManager;
