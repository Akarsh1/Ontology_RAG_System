# Ontology Creation and Gneneration using RAG.

#### Details of the files in the project:

1. setup.sh: This is the bash file or the main file that executes the entire project.
2. rag_implement_ontology.py: This python file contains functions such as text splitting, ontology generation, storing text in vector store and retrieving data for 
   implementing RAG application.
3. npm_requirements.txt: This txt file contains library for hosting the strealit app. In my case, it is localtunnel.
4. ollama_install_helper_module.py: This python file contains function used for executing terminal commands.
5. requirements.txt: This txt file contains libraries used in the project.
6. app.py: This python file contains the code for UI using streamlit.

**Steps to run the project:**

1. Execute the main bash file(setup.sh) in the terminal using the following command:
   
    <code>bash setup.sh</code>
   
   This will install all the dependencies in requirements.txt , npm_requirements.txt and Ollama. Further, it will also run the streamlit app via localtunnel server     and generate the link where the streamlit is 
   hosted.
   
   ```Note: The installation can take some time. Further, it will also take time to generate ontologies for the text chunks depending on the GPU.```
   
2. During execution of the setup.sh script, the local tunnel password will be generated.
   
     Example: Password: 25.21.14.0
   
     Copy this password and go to the link generated by the local tunnel strealit server as shown in the image.
   
     ![428423659-cde3e3e6-e00d-4d82-89bc-20f101b9ad80](https://github.com/user-attachments/assets/0e7c9626-b288-4c5d-b447-6ada52d836ce)

   
3. After clicking on the link, paste the password and proceed. The streamlit app opens and lets you interact with the application.

   ![image](https://github.com/user-attachments/assets/89574ef9-d1ca-4367-8312-345e66d329ee)

   ![image](https://github.com/user-attachments/assets/56b618b1-90c9-4bc2-a5a7-8911c7003f3b)


   
