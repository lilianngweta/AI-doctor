# 🏥 AI Doctor - Wellness Advisor

An AI-powered wellness application that provides health advice and helps address symptoms of various health conditions using medical knowledge from the Wikidoc dataset.

---

# Demo
You can use the app [here](https://ai-doctor-inky.vercel.app/)

---

# File structure

* `backend/`: Backend (FastAPI-based)
   * `data_loader.py`: loads data from Hugging Face
   * `main.py`: main entry point
   * `requirements.txt`
   * `vector_store.py`: Converts data into a LlamaIndex vector database
* `chroma_db`
   * `chroma.sqlite3`
* `frontend/`: Frontend (React-based)
   * `index.html`
   * `package-lock.json`
   * `package.json`
   * `src/`
      * `App.css`
      * `App.jsx`
      * `index.css`
      * `main.jsx`
   * `vite.config.js`

---

## 🚀 Quick Start

**New here?** Start with the [**Getting Started Guide**](GETTING_STARTED.md) for the fastest setup!

```bash
./setup.sh    # Run automated setup (macOS/Linux)
./start.sh    # Launch the application
```

Then open http://localhost:3000 in your browser.

---

## 📚 Documentation

- **[🚀 Getting Started](GETTING_STARTED.md)** - ⭐ Start here! Fastest way to get running
- **[📋 Setup Guide](SETUP.md)** - Detailed installation and setup instructions
- **[🏗️ Architecture](ARCHITECTURE.md)** - System architecture and technical details
- **[💡 Examples](EXAMPLES.md)** - Sample queries and use cases
- **[✅ Checklist](CHECKLIST.md)** - Quick reference checklist
- **[🎉 Project Summary](PROJECT_SUMMARY.md)** - Complete project overview

## 🌟 Features

- **AI-Powered Health Advice**: Get wellness recommendations based on medical knowledge
- **Medical Knowledge Base**: Uses the medical_meadow_wikidoc dataset from HuggingFace
- **Smart Search**: ChromaDB vector store for efficient similarity search
- **RAG Architecture**: LlamaIndex integration for retrieval-augmented generation
- **Modern Chat Interface**: Beautiful React-based chat UI
- **Fast API Backend**: Python FastAPI backend with async support

## 🏗️ Architecture

- **Backend**: Python, FastAPI, ChromaDB, LlamaIndex
- **Frontend**: React, Vite, Axios
- **Data Source**: medical_meadow_wikidoc dataset from HuggingFace
- **Vector Store**: ChromaDB for semantic search
- **LLM**: OpenAI GPT-3.5-turbo (configurable)

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- OpenAI API key (for LLM functionality)

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the backend server**
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```
   
   The app will be available at `http://localhost:3000`

## 📖 Usage

### First Time Setup

1. Start both backend and frontend servers
2. Open the app in your browser at `http://localhost:3000`
3. Click the **"Initialize System"** button to load the medical knowledge base
   - This will download and process the Wikidoc dataset (may take a few minutes)
   - The system loads 1000 medical documents by default
4. Once initialized, you can start asking health-related questions!

### Example Questions

- "What are the symptoms of diabetes?"
- "How can I manage high blood pressure?"
- "What causes migraine headaches?"
- "What are treatment options for anxiety?"
- "How do I improve my sleep quality?"

## 🔧 API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /status` - System status
- `POST /initialize` - Initialize vector store with medical data
- `POST /query` - Query the AI doctor
- `POST /reset` - Reset the vector store

## 📁 Project Structure

```
AI-doctor/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── data_loader.py       # HuggingFace data loading
│   ├── vector_store.py      # ChromaDB & LlamaIndex integration
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment variables template
│   └── .gitignore
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Styling
│   │   ├── main.jsx         # Entry point
│   │   └── index.css        # Global styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .gitignore
├── README.md
└── LICENSE
```

## ⚙️ Configuration

### Backend Configuration (`.env`)

```env
# OpenAI API Key (required)
OPENAI_API_KEY=your_key_here

# ChromaDB settings
CHROMA_DB_PATH=./chroma_db

# Server settings
HOST=0.0.0.0
PORT=8000
```

### Customization Options

**Adjust number of documents to load:**
```python
# In main.py, modify the initialize_index function default
max_samples: Optional[int] = 5000  # Load more documents
```

**Change LLM model:**
```python
# In vector_store.py, modify MedicalVectorStore.__init__
self.llm = OpenAI(
    model="gpt-4",  # Use GPT-4 instead
    temperature=0.1,
    max_tokens=512
)
```

**Adjust retrieval settings:**
```python
# In vector_store.py, modify query engine creation
self.query_engine = self.index.as_query_engine(
    similarity_top_k=5,  # Return more similar documents
    response_mode="compact"
)
```

## 🧪 Development

### Backend Development

```bash
cd backend
python -m pytest  # Run tests (if available)
python main.py    # Run with auto-reload
```

### Frontend Development

```bash
cd frontend
npm run dev      # Development server with hot reload
npm run build    # Build for production
npm run preview  # Preview production build
```

## ⚠️ Important Disclaimer

**This AI application provides general wellness information for educational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.**

## 📊 Dataset Information

This application uses the **medical_meadow_wikidoc** dataset from HuggingFace:
- **Source**: [medalpaca/medical_meadow_wikidoc](https://huggingface.co/datasets/medalpaca/medical_meadow_wikidoc)
- **Content**: Medical information from Wikidoc
- **Format**: Question-answer pairs about medical conditions, symptoms, and treatments

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Medical data from [Wikidoc](https://www.wikidoc.org/) via HuggingFace
- [LlamaIndex](https://www.llamaindex.ai/) for RAG framework
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [FastAPI](https://fastapi.tiangolo.com/) for backend framework
- [React](https://react.dev/) for frontend framework

## 📞 Support

If you encounter any issues or have questions:
1. Check the [troubleshooting section](#troubleshooting)
2. Review backend logs for error messages
3. Ensure all dependencies are correctly installed
4. Verify your OpenAI API key is valid

## 🔍 Troubleshooting

### Backend Issues

**Import errors:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**OpenAI API errors:**
- Verify your API key is correct in `.env`
- Check you have credits available in your OpenAI account

**ChromaDB errors:**
- Delete the `chroma_db` folder and re-initialize

### Frontend Issues

**Dependencies not installing:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**CORS errors:**
- Ensure backend is running on port 8000
- Check CORS middleware configuration in `main.py`

### General

**System initialization takes too long:**
- Reduce `max_samples` parameter when calling `/initialize`
- Use a faster embedding model

**Out of memory errors:**
- Reduce the number of documents loaded
- Use a machine with more RAM

---

This project was done at [Sundai Club](https://research.sundai.club)
