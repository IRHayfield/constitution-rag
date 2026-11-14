"""
Data loader module for extracting and processing constitution documents.
"""

import os
import pymupdf
from typing import List, Dict
import re
import requests
from bs4 import BeautifulSoup

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

def download_constitution_from_web(constitution_name: str, output_dir: str) -> None:
    """
    Download constitution text from the constitution project website.
    
    Args:
        constitution_name (str): Name of the constitution to download
        output_dir (str): Directory to save the downloaded file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Construct URL
    url = f"https://www.constituteproject.org/constitution/{constitution_name}"
    
    try:
        # Fetch the webpage
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the constitution content
        content_div = soup.find('div', class_='constitution-content__copy')
        
        if content_div:
            # Extract text from the content div
            text_content = content_div.get_text(strip=False)
            
            # Write to file
            filename = f"{constitution_name}.txt"
            file_path = os.path.join(output_dir, filename)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text_content)
                
            print(f"Downloaded and saved {filename}")
        else:
            print(f"Could not find constitution content for {constitution_name}")
            
    except requests.RequestException as e:
        print(f"Error downloading {constitution_name}: {e}")

def download_constitutions(constitutions_list_file: str, output_dir: str) -> None:
    """
    Download constitutions listed in a file and save them to the output directory.
    
    Args:
        constitutions_list_file (str): Path to a file containing newline-separated constitution names
        output_dir (str): Directory to save the downloaded files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        with open(constitutions_list_file, 'r') as f:
            constitution_names = [line.strip() for line in f if line.strip()]
        
        for constitution_name in constitution_names:
            # Check if file already exists
            filename = f"{constitution_name}.txt"
            file_path = os.path.join(output_dir, filename)
            
            if os.path.exists(file_path):
                print(f"File {filename} already exists, skipping download")
                continue
                
            download_constitution_from_web(constitution_name, output_dir)
            
    except FileNotFoundError:
        print(f"Error: Could not find file {constitutions_list_file}")
    except Exception as e:
        print(f"Error reading constitutions list: {e}")

if __name__ == "__main__":
    # Example usage
    constitutions_list = "constitutions_list.txt"
    constitutions_dir = "constitutions"
    
    download_constitutions(constitutions_list, constitutions_dir)
