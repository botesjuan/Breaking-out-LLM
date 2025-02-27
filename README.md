# Breaking-out-LLM  

>My work in progress notes as my knowledge expand while doing research and learning to build my objective.  
>Breaking out of LLM constrains and build AI Task Assistant to perform interactive security assessment.  
  
<img src="/images/jail.png" width=250 height=200>

>The research and learnings I am document here is to build an `AI` assistant that performs authorized penetration testing tasks by running commands and tools against a target and reviewing output from said tools to perform additional activities based on results and document artifacts.  

<img src="/images/break-glass.png" width=250 height=200>

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

## Design  

>Integration of LLM, Ollama, WebUI, Middleware API, host instructions:  

![breakout llm design jail](/images/breakout-llm-design.png)  

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

>Set the docker instance for Ollama-WebUI to auto start the container after Ubuntu boot:  

```
sudo docker run -d --restart unless-stopped -p 3000:8080 --name open-webui ghcr.io/open-webui/open-webui:main
```  

>Docker instance of Open WebUI: `http://127.0.0.1:3000/`  
>Connected to Ollama local instance: `http://192.168.255.57:11434`  

## Large Language Model LLM  

>`Deepseek R1` LLM that provide the inital interactive input, is not an `Agentic` Model  

>Ollama API get Models Downloaded locally: `http://192.168.255.57:11434/api/tags`  

>Agentic Model testing: ``  

## Integration Authorization  

>Protect access control what services may interact with Middleware API, to prevent unauthorized access from rogue actors.

## Middleware API  

>Develop API integration with the input prompt, the LLM must perform the security actitivity by running local bash commands on Ubuntu.  

>Path Python API Script: `/home/peanut/Downloads/breakout_api`  

>Start API: `python3 ollama_command_executor.py`  
>Running on `http://0.0.0.0:5001`  

>The Ollama LLM is processing the text based input from user but does not inherently send HTTP requests.
>The Ollama WebUI frontend running in docker sends user queries to the local Ollama instance,  
>and if Ollama is instructed to execute commands via the middleware, the WebUI must generate the and send HTTP POST requests.  

### Troubleshooting Integration  

>Communication and permissions between docker WebUI and localhost Middleware on port 5001.  

```
sudo docker exec -it open-webui bash
curl -X POST http://192.168.255.57:5001/execute -H "Content-Type: application/json" -d '{"command":"ls -al /home"}'
```  

>Above will test if the docker instance bash shell have permissions to execute and reach the middleware API running on localhost port 5001.  


## Import Results from Tasks  

>The Output from the commands executed must be imported into the LLM chat input as results and then analysed to produce next steps to execute.  

## Loop Methodology  

>Penetration Testing methodology.  
>The LLM must continue until it needs more input from the human security analyst and guidenance if stuck.  

## Record Artifacts  

>Results must be saved and records as evidence that will be put into document, screenshots taken as part of evendice.  

## Screenshots Evidence   

>Screenshots must include dates for timeline and logging.  

## Training & Enhance  

>LLM trained on personal data sets on security methodology documentation containing example commands and results to enhance the LLM knowledge base.  

----  

>Status: Inprogress research since: January 2025  
  
