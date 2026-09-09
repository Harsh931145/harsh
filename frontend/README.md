# Frontend - Exam Dashboard

React-based user interface for the Exam Preparation Dashboard.

## Installation

```bash
npm install
```

## Running

```bash
npm start
```

Opens at `http://localhost:3000`

## Building for Production

```bash
npm run build
```

Creates optimized production build in `build/` folder.

## Project Structure

```
frontend/
├── public/
│   └── index.html           # HTML template
├── src/
│   ├── components/          # React components
│   │   ├── Header.js       # Top navigation
│   │   ├── SearchBox.js    # Question input
│   │   ├── AnswerDisplay.js # Answer view
│   │   └── DocumentManager.js # PDF management
│   ├── App.js              # Main application
│   ├── index.js            # Entry point
│   └── *.css               # Component styles
└── package.json
```

## Components

### Header
- Logo and branding
- "Manage Documents" button
- Responsive design

### SearchBox
- Text input for questions
- Image upload button
- Screenshot preview
- Form submission

### AnswerDisplay
- Formatted answer text
- Source document tags
- Confidence score bar
- Color-coded confidence levels

### DocumentManager
- List of uploaded PDFs
- Upload new documents
- Delete documents
- Refresh index

## Environment Variables

Create `.env` file:

```env
REACT_APP_API_URL=http://localhost:8000
```

## Styling

- Uses CSS modules for component isolation
- Gradient backgrounds
- Responsive breakpoints at 768px
- Smooth animations and transitions

## Dependencies

- **react**: UI library
- **react-dom**: DOM renderer
- **axios**: HTTP requests
- **lucide-react**: Icon library
- **react-scripts**: Build tooling

## Development Tips

### Hot Reload
Changes auto-reload in development mode

### Component Testing
```bash
npm test
```

### Linting
```bash
npm run lint
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## API Integration

All API calls go through `axios`:

```javascript
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Example request
const response = await axios.post(`${API_URL}/ask`, {
  question: "What is AI?"
});
```

## Responsive Design

- Desktop: Full-width layout with sidebars
- Tablet: Stacked layout
- Mobile: Single column, optimized touch targets
