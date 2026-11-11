"""
Data loader module for extracting and processing constitution documents.
"""

import os
import pymupdf
from typing import List, Dict
import re

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file using PyMuPDF.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    doc = pymupdf.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

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
        if filename.endswith('.pdf'):
            file_path = os.path.join(constitution_dir, filename)
            
            # Extract text from PDF
            raw_text = extract_text_from_pdf(file_path)
            
            # Clean the text
            cleaned_text = clean_text(raw_text)
            
            constitutions.append({
                'filename': filename,
                'content': cleaned_text,
                'source_path': file_path
            })
    
    return constitutions

def process_constitution_files(constitution_dir: str, output_dir: str) -> None:
    """
    Process all constitution files and save them in a structured format.
    
    Args:
        constitution_dir (str): Directory containing input PDFs
        output_dir (str): Directory to save processed files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    constitutions = load_constitution_files(constitution_dir)
    
    for constitution in constitutions:
        filename = constitution['filename']
        content = constitution['content']
        
        # Save cleaned text to output directory
        output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Processed {filename} and saved to {output_path}")

if __name__ == "__main__":
    # Example usage
    constitutions_dir = "constitutions"
    output_dir = "output/processed_constitutions"
    
    process_constitution_files(constitutions_dir, output_dir)