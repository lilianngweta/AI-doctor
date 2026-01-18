# 🚀 Getting Started with AI Doctor

## The Fastest Way to Get Running

### Option 1: Automated Setup (Recommended) ⚡

**On macOS/Linux:**
```bash
./setup.sh
```

**On Windows:**
```cmd
setup.bat
```

This will:
- ✅ Check system requirements
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create .env file
- ✅ Prompt for OpenAI API key

Then run:
```bash
./start.sh    # macOS/Linux
start.bat     # Windows
```

### Option 2: Manual Setup (5 minutes) 🛠️

#### Step 1: Backend (Terminal 1)
```bash
cd backend
python -m venv venv
source venv/bin/activate          # macOS/Linux
# OR
venv\Scripts\activate             # Windows

pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OpenAI API key
python main.py
```

#### Step 2: Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```

#### Step 3: Open Browser
Navigate to: **http://localhost:3000**

## 📋 Pre-Requirements

Before starting, ensure you have:

### Required Software
- [x] **Python 3.8+** ([Download](https://www.python.org/downloads/))
- [x] **Node.js 16+** ([Download](https://nodejs.org/))
- [x] **OpenAI API Key** ([Get Here](https://platform.openai.com/))

### Quick Version Check
```bash
python --version   # Should show 3.8 or higher
node --version     # Should show v16 or higher
```

## 🔑 Getting Your OpenAI API Key

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Click on your profile → "View API Keys"
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)
6. Add to `backend/.env`:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

⚠️ **Important:** Never share or commit your API key!

## 🎯 First Run

1. **Start the Application**
   ```bash
   ./start.sh  # or start.bat on Windows
   ```

2. **Open Your Browser**
   - Navigate to http://localhost:3000
   - You should see the AI Doctor interface

3. **Initialize the System**
   - Click the "Initialize System" button
   - Wait 2-5 minutes for data loading
   - Status will change from "Not Ready" to "Ready"

4. **Start Chatting!**
   - Type your health question
   - Click "Send"
   - Get AI-powered wellness advice

## 💬 Try These First Questions

Once initialized, try asking:
- "What are the symptoms of diabetes?"
- "How can I improve my sleep quality?"
- "What is high blood pressure?"
- "Tell me about the flu"

## 🎨 What You'll See

### Before Initialization
```
┌─────────────────────────────────────┐
│ 🏥 AI Doctor                        │
│ [Initialize System] 🔴 Not Ready   │
├─────────────────────────────────────┤
│                                     │
│ ⚠️ Welcome to AI Doctor!           │
│ The system needs to be initialized │
│ Click "Initialize System" to load  │
│ the medical knowledge base.        │
│                                     │
└─────────────────────────────────────┘
```

### During Initialization
```
┌─────────────────────────────────────┐
│ 🏥 AI Doctor                        │
│ [Initializing...] 🟡 Not Ready     │
├─────────────────────────────────────┤
│                                     │
│ ⚙️ Initializing system with        │
│ medical knowledge from Wikidoc...  │
│ This may take a few minutes.       │
│                                     │
└─────────────────────────────────────┘
```

### After Initialization
```
┌─────────────────────────────────────┐
│ 🏥 AI Doctor                        │
│                      🟢 Ready       │
├─────────────────────────────────────┤
│                                     │
│ 🤖 AI Doctor:                      │
│ Hello! I'm your AI wellness        │
│ advisor. How can I help you?       │
│                                     │
│                          You: 👤    │
│        What are flu symptoms?      │
│                                     │
│ 🤖 AI Doctor:                      │
│ Common flu symptoms include...     │
│                                     │
├─────────────────────────────────────┤
│ [Type your question...] [Send]     │
└─────────────────────────────────────┘
```

## 🚨 Troubleshooting Quick Fixes

### "Cannot find module" errors
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules
npm install
```

### "Connection refused" or CORS errors
- Make sure backend is running on port 8000
- Check terminal for error messages
- Verify .env file has API key

### "OpenAI API error"
- Check API key is correct in `.env`
- Verify you have credits in your OpenAI account
- Key should start with `sk-`

### Initialization takes forever
- Normal first time (2-5 minutes)
- Check internet connection
- Look at backend terminal for progress
- Try with fewer samples: `/initialize?max_samples=100`

### Backend crashes during startup
```bash
# Check for missing dependencies
cd backend
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Check .env file exists and has API key
cat .env
```

## 📚 Where to Go Next

### Essential Reading
1. **[README.md](README.md)** - Full feature overview
2. **[EXAMPLES.md](EXAMPLES.md)** - Sample queries to try
3. **[ARCHITECTURE.md](ARCHITECTURE.md)** - How it all works

### Learn More
- **Backend API:** http://localhost:8000/docs (Swagger UI)
- **Modify Settings:** Check [ARCHITECTURE.md](ARCHITECTURE.md) Configuration section
- **Add Features:** See [README.md](README.md) Roadmap section

## 🎓 Understanding the Workflow

```
YOU type a question
        ↓
Frontend sends to Backend
        ↓
Backend searches ChromaDB
        ↓
Finds relevant medical info
        ↓
Sends to OpenAI GPT
        ↓
GPT generates answer
        ↓
Answer displayed in chat
```

## ⚡ Quick Commands Reference

### Backend
```bash
cd backend
source venv/bin/activate   # Activate environment
python main.py             # Start server
deactivate                 # Exit environment
```

### Frontend
```bash
cd frontend
npm run dev               # Development server
npm run build            # Build for production
npm run preview          # Preview production build
```

### Full Application
```bash
./start.sh               # Start both (Unix)
start.bat               # Start both (Windows)
Ctrl+C                  # Stop servers
```

## 🎯 Success Indicators

You know everything is working when:
- ✅ No errors in terminal windows
- ✅ Backend shows: "Application startup complete"
- ✅ Frontend shows: "Local: http://localhost:3000"
- ✅ Browser displays the AI Doctor interface
- ✅ Status indicator shows green "Ready"
- ✅ You can send messages and get responses

## 💡 Pro Tips

1. **Keep terminals open** - Don't close terminal windows while using the app
2. **Watch the logs** - Backend terminal shows what's happening
3. **Be patient** - First initialization takes a few minutes
4. **Start simple** - Try basic questions first
5. **Read disclaimers** - This is for information, not diagnosis

## 🎉 You're Ready!

Follow these steps in order:
1. ✅ Check requirements (Python, Node, API key)
2. ✅ Run setup script
3. ✅ Start the application
4. ✅ Initialize the system
5. ✅ Ask your first question!

---

**Need help?** Check the other documentation files:
- Setup issues? → [SETUP.md](SETUP.md)
- Want examples? → [EXAMPLES.md](EXAMPLES.md)
- Technical details? → [ARCHITECTURE.md](ARCHITECTURE.md)

**Ready to start?** Run `./setup.sh` now! 🚀
