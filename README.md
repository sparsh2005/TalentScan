# TalentScan

A full-stack application for resume parsing and AI-powered talent search.

## Features
- Resume upload and parsing (PDF, DOCX)
- Automated information extraction using LLM
- HR Chatbot for intelligent candidate queries
- Modern React frontend
- FastAPI backend
- Supabase integration for data storage

## Project Structure
```
talentscan/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── requirements.txt
│   └── main.py
└── frontend/
    ├── public/
    ├── src/
    └── package.json
```

## Setup Instructions

### Backend Setup
1. Create a Python virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory with:
```
OPENAI_API_KEY=your_key_here
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

4. Run the backend server:
```bash
uvicorn main:app --reload
```

### Frontend Setup
1. Install dependencies:
```bash
cd frontend
npm install
```

2. Create a `.env` file in the frontend directory with:
```
REACT_APP_API_URL=http://localhost:8000
```

3. Run the development server:
```bash
npm start
```

## API Endpoints
- `POST /api/resume/upload` - Upload and parse resume
- `POST /api/chat` - HR Chatbot endpoint
- `GET /api/candidates` - Get all candidates

## Tech Stack
- Backend: FastAPI, pdfminer.six, python-docx, OpenAI API
- Frontend: React, Axios, TailwindCSS
- Database: Supabase
