"""
Vector store module for managing embeddings and retrieval.
"""

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
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
            texts.append(doc['content'])
            metadatas.append({
                'filename': doc['filename'],
                'source': doc.get('source_path', ''),
                'type': 'constitution'
            })
        
        # Split texts into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        
        split_texts = text_splitter.split_text("\n\n".join(texts))
        split_metadatas = []
        
        for i, text in enumerate(split_texts):
            # Distribute metadata to chunks
            doc_index = min(i // 5, len(metadatas) - 1)  # Assuming 5 chunks per doc
            split_metadatas.append(metadatas[doc_index])
        
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
            self.vectorstore.persist()
            print("Vector store saved successfully")
        else:
            print("No vector store to save")

if __name__ == "__main__":
    # Example usage
    # This would typically be called after data processing
    pass