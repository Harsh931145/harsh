# Changelog

## Latest Update - Enhanced Screenshot Feature

### ✨ New Features

#### 1. **Paste Screenshots Directly (Ctrl+V)**
- No need to browse for files anymore!
- Take a screenshot and paste it directly into the search box
- Works with Windows Snipping Tool, Print Screen, and all screenshot tools
- Instant preview before submitting

#### 2. **Drag and Drop Support**
- Drag image files directly onto the search box
- Visual feedback when dragging (blue dashed border)
- Drop to add - it's that simple!

#### 3. **Three Ways to Add Images**
- **Method 1**: Paste with Ctrl+V (fastest!)
- **Method 2**: Drag and drop files
- **Method 3**: Browse files with camera icon (original method still works)

### 🎨 UI Improvements

- Updated placeholder text: "Ask a question or paste a screenshot (Ctrl+V)..."
- Added helpful tip below search box
- Visual drag-and-drop overlay
- Better user guidance

### 📝 Updated Documentation

- Updated README.md with new screenshot methods
- Created PASTE_FEATURE.md guide
- Updated subtitle in app interface

### 🔧 Technical Changes

**Frontend Changes:**
- `SearchBox.js`: Added paste event listener
- `SearchBox.js`: Added drag-and-drop handlers
- `SearchBox.css`: Added drag overlay styles
- `App.js`: Updated subtitle text

**Files Modified:**
- `frontend/src/components/SearchBox.js`
- `frontend/src/components/SearchBox.css`
- `frontend/src/App.js`
- `README.md`

**New Files:**
- `frontend/PASTE_FEATURE.md`
- `CHANGELOG.md`

### 💡 Usage Tips

**Fastest Workflow:**
1. Press `Win+Shift+S` (Windows Snipping Tool)
2. Select the area to capture
3. Click in search box
4. Press `Ctrl+V`
5. Click "Get Answer"

**No file browsing needed - screenshot and paste instantly!**

---

## Previous Features

### Core Functionality
- AI-powered question answering
- PDF knowledge base management
- Text and image question support
- Confidence scoring
- Source citations
- Document upload/delete/refresh

### Technical Stack
- Backend: FastAPI, OpenAI, FAISS, Sentence Transformers
- Frontend: React, Axios, Lucide Icons
- AI: GPT-4 for text, GPT-4 Vision for images

---

**Version**: 1.1.0  
**Date**: 2026-09-09
