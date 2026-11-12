#!/usr/bin/env python3
"""
Quick demonstration script for the Constitution RAG system with Ollama.
"""

import os
import sys
import argparse

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rag_pipeline import ConstitutionRAG

def main():
    parser = argparse.ArgumentParser(description='Constitution RAG System Demo')
    parser.add_argument('--query', type=str, help='Query to ask about constitutions')
    parser.add_argument('--generate', type=str, help='Prompt for generating a new constitution')
    parser.add_argument('--setup-only', action='store_true', help='Only set up the system without querying')
    parser.add_argument('--model', type=str, default='mistral', help='Ollama model to use')
    
    args = parser.parse_args()
    
    # Initialize RAG system
    rag = ConstitutionRAG(model_name=args.model)
    
    print("Setting up Constitution RAG system...")
    rag.setup_pipeline(use_existing=True)
    
    if args.setup_only:
        print("System setup complete. No queries executed.")
        return
        
    if args.query:
        print(f"\nQuery: {args.query}")
        answer = rag.query(args.query)
        print(f"Answer: {answer}")
        
    if args.generate:
        print(f"\nGenerating constitution based on prompt: {args.generate}")
        generated = rag.generate_constitution(args.generate)
        print(f"Generated constitution: {generated}")

if __name__ == "__main__":
    main()