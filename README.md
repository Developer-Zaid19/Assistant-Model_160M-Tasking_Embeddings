# 🧠 Local AI Studio

A desktop AI platform that combines local language model inference, semantic search, vector embeddings, and intelligent desktop automation.

Local AI Studio enables users to interact with an offline AI assistant capable of understanding natural language, retrieving information, and executing desktop commands without relying on cloud services.

---

## ✨ Features

* 🤖 Local GPT-NeoX powered AI assistant
* 🔍 Semantic search using vector embeddings
* 🧠 Natural language command understanding
* ⚡ Desktop automation through Python system APIs
* 📚 Wikipedia-powered knowledge retrieval
* 🔒 Fully local execution with no external AI dependency
* 📈 Cosine similarity based command ranking
* 🗂 Embedding-based command database

---


## 🚀 How to Run

## 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-folder>
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 4. Download Model Files

Create the following directory structure:

```text
models/
└── 160M/
```

Place the model files inside the `160M` folder:

```text
models/
└── 160M/
    ├── config.json
    ├── model.safetensors
    └── tokenizer.json
```

> Ensure all required model weights and configuration files are present before starting the application.

## 5. Run the Application

```bash
python main.py
```

If your project uses a different entry point, replace `main.py` with the appropriate file.

## Troubleshooting

* Verify that the virtual environment is activated.
* Ensure all dependencies are installed successfully.
* Confirm that the `models/160M` directory contains the required model files.
* Check the terminal output for any missing package or file errors.

---

## 🚀 Overview


Local AI Studio combines conversational AI with semantic command execution.

Instead of relying on traditional keyword matching, the assistant converts both user queries and predefined commands into vector embeddings. This allows it to understand intent and trigger actions even when users phrase requests differently.

For example:

```text
Open Chrome
Launch my browser
Start Google Chrome
```

All of these requests can be mapped to the same underlying command through semantic similarity.

---

## 🧩 How It Works

### 1. Language Model

A locally hosted GPT-NeoX model handles conversational responses and text generation.

```text
User Input
      │
      ▼
 GPT-NeoX Model
      │
      ▼
 AI Response
```

---

### 2. Embedding Engine

User messages are converted into 384-dimensional vector embeddings.

```text
Text
  │
  ▼
Embedding Model
  │
  ▼
384D Vector
```

These vectors represent semantic meaning rather than exact words.

---

### 3. Semantic Command Matching

When a user sends a request:

1. The query embedding is generated.
2. Stored command embeddings are retrieved.
3. Cosine similarity scores are calculated.
4. The most relevant command is selected.
5. The action is executed automatically.

```text
User Query
      │
      ▼
Query Embedding
      │
      ▼
Similarity Search
      │
      ▼
Best Match
      │
      ▼
Command Execution
```

---

### 4. Desktop Automation

Matched commands are executed using Python system utilities such as:

* `os.startfile()`
* `subprocess`
* `webbrowser`

This enables actions such as:

* Opening applications
* Launching websites
* Running local programs
* Automating desktop workflows

---

## 🏗 Architecture

```text
┌─────────────────────┐
│     User Input      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Embedding Generator │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Similarity Search   │
│ (Cosine Ranking)    │
└──────────┬──────────┘
           │
 ┌─────────┴─────────┐
 ▼                   ▼
Command Match   GPT-NeoX Model
 ▼                   ▼
Automation      AI Response
 ▼                   ▼
Desktop Action   User Output
```

---

## 🛠 Technology Stack

### AI & NLP

* GPT-NeoX 160M
* Sentence Embeddings
* Semantic Search
* Cosine Similarity

### Backend

* Python
* Wikipedia API

### Automation

* os.startfile
* subprocess
* webbrowser

### Data Processing

* Vector Embeddings
* Command Ranking
* Semantic Matching

---

## 🎯 Key Concepts

### Embedding-Based Command Intelligence

Traditional assistants depend heavily on keyword matching.

Local AI Studio uses semantic embeddings to understand intent, allowing users to interact naturally without memorizing exact commands.

### Vector Search

Every command is represented as a numerical vector. User requests are transformed into vectors and compared against stored command embeddings to identify the closest semantic match.

### Intelligent Automation

By combining semantic search with desktop execution APIs, the platform bridges the gap between conversational AI and real-world desktop actions.

---

## 🔮 Future Improvements

* Multi-command workflows
* Voice assistant integration
* Local document search
* Custom command training
* RAG-based knowledge retrieval
* Plugin ecosystem
* Larger local language models

---

## 📜 License

This project is intended for educational and experimental purposes.

---

### Built with Python, GPT-NeoX, Semantic Search, and Local AI Automation.
