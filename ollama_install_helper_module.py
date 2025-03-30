
#Importing the libraries.
import subprocess
import os 

def run_commands(commands):
    """ Function for executing list of shell of commands.

    Args:
    =====
    commands: The list of shell commands.
    """
    #Iterate through list of comamnds.
    for command in commands:
        #Execute shell commands and captures shell output and error.
        with subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=1) as sp:
            #Reads the output line by line.
            for line in sp.stdout:
                #Decodes each line and converts it into string from bytes.
                line=line.decode('UTF-8',errors='replace')
                #Checks if the output contains "undefined_reference" indicating a failure,
                if "undefined_reference" in line:
                    raise RuntimeError("Failed Processing..")
                print(line,flush = True,end="")

