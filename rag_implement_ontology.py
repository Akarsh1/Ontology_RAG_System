
### Importing libraries
import requests
import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize
import re
import os
import subprocess
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# The LLM Model (Using LLAMA 3)
model = 'llama3.1:8b-instruct-q8_0'


def clean_text(text):
    """Cleans raw text from books by removing unwanted content.
    
    Args:
    ======
    text: The text to be cleaned.

    Return
    ======
    text: The cleaned text.

    """
    
    # Remove extra spaces, newlines, and tabs
    text = re.sub(r'\s+', ' ', text)

    # Remove special characters such as emojis, unwanted characters and converts into single space.
    text = re.sub(r'[^a-zA-Z0-9.,?!\'" ]+', ' ', text)

    # Fix hyphenated words that occur at line breaks (e.g., "deep-\nlearning" → "deep learning")
    text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)

    # Normalize spaces again
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def load_text(url):
    """ Loads the text from the url, cleans it and outputs it into chunks.
    Args:
    ====
    url: The full path of the book.

    Return:
    ======
    split_into_sentences(): Function that will split the text into chunks.
    
    """
    try:
        #Download text of the book from the given url.
        response = requests.get(url)
        # Raise error if url in unvalid
        response.raise_for_status()
        # Removes leading and trailing spaces in response text.
        text = response.text.strip()
        # cleans the text
        cleaned_text = clean_text(text)
        
        def split_into_sentences(text,chunk_size=10):
            """ Splitting the text into chunk of sentences
            
            Args:
            ====

            text: The cleaned text to be chunked into sentences.
            chunk_size = The number of sentence a chunk can hold.
            
            """
            #Splits the text using NLTK sentence tokenizer.
            sentences = sent_tokenize(text)
            #Return the list of text chunks of chunk_size.
            return [" ".join(sentences[i:i+chunk_size]) for i in range(0,len(sentences),chunk_size)]

        return split_into_sentences(cleaned_text,chunk_size=10)

    # For error encountered during downloading file.
    except requests.exceptions.RequestException as e:
        st.error(f"Error downloading file: {e}")
        return []

def generate_ontology(text_chunks):
    """ Generate ontologies from the text chunks 
    Args:
    ====
    text_chunks: The text chunks for which ontologies to be generated.

    Return:
    =======
    ontology: The dictionary of ontologies for the text chunks.
    
    """
    # The dictionary of key concepts and relations.
    ontology = {}
    # Enumerate for each text_chunks.
    for i, doc in enumerate(text_chunks):
        # Prompt for extracting key and relationship.
        prompt = f"Extract key concepts and relationships from the following text:\n\n{doc}"
        # Use Ollama to run Llama 3 with the prompt
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True, #capture the output.
            text=True # Returned Output as string.
        )
        # Removes spaces in output given by llm.
        response = result.stdout.strip()
        #Store the output in dictionary.
        ontology[f"chunk_{i}"] = response
        
    return ontology


def store_ontology(ontology):
    """ Store the ontologoes in a FAISS vector db for efficient retrieval.

    Args:
    ====
    ontology: Dictionary of ontologies.

    Return:
    ======
    index: Faiss index containing embeddings for retrieva.
    texts: List of ontology dictionary values.
    embedding_model: The embedding model.
    """
    #Initializing the embedding model.
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    # Converting ontology dictionary values in list.
    texts = list(ontology.values())
    #Comverts texts to numerical numerical vector embeddings using embedding model
    embeddings = embedding_model.encode(texts,convert_to_numpy=True)
    # Retrieves nunber of features in the embedding vector.
    dimension = embeddings.shape[1]
    # Creates a faiss index using euclidean distance for similarity search.
    index = faiss.IndexFlatL2(dimension)
    #Adds the embeddings into the faiss index for retreival.
    index.add(embeddings)

    return index,texts,embedding_model
    

def answer_question(query, index, texts,embedding_model):
    """ Retrieve relevant information from faiss index and generates answers using Llama 3.

    Args:
    ====
    query: The query or question.
    index: Faiss index containing embeddings for retrieva.
    texts: List of ontology dictionary values.
    embedding_model: The embedding model.

    Return:
    ======
    response: The answer generated by the LLM.
    
    """
    # Embed the query and convert to numerical representation.
    query_embedding = embedding_model.encode([query], convert_to_numpy=True)
    # Search the FAISS index for 5 most similar embeddigs to query embeddings.
    distances, indices = index.search(query_embedding, k=5)
    
    # Retrieve the most relevant texts
    retrieved_texts = [texts[idx] for idx in indices[0]]
    #Joins the retrived text with double new lines to form cohrent text.
    context = "\n\n".join(retrieved_texts)
    
    # Formulate the prompt for Llama 3
    prompt = f"Using the following context, answer the question:\n\nContext:\n{context}\n\nQuestion:\n{query}"
    
    # Use Ollama to run Llama 2 with the prompt
    result = subprocess.run(
        ["ollama", "run", model, prompt],
        capture_output=True,
        text=True
    )
    # Removes spaces in output given by llm.
    response = result.stdout.strip()
    return response
