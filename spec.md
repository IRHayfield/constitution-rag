# Constitution RAG Project

## Overview

This project aims to build a Retrieval-Augmented Generation (RAG) system using constitutional documents to enable querying and generation of new constitution-style documents.

## Objectives
1. Query the RAG about any information in the constitutions
2. Create new constitution-style documents with reference to a set of constitutions as guidance

## Tools used by this RAG System

### 1. Data Processing & Preprocessing
- **HTML Text Extraction**: BeautifulSoup for extracting text from html constitution web pages
- **Text Cleaning**: NLTK, spaCy, or regular expressions for cleaning and normalizing text
- **Chunking**: LangChain's RecursiveCharacterTextSplitter or similar tools for dividing documents into manageable chunks

### 2. Vector Database & Embeddings
- **Embedding Models**: Sentence Transformers (all-MiniLM-L6-v2 or similar) or OpenAI embeddings
- **Vector Store**: ChromaDB for storing and retrieving vector embeddings
- **Retrieval**: Similarity search using cosine similarity or other distance metrics

### 3. LLM Integration
- **Local LLMs with Ollama**: Run models like Mistral, Llama2, or Phi locally via Ollama
- **Prompt Engineering**: LangChain's prompt templates or custom prompt engineering frameworks
- **Generation Pipeline**: LangChain's LLM chains for orchestrating retrieval and generation

### 5. Environment Management
- **uv**: Modern Python dependency management tool for creating isolated environments
- **Ollama**: Local LLM serving platform for running models without internet connection

## Implementation Approach

1. **Document Ingestion**
   - Download constitutions from the web
   - Clean and preprocess text data
   - Split into chunks for embedding

2. **Vector Store Creation**
   - Generate embeddings for document chunks
   - Store in vector database
   - Configure retrieval parameters

3. **Query Interface**
   - Implement similarity search
   - Create prompt templates for question answering
   - Build generation pipeline using Ollama LLMs

4. **Generation Capability**
   - Enable creating new constitution-style documents
   - Support for guided generation with reference to specific constitutions
   - Version control for generated documents

## Technology Stack Recommendation

### Core Libraries:
- Python 3.14+
- LangChain (for RAG orchestration)
- Hugging Face Transformers (for LLMs)
- Sentence Transformers (for embeddings)
- ChromaDB (for vector storage)

### Environment Management:
- uv: Modern Python dependency management tool

### Local LLM Platform:
- Ollama: For running local models like Mistral, Llama2, or Phi without internet connection

### Setup Steps:
1. Install uv: https://docs.astral.sh/uv/
2. Install Ollama: https://ollama.com/download
3. Pull required models with Ollama:
   ```bash
   ollama pull mistral
   ollama pull llama2
   ```
4. Create virtual environment with uv:
   ```bash
   uv venv
   source .venv/bin/activate
   ```
5. Install dependencies:
   ```bash
   uv sync
   ```
6. Create data processing pipeline
7. Set up vector database
8. Configure Ollama LLM integration
9. Build query interface
10. Implement generation functionality

## File Structure
```
constitution-rag/
├── spec.md                 # This specification file
├── constitutions/          # Input txt constitution files
├── src/
│   ├── __init__.py
│   ├── data_loader.py      # PDF extraction and text processing
│   ├── vector_store.py     # Vector database setup and management
│   └── rag_pipeline.py     # Main RAG system implementation
├── demo.py                 # Demo script for testing the system
├── README.md               # Project documentation
└── pyproject.toml          # Project configuration for uv
```

## Next Steps
1. Create the basic project structure
2. Set up Python virtual environment with uv
3. Install required dependencies
4. Implement data loading and preprocessing
5. Build vector database
6. Configure Ollama LLM integration
7. Create query interface
8. Implement generation capability