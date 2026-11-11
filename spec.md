# Constitution RAG Project

## Overview

This project aims to build a Retrieval-Augmented Generation (RAG) system using constitutional documents to enable querying and generation of new constitution-style documents.

## Objectives
1. Query the RAG about any information in the constitutions
2. Create new constitution-style documents with reference to a set of constitutions as guidance

## Recommended Tools for RAG System

### 1. Data Processing & Preprocessing
- **PDF Extraction**: PyMuPDF (fitz) or pdfplumber for extracting text from PDF constitution files
- **Text Cleaning**: NLTK, spaCy, or regular expressions for cleaning and normalizing text
- **Chunking**: LangChain's RecursiveCharacterTextSplitter or similar tools for dividing documents into manageable chunks

### 2. Vector Database & Embeddings
- **Embedding Models**: Sentence Transformers (all-MiniLM-L6-v2 or similar) or OpenAI embeddings
- **Vector Store**: ChromaDB, Pinecone, or FAISS for storing and retrieving vector embeddings
- **Retrieval**: Similarity search using cosine similarity or other distance metrics

### 3. LLM Integration
- **Large Language Models**: OpenAI GPT models, Hugging Face models (LLaMA, Mistral), or local models like Llama.cpp
- **Prompt Engineering**: LangChain's prompt templates or custom prompt engineering frameworks
- **Generation Pipeline**: LangChain's LLM chains for orchestrating retrieval and generation

### 4. Framework & Libraries
- **LangChain**: Comprehensive framework for building LLM applications with built-in support for data loading, vector stores, and LLM integration
- **LlamaIndex (formerly GPT Index)**: Alternative framework focused on data indexing and retrieval
- **Transformers (Hugging Face)**: For running local models and custom fine-tuning

### 5. Environment Management
- **uv**: Modern Python dependency management tool for creating isolated environments
- **Poetry**: Alternative dependency and environment management tool

## Implementation Approach

1. **Document Ingestion**
   - Extract text from PDF constitution files
   - Clean and preprocess text data
   - Split into chunks for embedding

2. **Vector Store Creation**
   - Generate embeddings for document chunks
   - Store in vector database
   - Configure retrieval parameters

3. **Query Interface**
   - Implement similarity search
   - Create prompt templates for question answering
   - Build generation pipeline

4. **Generation Capability**
   - Enable creating new constitution-style documents
   - Support for guided generation with reference to specific constitutions
   - Version control for generated documents

## Technology Stack Recommendation

For this project, I recommend the following stack:

### Core Libraries:
- Python 3.8+
- LangChain (for RAG orchestration)
- Hugging Face Transformers (for LLMs)
- Sentence Transformers (for embeddings)
- ChromaDB (for vector storage)

### Environment Management:
- uv: Modern Python dependency management tool

### Setup Steps:
1. Install uv: https://docs.astral.sh/uv/
2. Create virtual environment with uv:
   ```bash
   uv venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   uv pip install -e .
   ```
4. Create data processing pipeline
5. Set up vector database
6. Configure LLM integration
7. Build query interface
8. Implement generation functionality

## File Structure
```
constitution-rag/
├── spec.md                 # This specification file
├── constitutions/          # Input PDF constitution files
├── output/                 # Output directory for processed data and results
├── src/
│   ├── __init__.py
│   ├── data_loader.py      # PDF extraction and text processing
│   ├── vector_store.py     # Vector database setup and management
│   └── rag_pipeline.py     # Main RAG system implementation
├── demo.py                 # Demo script for testing the system
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies (uv format)
└── pyproject.toml          # Project configuration for uv
```

## Next Steps
1. Create the basic project structure
2. Set up Python virtual environment with uv
3. Install required dependencies
4. Implement data loading and preprocessing
5. Build vector database
6. Create query interface
7. Implement generation capability