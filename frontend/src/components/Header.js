import React from 'react';
import { BookOpen, FileText } from 'lucide-react';
import './Header.css';

function Header({ onToggleDocuments }) {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <BookOpen size={32} />
          <span>Exam Dashboard</span>
        </div>
        <button className="doc-button" onClick={onToggleDocuments}>
          <FileText size={20} />
          <span>Manage Documents</span>
        </button>
      </div>
    </header>
  );
}

export default Header;
