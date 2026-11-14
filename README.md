# Constitution RAG System

A Retrieval-Augmented Generation (RAG) system for analyzing and generating constitutional documents with Ollama integration.

## Overview

This project implements a RAG system that can:
1. Query information from constitutional documents
2. Generate new constitution-style documents based on guidance

## Features

- Downloading of constitutions from the web
- PDF processing of pdf constitutional documents
- Vector storage and similarity search
- Local LLM integration using Ollama
- Modular architecture for extensibility

## Installation

### Prerequisites

1. Install [uv](https://docs.astral.sh/uv/)
2. Install [Ollama](https://ollama.com/download)
3. Pull required models:
   ```bash
   ollama pull mistral
   ollama pull llama2
   ```

### Setup

```bash
# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv sync
```

## Usage

### Setup
```bash
python demo.py --setup-only
```

### Query
```bash
python demo.py --query "What are the fundamental rights mentioned in the constitutions?"
```

### Generate
```bash
python demo.py --generate "Create a new constitution using principles from constitutions written before 1900"
```

## Project Structure

```
constitution-rag/
├── spec.md                 # Specification document
├── constitutions/          # Input TXT constitution files
├── output/                 # Processed documents and results
├── src/
│   ├── __init__.py
│   ├── data_loader.py      # PDF extraction and text processing
│   ├── vector_store.py     # Vector database setup and management
│   └── rag_pipeline.py     # Main RAG system implementation
├── demo.py                 # Demo script
├── README.md               # This file
├── requirements.txt        # Python dependencies (for reference)
└── pyproject.toml          # Project configuration for uv
```

## Technology Stack

- **LangChain**: For RAG orchestration and LLM integration
- **Sentence Transformers**: For generating document embeddings  
- **ChromaDB**: For vector storage and similarity search
- **Ollama**: For running local LLMs like Mistral, Llama2, or Phi
- **PyMuPDF**: For PDF text extraction
- **BeautifulSoup**: For html text extraction

## License

MIT