# AI Doctor Setup Guide

## Initial Setup (One-time)

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# You can use nano, vim, or any text editor
nano .env
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
```

### 3. Get OpenAI API Key

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add it to `backend/.env`:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

## Running the Application

### Option 1: Using Start Script (Recommended)

**On macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**On Windows:**
```bash
start.bat
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## First Use

1. Open http://localhost:3000 in your browser
2. Click "Initialize System" button
3. Wait for the medical knowledge base to load (2-5 minutes)
4. Start asking health questions!

## Common Issues

### "Import could not be resolved" errors
These are just linting warnings before dependencies are installed. Run:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Backend connection failed
- Ensure backend is running on port 8000
- Check backend terminal for error messages
- Verify .env file has valid OpenAI API key

### Initialization takes too long
- Reduce the number of documents in the `/initialize` endpoint
- Default is 1000 documents, you can reduce to 500 or 100 for testing

## Stopping the Application

- If using start script: Press `Ctrl+C`
- If manual: Press `Ctrl+C` in both terminal windows

## Development Tips

### Backend Development
```bash
# Run backend with auto-reload
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### Frontend Development
```bash
# Frontend has hot-reload by default
cd frontend
npm run dev
```

### Reset Vector Store
If you want to re-initialize with fresh data:
```bash
# Delete the database
rm -rf backend/chroma_db

# Restart backend and click "Initialize System" again
```

## Testing API Endpoints

You can test the API using curl or the Swagger UI at http://localhost:8000/docs

**Check status:**
```bash
curl http://localhost:8000/status
```

**Initialize system:**
```bash
curl -X POST http://localhost:8000/initialize?max_samples=100
```

**Query:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What are symptoms of diabetes?"}'
```

## Next Steps

- Customize the number of documents loaded
- Adjust the LLM model (GPT-3.5 vs GPT-4)
- Modify the UI styling
- Add new features from the roadmap

## Need Help?

Check the main README.md for more detailed information and troubleshooting steps.
