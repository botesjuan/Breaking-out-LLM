# Breaking-out-LLM  

>Breaking out of LLM constrains and build AI Task Assistant to perform interactive security assessment.  
  
<img src="/images/jail.png" width=250 height=200>

>The research and learnings I am document here is to build an `AI` assistant that performs authorized penetration testing tasks by running commands and tools against a target and reviewing output from said tools to perform additional activities based on results and document artifacts.  

![Break the glasss Emergency](/images/break-glass.png)  

----  

## Objectives  

1. Create private secure local LLM running Ollama that is running on personal Ubuntu host.  
2. Start with LLM that provide the inital interactive input.  
3. Based on the input prompt, the LLM must perform the security actitivity by running local bash commands on Ubuntu.
4. The Output from the commands executed must be imported into the LLM chat input as results and then analysed to produce next steps to execute.
5. The LLM must continue until it needs more input from the human security analyst and guidenance if stuck.
6. Results must be saved and records as evidence that will be put into document, screenshots taken as part of evendice. 
7. Screenshots must include dates for timeline and logging.
8. LLM trained on security methodology documentation containing example commands and results to enhance the logic flow.  

## Constrains  

>This research is constrained by the available resources and funding to test performance.
>This proof of concept (POC) is to validate the execution functionality, results and not the speed.  

----  

## Setup  

>Physical Hardware and OS:  

- Ubuntu 24.04.2
- Architecture 64-bit
- CPU AMD Ryzen 5 2600 
- CPU's 12
- GPU Nvidia GeForce RTX 4060 Ti with 16 GB onboard memory 
- Onboard memory 32 GB 

>Local Ollama installed `http://0.0.0.0:11434`  

>Configuration altered to allow Ollama to be reachable from all local interfaces edit:  

```
sudo systemctl edit --full ollama
```  

## Large Language Model LLM  

>`Deepseek R1` LLM that provide the inital interactive input.  

## Agent API  

>Develop API integration with the input prompt, the LLM must perform the security actitivity by running local bash commands on Ubuntu.

## Import Results from Tasks  

>The Output from the commands executed must be imported into the LLM chat input as results and then analysed to produce next steps to execute.  

## Loop Methodology  

>Penetration Testing methodology.  
>The LLM must continue until it needs more input from the human security analyst and guidenance if stuck.  

## Record Artifacts  

>Results must be saved and records as evidence that will be put into document, screenshots taken as part of evendice.  

## Take Screenshots as part of Artifacts  

>Screenshots must include dates for timeline and logging.  

## Training & Enhance  

>LLM trained on security methodology documentation containing example commands and results to enhance the logic flow.  

----  

>Status: Inprogress research since: January 2025  
  