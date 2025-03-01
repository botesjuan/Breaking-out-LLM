import requests
import json

# Define API endpoints
OLLAMA_CHAT_URL = "http://192.168.255.57:11434/api/chat"
MIDDLEWARE_API_URL = "http://192.168.255.57:5001/execute"

# Function to prompt user for input
def get_user_input():
    print("\n📝 Enter a command request (e.g., 'List all files in /etc'): ")
    user_request = input("> ").strip()
    return user_request if user_request else None

# Step 1: Query the LLM to generate a bash command payload
def get_llm_generated_command(user_request):
    payload = {
        "model": "llama3",  # Change this to your actual model
        "messages": [
            {
                "role": "user",
                "content": f"Format the following as a JSON payload: {{ 'command': '<bash_command>' }} "
                           f"based on this request: '{user_request}'"
            }
        ],
        "stream": False
    }
    
    try:
        print("\n📡 Sending request to Ollama LLM...\n")
        response = requests.post(OLLAMA_CHAT_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Extract response text
        generated_text = data.get("message", {}).get("content", "").strip()

        # Extract JSON from LLM output
        json_start = generated_text.find("{")
        json_end = generated_text.rfind("}") + 1
        if json_start != -1 and json_end != -1:
            extracted_json = generated_text[json_start:json_end]
            command_payload = json.loads(extracted_json)

            print("\n✅ LLM Generated Command Payload:\n")
            print(json.dumps(command_payload, indent=4, sort_keys=True))  # Pretty-print JSON output
            return command_payload
        else:
            print("\n❌ Error: LLM response does not contain valid JSON.\n")
            return None

    except requests.RequestException as e:
        print(f"\n🚨 Error communicating with Ollama API: {e}\n")
        return None

# Step 2: Send the extracted command to the middleware API
def execute_command_on_middleware(command_payload):
    try:
        print("\n📡 Sending extracted command to Middleware API...\n")
        response = requests.post(MIDDLEWARE_API_URL, json=command_payload)
        response.raise_for_status()
        api_response = response.json()

        print("\n✅ Middleware API Response (Formatted Output):\n")
        print_pretty_output(api_response)

        return api_response

    except requests.RequestException as e:
        print(f"\n🚨 Error executing command on middleware API: {e}\n")
        return None

# Function to format the output for better readability
def print_pretty_output(api_response):
    if isinstance(api_response, dict):  # Check if response is a JSON object
        print(json.dumps(api_response, indent=4, sort_keys=True))
    elif isinstance(api_response, str):  # If response is plain text, format it
        print("\n".join(["  " + line for line in api_response.strip().split("\n")]))
    else:
        print("⚠️ Unexpected response format received.")

# Main execution flow
if __name__ == "__main__":
    print("\n🚀 **Automated LLM Command Execution Started** 🚀\n")
    
    user_request = get_user_input()
    
    if user_request:
        command_payload = get_llm_generated_command(user_request)
        
        if command_payload:
            execution_response = execute_command_on_middleware(command_payload)
            
            if execution_response:
                print("\n🎯 **Execution Completed Successfully!** 🎯\n")
            else:
                print("\n⚠️ **Execution Failed at Middleware API Stage.**\n")
        else:
            print("\n⚠️ **LLM Did Not Generate a Valid Command.**\n")
    else:
        print("\n⚠️ **No user input provided. Exiting.**\n")

    print("\n✅ **Process Completed.**\n")
