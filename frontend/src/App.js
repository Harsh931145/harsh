import React, { useState } from 'react';
import './App.css';
import SearchBox from './components/SearchBox';
import AnswerDisplay from './components/AnswerDisplay';
import DocumentManager from './components/DocumentManager';
import Header from './components/Header';

function App() {
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showDocuments, setShowDocuments] = useState(false);

  const handleAnswerReceived = (answerData) => {
    setAnswer(answerData);
    setLoading(false);
  };

  const handleSearchStart = () => {
    setLoading(true);
    setAnswer(null);
  };

  return (
    <div className="App">
      <Header onToggleDocuments={() => setShowDocuments(!showDocuments)} />
      
      <div className="container">
        {showDocuments ? (
          <DocumentManager onClose={() => setShowDocuments(false)} />
        ) : (
          <>
            <div className="main-content">
              <h1 className="title">Exam Preparation Assistant</h1>
              <p className="subtitle">
                Ask questions by typing, pasting screenshots (Ctrl+V), or dragging images
              </p>
              
              <SearchBox 
                onAnswerReceived={handleAnswerReceived}
                onSearchStart={handleSearchStart}
              />
              
              {loading && (
                <div className="loading">
                  <div className="spinner"></div>
                  <p>Searching knowledge base...</p>
                </div>
              )}
              
              {answer && !loading && (
                <AnswerDisplay answer={answer} />
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
