# AI Group Chat & Document Editor

## Concept & Vision

A professional tool that combines multi-model AI chat with document editing. The left panel hosts group conversations with multiple AI models simultaneously, while the right panel provides a Word-like rich text editor. Users can fluidly transfer chat content to the editor for refinement and export to DOCX.

## Technical Stack

- **Backend**: Python Flask
- **Database**: MongoDB (local)
- **Frontend**: HTML/CSS/JavaScript with Quill.js (rich text editor)
- **AI Models**: OpenAI, Claude, DeepSeek, Minimax (extensible)

## Design Language

- **Aesthetic**: Clean, professional, productivity-focused
- **Colors**:
  - Primary: #2563eb (blue)
  - Secondary: #64748b (slate)
  - Accent: #10b981 (emerald)
  - Background: #f8fafc
  - Text: #1e293b
- **Typography**: Inter (UI), system fonts fallback
- **Layout**: Two-panel split view (resizable)

## Layout & Structure

### Main Interface
```
┌─────────────────────────────────────────────────────┐
│  Header: App Title + Settings + Model Selector      │
├──────────────────────┬──────────────────────────────┤
│                      │                              │
│   Chat Panel         │   Document Editor            │
│   (40% width)        │   (60% width)                │
│                      │                              │
│   ┌────────────┐     │   ┌──────────────────────┐   │
│   │ Model Tabs │     │   │   Toolbar             │   │
│   │ ○ DeepSeek │     │   │ B I U | H1 H2 | List │   │
│   │ ○ Claude   │     │   └──────────────────────┘   │
│   │ ○ OpenAI   │     │                              │
│   │ ○ Minimax  │     │   ┌──────────────────────┐   │
│   └────────────┘     │   │                      │   │
│                      │   │   Rich Text Area     │   │
│   ┌────────────┐     │   │                      │   │
│   │ Chat Area  │     │   │                      │   │
│   │            │     │   │                      │   │
│   └────────────┘     │   └──────────────────────┘   │
│                      │                              │
│   ┌────────────┐     │   ┌──────────────────────┐   │
│   │ Input Box  │     │   │ Save | Export DOCX   │   │
│   └────────────┘     │   └──────────────────────┘   │
│                      │                              │
├──────────────────────┴──────────────────────────────┤
│  Status Bar: Connection status + Document status     │
└─────────────────────────────────────────────────────┘
```

## Features & Interactions

### Chat Panel
- **Model Selection**: Checkbox list to select which models participate in group chat
- **Message Input**: Textarea with send button (Enter to send, Shift+Enter for newline)
- **Chat Display**: Message bubbles with model name, timestamp, copy button
- **Actions per message**:
  - Copy to clipboard
  - Insert into editor at cursor position
  - Delete message

### Document Editor
- **Rich Text Toolbar**:
  - Bold, Italic, Underline
  - Headings (H1, H2, H3)
  - Bullet list, Numbered list
  - Text alignment (left, center, right)
  - Clear formatting
- **Content Operations**:
  - Manual save (Ctrl+S)
  - Auto-save every 30 seconds
  - Export to DOCX
- **Document List**: Sidebar to manage saved documents

### Settings Modal
- API key configuration for each model
- MongoDB connection settings
- Theme toggle (light/dark)

## Data Model

### MongoDB Collections

**conversations**
```json
{
  "_id": "ObjectId",
  "title": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "messages": [
    {
      "id": "string",
      "model": "string",
      "role": "user|assistant",
      "content": "string",
      "timestamp": "datetime"
    }
  ]
}
```

**documents**
```json
{
  "_id": "ObjectId",
  "title": "string",
  "content": "string (HTML)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**settings**
```json
{
  "_id": "ObjectId",
  "api_keys": {
    "openai": "string",
    "anthropic": "string",
    "deepseek": "string",
    "minimax": "string"
  },
  "mongodb_uri": "string"
}
```

## API Endpoints

### Chat
- `POST /api/chat` - Send message to selected models
- `GET /api/conversations` - List all conversations
- `POST /api/conversations` - Create new conversation
- `GET /api/conversations/<id>` - Get conversation details
- `DELETE /api/conversations/<id>` - Delete conversation

### Documents
- `GET /api/documents` - List all documents
- `POST /api/documents` - Create/save document
- `GET /api/documents/<id>` - Get document
- `PUT /api/documents/<id>` - Update document
- `DELETE /api/documents/<id>` - Delete document
- `GET /api/documents/<id>/export` - Export as DOCX

### Settings
- `GET /api/settings` - Get current settings
- `PUT /api/settings` - Update settings

## Component Inventory

### ChatMessage
- States: user (right-aligned, blue), assistant (left-aligned, gray)
- Hover: show action buttons (copy, insert, delete)

### ModelSelector
- Checkbox per model
- Visual indicator when model is responding

### EditorToolbar
- Icon buttons with tooltips
- Active state for current formatting

### DocumentCard
- Title, preview snippet, last modified date
- Hover: show edit/delete buttons

### Modal
- Backdrop blur
- Close on Escape key

## Technical Approach

### Backend (Flask)
- Flask with Blueprint organization
- PyMongo for MongoDB connection
- python-docx for DOCX export
- langchain or direct API calls for AI models

### Frontend
- Vanilla JavaScript (no heavy frameworks)
- Quill.js for rich text editing
- Fetch API for backend communication
- CSS Grid for layout
- CSS Variables for theming
