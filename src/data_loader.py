"""
Data loader module for extracting and processing constitution documents.
"""

import os
import pymupdf
from typing import List, Dict
import re

def clean_text(text: str) -> str:
    """
    Clean and normalize extracted text.
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that might interfere with processing
    text = re.sub(r'[^\w\s\.\,\!\?\;\:]', '', text)
    
    return text.strip()

def load_constitution_files(constitution_dir: str) -> List[Dict]:
    """
    Load all constitution files from the specified directory.
    
    Args:
        constitution_dir (str): Path to directory containing constitution PDFs
        
    Returns:
        List[Dict]: List of dictionaries with filename and content
    """
    constitutions = []
    
    for filename in os.listdir(constitution_dir):
        file_path = os.path.join(constitution_dir, filename)
        
        raw_text = ""

        with open(file_path, "r") as file:
            raw_text = file.read()
        
        # Clean the text
        cleaned_text = clean_text(raw_text)
        
        constitutions.append({
            'filename': filename,
            'content': cleaned_text,
            'source_path': file_path
        })
    
    return constitutions

def process_pdf_constitution_files(constitution_dir: str, output_dir: str) -> None:
    """
    Process all constitution files and save them in a structured format.
    
    Args:
        constitution_dir (str): Directory containing input PDFs
        output_dir (str): Directory to save processed files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(constitution_dir):
        pdf_path = os.path.join(constitution_dir, filename)
        stem, _ = os.path.splitext(filename)
        txt_filename = stem + ".txt"
        txt_path = os.path.join(output_dir, txt_filename)
        
        with pymupdf.open(pdf_path) as doc:
            text = "\n".join(page.get_text("text") for page in doc)
        
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
            
        print(f"Processed {filename} and saved to {txt_path}")

if __name__ == "__main__":
    # Example usage
    constitutions_dir = "constitutions"
    output_dir = "output/processed_constitutions"
    
    process_constitution_files(constitutions_dir, output_dir)