import React, { useState, useRef, useEffect } from 'react';
import { Search, Image as ImageIcon, X } from 'lucide-react';
import axios from 'axios';
import './SearchBox.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function SearchBox({ onAnswerReceived, onSearchStart }) {
  const [question, setQuestion] = useState('');
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);
  const inputRef = useRef(null);
  const containerRef = useRef(null);

  // Handle paste events for images
  useEffect(() => {
    const handlePaste = (e) => {
      const items = e.clipboardData?.items;
      if (!items) return;

      for (let i = 0; i < items.length; i++) {
        const item = items[i];
        
        // Check if the pasted item is an image
        if (item.type.indexOf('image') !== -1) {
          e.preventDefault();
          const blob = item.getAsFile();
          
          if (blob) {
            setImage(blob);
            const reader = new FileReader();
            reader.onloadend = () => {
              setImagePreview(reader.result);
            };
            reader.readAsDataURL(blob);
          }
        }
      }
    };

    // Handle drag and drop
    const handleDragOver = (e) => {
      e.preventDefault();
      setIsDragging(true);
    };

    const handleDragLeave = (e) => {
      e.preventDefault();
      setIsDragging(false);
    };

    const handleDrop = (e) => {
      e.preventDefault();
      setIsDragging(false);

      const files = e.dataTransfer?.files;
      if (files && files.length > 0) {
        const file = files[0];
        if (file.type.startsWith('image/')) {
          setImage(file);
          const reader = new FileReader();
          reader.onloadend = () => {
            setImagePreview(reader.result);
          };
          reader.readAsDataURL(file);
        }
      }
    };

    // Add event listeners
    const containerElement = containerRef.current;
    if (containerElement) {
      containerElement.addEventListener('paste', handlePaste);
      containerElement.addEventListener('dragover', handleDragOver);
      containerElement.addEventListener('dragleave', handleDragLeave);
      containerElement.addEventListener('drop', handleDrop);
    }

    return () => {
      if (containerElement) {
        containerElement.removeEventListener('paste', handlePaste);
        containerElement.removeEventListener('dragover', handleDragOver);
        containerElement.removeEventListener('dragleave', handleDragLeave);
        containerElement.removeEventListener('drop', handleDrop);
      }
    };
  }, []);

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleRemoveImage = () => {
    setImage(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!question.trim() && !image) {
      alert('Please enter a question or upload an image');
      return;
    }

    onSearchStart();

    try {
      const formData = new FormData();
      formData.append('question', question || 'What is shown in this image?');
      if (image) {
        formData.append('image', image);
      }

      const response = await axios.post(`${API_URL}/ask-multipart`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      onAnswerReceived(response.data);
      
      // Clear form after successful submission
      setQuestion('');
      handleRemoveImage();
      
    } catch (error) {
      console.error('Error asking question:', error);
      onAnswerReceived({
        answer: error.response?.data?.detail || 'Error connecting to server. Please make sure the backend is running.',
        sources: [],
        confidence: 0
      });
    }
  };

  return (
    <div className="search-box" ref={containerRef}>
      <form onSubmit={handleSubmit}>
        <div className={`input-container ${isDragging ? 'dragging' : ''}`}>
          <Search className="search-icon" size={24} />
          <input
            ref={inputRef}
            type="text"
            placeholder="Ask a question or paste a screenshot (Ctrl+V)..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="search-input"
          />
          <button
            type="button"
            className="image-button"
            onClick={() => fileInputRef.current?.click()}
            title="Upload screenshot from file"
          >
            <ImageIcon size={24} />
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleImageSelect}
            style={{ display: 'none' }}
          />
        </div>

        {isDragging && (
          <div className="drag-overlay">
            <ImageIcon size={48} />
            <p>Drop image here</p>
          </div>
        )}

        {imagePreview && (
          <div className="image-preview">
            <img src={imagePreview} alt="Preview" />
            <button
              type="button"
              className="remove-image"
              onClick={handleRemoveImage}
            >
              <X size={20} />
            </button>
          </div>
        )}

        {!imagePreview && (
          <div className="paste-hint">
            <ImageIcon className="paste-hint-icon" size={16} />
            <span>Tip: You can paste screenshots directly with Ctrl+V or click the icon to browse files</span>
          </div>
        )}

        <button type="submit" className="submit-button">
          Get Answer
        </button>
      </form>
    </div>
  );
}

export default SearchBox;
