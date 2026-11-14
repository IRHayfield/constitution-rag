"""
Vector store module for managing embeddings and retrieval.
"""

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict
import os

class ConstitutionVectorStore:
    """
    Class for managing vector storage of constitution documents.
    """
    
    def __init__(self, persist_directory: str = "vector_store"):
        """
        Initialize the vector store.
        
        Args:
            persist_directory (str): Directory to persist vector database
        """
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = None
        
    def create_vectorstore(self, documents: List[Dict]) -> None:
        """
        Create vector store from processed documents.
        
        Args:
            documents (List[Dict]): List of document dictionaries with 'content' and 'metadata'
        """
        # Prepare documents for vectorization
        texts = []
        metadatas = []
        for doc in documents:
            content = doc['content'].strip()
            if content:  # Only process non-empty content
                texts.append(content)
                metadatas.append({
                    'filename': doc['filename'],
                    'source': doc.get('source_path', ''),
                    'type': 'constitution'
                })
        
        if not texts:
            raise ValueError("No valid text content found in documents")
        
        # Split texts into chunks
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            encoding_name="cl100k_base",
            chunk_size=500,          # ~500 tokens (~2,000 characters)
            chunk_overlap=50,        # 10% overlap to preserve boundary context
            is_separator_regex=True,
            separators=[
                r"\n(?=ARTICLE\s+[IVXLCDM\d]+)",  # Split before Articles (e.g., ARTICLE I)
                r"\n(?=Section\s+\d+\.)",          # Split before Sections (e.g., Section 1.)
                r"\n(?=\(\d+\)|[a-z]\))",          # Split before sub-clauses like (1) or a)
                r"\n\n",
                r"\n",
                r"(?<=\.)\s+",                     # Split at sentence endings
                r" ",
                r""
            ]
        )
        
        individual_chunks = []
        individual_chunk_metadatas = []
        
        for doc_content, doc_metadata in zip(texts, metadatas):
            # Split document's content
            doc_split_texts = text_splitter.split_text(doc_content)
            
            # Add each chunk with its metadata
            for chunk in doc_split_texts:
                if chunk.strip():  # Only add non-empty chunks
                    individual_chunks.append(chunk)
                    individual_chunk_metadatas.append(doc_metadata)
        
        split_texts = individual_chunks
        split_metadatas = individual_chunk_metadatas
        
        if not split_texts:
            raise ValueError("No valid text chunks found after splitting")
        
        # Create vector store
        self.vectorstore = Chroma.from_texts(
            texts=split_texts,
            metadatas=split_metadatas,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        print(f"Created vector store with {len(split_texts)} chunks")
        
    def load_vectorstore(self) -> None:
        """
        Load existing vector store from persistence directory.
        """
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """
        Search for relevant documents.
        
        Args:
            query (str): Query string
            k (int): Number of results to return
            
        Returns:
            List[Dict]: List of search results with content and metadata
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Call create_vectorstore() or load_vectorstore() first.")
            
        results = self.vectorstore.similarity_search(query, k=k)
        
        return [
            {
                'content': result.page_content,
                'metadata': result.metadata
            } for result in results
        ]
        
    def save(self) -> None:
        """
        Save the vector store to disk.
        """
        if self.vectorstore is not None:
            print("Vector store saved successfully")
        else:
            print("No vector store to save")

if __name__ == "__main__":
    # Example usage
    # This would typically be called after data processing
    pass