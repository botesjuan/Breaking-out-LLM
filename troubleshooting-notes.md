# Troubleshooting Notes  

My local LLM agentic setup consist of the following:

1. Ollama instance on Ubuntu 24 host
2. WebUI in docker container
3. Python middleware API accepting POST requests and executing bash commands on the local Ubuntu 24 host.
4. Downloaded various LLM models in Ollama

Successful Test results:

1. Ollama instance running on http://192.168.255.57:11434 accessible
2. WebUI http://127.0.0.1:3000 accessable from localhost.
3. WebUI admin settings connected to the Ollama instance from docker
4. Python middleware API running and accessable at http://192.168.255.57:5001/request
5. Sending Curl POST request from docker WebUI bash shell to http://192.168.255.57:5001/request successfully execute the bash command on local Ubuntu host.

Failed Test Cases:

1. Sending context prompt via WebUI to different LLM loaded models, that it should use http://192.168.255.57:5001/request to POST command requests fail
2. TCPdump on localhost Ubuntu fail to intercept any traffic from WebUI to the middleware API python service.
3. Change the LLM in the WebUI prompt to use have no effect and no success in sending POST request to middleware API at http://192.168.255.57:5001/request

What must I change in my design architecture to achieve interactive prompts that execute bash commands on the Ubuntu localhost? 
