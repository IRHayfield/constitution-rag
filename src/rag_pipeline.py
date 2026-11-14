"""
Main RAG pipeline for constitution queries and generation with Ollama integration.
"""

from langchain_classic.chains import RetrievalQA
from langchain_ollama import OllamaLLM
from langchain_classic.prompts import PromptTemplate
from src.data_loader import load_constitution_files, download_constitutions
from src.vector_store import ConstitutionVectorStore
import os

class ConstitutionRAG:
    """
    Main RAG system for constitution documents with Ollama integration.
    """
    
    def __init__(self, vector_store_path: str = "vector_store", model_name: str = "mistral"):
        """
        Initialize the RAG system.
        
        Args:
            vector_store_path (str): Path to vector store directory
            model_name (str): Name of the Ollama model to use
        """
        self.vector_store_path = vector_store_path
        self.model_name = model_name
        self.vectorstore = ConstitutionVectorStore(persist_directory=vector_store_path)
        self.qa_chain = None
        
    def setup_pipeline(self, use_existing: bool = True) -> None:
        """
        Set up the complete RAG pipeline.
        
        Args:
            use_existing (bool): Whether to use existing vector store or rebuild
        """
        if use_existing and os.path.exists(self.vector_store_path):
            print("Loading existing vector store...")
            self.vectorstore.load_vectorstore()
        else:
            print("Creating new vector store from constitution files...")
            # Download constitution files first
            constitutions_list = "constitutions_list.txt"
            constitutions_dir = "constitutions"
            
            download_constitutions(constitutions_list, constitutions_dir)
            
            # Load processed documents
            documents = load_constitution_files(constitutions_dir)
            
            # Create vector store
            self.vectorstore.create_vectorstore(documents)
            self.vectorstore.save()
            
        print("Pipeline setup complete.")
        
    def query(self, question: str) -> str:
        """
        Query the RAG system with a question.
        
        Args:
            question (str): Question to ask
            
        Returns:
            str: Answer from the RAG system
        """
        if self.vectorstore.vectorstore is None:
            raise ValueError("Vector store not initialized. Call setup_pipeline() first.")
            
        # Create retrieval QA chain using Ollama
        prompt_template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        
        {context}
        
        Question: {question}
        Helpful Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        
        # Initialize the QA chain with Ollama
        llm = OllamaLLM(model=self.model_name, temperature=0.1)
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectorstore.vectorstore.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        # Run the query
        result = self.qa_chain.invoke({"query": question})
        
        # Display source documents (files being used for context)
        if "source_documents" in result and result["source_documents"]:
            print("\n===============")
            print("\nFiles being used as context:")
            for doc in result["source_documents"]:
                print(f"- {doc.metadata.get('source', 'Unknown source')}")
            print("\n===============\n")
        else:
            print("No source documents found for this query.")
            
        return result["result"]
        
    def generate_constitution(self, prompt: str) -> str:
        """
        Generate a new constitution-style document based on the prompt.
        
        Args:
            prompt (str): Prompt describing what kind of constitution to create
            
        Returns:
            str: Generated constitution text
        """
        # Create a more specific prompt for constitution generation
        generation_prompt = f"""
        You are an expert constitutional writer. Using the principles and content from the provided constitutional documents,
        write a new constitution that follows this guidance: {prompt}
        
        Ensure your response is in proper constitutional format with:
        1. Preamble
        2. Articles
        3. Amendments process
        4. Rights and freedoms
        5. Government structure
        
        Use language and concepts appropriate for a modern constitution.
        """
        
        # Use the query method to get relevant context and then generate
        return self.query(generation_prompt)

if __name__ == "__main__":
    # Example usage - this is just for testing imports
    print("RAG system initialized successfully!")