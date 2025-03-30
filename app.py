
#Importing libraries and python module.
import streamlit as st
#Using functions from rag_implement_intology
from rag_implement_ontology import *

def main():
    #Title off the app
    st.title("Ontology-Based RAG System")
    url = st.text_input("Enter the URL of the text File: ")
    if url:
        st.write("Fetching and Processing Text....")
        text_chunks = load_text(url)
    
        st.write("Genertaing ontology...")
        ontology = generate_ontology(text_chunks)
    
        st.write("Storing Ontologies in a vector DB..")
        index, texts, embedding_model = store_ontology(ontology)
        
        st.success("The knowledge base has been processed successfully. You can now ask questions.")
    
        # Question input
        user_query = st.text_input("Enter your question:")
    
        if user_query:
            st.write("Retrieving answer...")
            #The answer of the user question.
            answer = answer_question(user_query, index, texts,embedding_model)
            st.write("Answer:", answer)
            
if __name__ == '__main__':
    main()
