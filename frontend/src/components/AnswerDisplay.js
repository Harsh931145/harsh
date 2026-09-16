import React from 'react';
import { CheckCircle, BookOpen, TrendingUp } from 'lucide-react';
import './AnswerDisplay.css';

function AnswerDisplay({ answer }) {
  const confidencePercentage = Math.round(answer.confidence * 100);
  const confidenceLevel = 
    confidencePercentage >= 80 ? 'high' : 
    confidencePercentage >= 50 ? 'medium' : 'low';
  const answerText = answer.answer && answer.answer.trim()
    ? answer.answer
    : 'Answer unavailable. Please try again.';

  return (
    <div className="answer-display">
      <div className="answer-header">
        <CheckCircle className="check-icon" size={28} />
        <div>
          <span className="answer-label">Result</span>
          <h2>Answer</h2>
        </div>
      </div>

      <div className="answer-content">
        <div className="answer-badge">
          <CheckCircle size={18} />
          <span>Highlighted answer</span>
        </div>
        <p>{answerText}</p>
      </div>

      {answer.sources && answer.sources.length > 0 && (
        <div className="sources-section">
          <div className="sources-header">
            <BookOpen size={20} />
            <h3>Sources</h3>
          </div>
          <div className="sources-list">
            {answer.sources.map((source, index) => (
              <span key={index} className="source-tag">
                {source}
              </span>
            ))}
          </div>
        </div>
      )}

      {answer.confidence !== undefined && (
        <div className="confidence-section">
          <div className="confidence-header">
            <TrendingUp size={20} />
            <h3>Confidence</h3>
          </div>
          <div className="confidence-bar-container">
            <div 
              className={`confidence-bar ${confidenceLevel}`}
              style={{ width: `${confidencePercentage}%` }}
            >
              <span className="confidence-text">{confidencePercentage}%</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default AnswerDisplay;
