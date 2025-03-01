import requests
import json
import re

# Define API endpoints
OLLAMA_CHAT_API = "http://192.168.255.57:11434/api/chat"
MIDDLEWARE_API = "http://192.168.255.57:5001/execute"

# Function to query LLM for a security-related command
def get_llm_generated_command(user_request):
    payload = {
        "model": "llama3",
        "messages": [
            {
                "role": "user",
                "content": f"Format the following as a JSON payload: {{ 'command': '<bash_command>' }} "
                           f"based on this security assessment request: '{user_request}'"
            }
        ],
        "stream": False
    }

    try:
        print("\n📡 Sending request to Ollama LLM...\n")
        response = requests.post(OLLAMA_CHAT_API, json=payload)
        response.raise_for_status()
        data = response.json()

        generated_text = data.get("message", {}).get("content", "").strip()

        json_start = generated_text.find("{")
        json_end = generated_text.rfind("}") + 1
        if json_start != -1 and json_end != -1:
            extracted_json = generated_text[json_start:json_end]
            command_payload = json.loads(extracted_json)

            print("\n✅ LLM Generated Command Payload:\n")
            print(json.dumps(command_payload, indent=4, sort_keys=True))
            return command_payload
        else:
            print("\n❌ Error: LLM response does not contain valid JSON.\n")
            return None

    except requests.RequestException as e:
        print(f"\n🚨 Error communicating with Ollama API: {e}\n")
        return None

# Function to execute a command on middleware API
def execute_command_on_middleware(command_payload):
    try:
        print("\n📡 Sending extracted command to Middleware API...\n")
        response = requests.post(MIDDLEWARE_API, json=command_payload)
        response.raise_for_status()
        api_response = response.json()

        print("\n✅ Middleware API Response (Formatted Output):\n")
        print_pretty_output(api_response)

        return api_response

    except requests.RequestException as e:
        print(f"\n🚨 Error executing command on middleware API: {e}\n")
        return None

# Function to interpret results using LLM
def get_llm_explanation(api_response):
    payload = {
        "model": "llama3",
        "messages": [
            {
                "role": "user",
                "content": f"Explain the results returned, not the formatting, but rather give info about what each data line represents:\n{json.dumps(api_response, indent=4)}"
            }
        ],
        "stream": False
    }

    try:
        print("\n📡 Asking Ollama LLM for explanation of results...\n")
        response = requests.post(OLLAMA_CHAT_API, json=payload)
        response.raise_for_status()
        data = response.json()

        explanation = data.get("message", {}).get("content", "").strip()
        
        print("\n📝 LLM Explanation of Results:\n")
        print(explanation)

        return explanation

    except requests.RequestException as e:
        print(f"\n🚨 Error getting explanation from Ollama API: {e}\n")
        return None

# Function to get next suggested security command
def get_next_security_command(api_response):
    payload = {
        "model": "llama3",
        "messages": [
            {
                "role": "user",
                "content": f"Based on the following security assessment results, suggest the next command to further analyze the target:\n{json.dumps(api_response, indent=4)}"
            }
        ],
        "stream": False
    }

    try:
        print("\n📡 Asking Ollama LLM for next suggested command...\n")
        response = requests.post(OLLAMA_CHAT_API, json=payload)
        response.raise_for_status()
        data = response.json()

        suggested_command = data.get("message", {}).get("content", "").strip()
        
        print("\n🔍 Suggested Next Command:\n", suggested_command)

        return suggested_command

    except requests.RequestException as e:
        print(f"\n🚨 Error getting next command suggestion from Ollama API: {e}\n")
        return None

# Function to format and display structured output
def print_pretty_output(api_response):
    if isinstance(api_response, dict):
        print(json.dumps(api_response, indent=4, sort_keys=True))
    elif isinstance(api_response, str):
        print("\n".join(["  " + line for line in api_response.strip().split("\n")]))
    else:
        print("⚠️ Unexpected response format received.")

# Main execution loop
if __name__ == "__main__":
    print("\n🚀 **Automated LLM Security Assessment Started** 🚀\n")
    
    user_request = input("\n📝 Enter the initial security command request (e.g., 'List open ports'): ").strip()

    while True:
        # Step 1: Get LLM-generated command
        command_payload = get_llm_generated_command(user_request)
        
        if command_payload:
            # Step 2: Execute command
            execution_response = execute_command_on_middleware(command_payload)
            
            if execution_response:
                # Step 3: Get explanation of results
                get_llm_explanation(execution_response)

                # Step 4: Get next suggested command
                suggested_command = get_next_security_command(execution_response)

                if suggested_command:
                    print("\n🔄 Do you want to execute the suggested command? (yes/no/exit)")
                    user_choice = input("> ").strip().lower()

                    if user_choice == "yes":
                        user_request = suggested_command  # Use the suggested command directly
                        continue  # Skip user input and continue execution
                    elif user_choice == "no":
                        user_request = input("\n📝 Enter your own next security command: ").strip()
                    elif user_choice == "exit":
                        print("\n👋 Exiting security assessment loop...\n")
                        break
                else:
                    print("\n⚠️ No next command suggested. Please enter a new command manually.")
                    user_request = input("\n📝 Enter a security command: ").strip()
            else:
                print("\n⚠️ **Execution Failed at Middleware API Stage.**\n")
                user_request = input("\n📝 Enter a new security command: ").strip()
        else:
            print("\n⚠️ **LLM Did Not Generate a Valid Command.**\n")
            user_request = input("\n📝 Enter a new security command: ").strip()

    print("\n✅ **Process Completed.**\n")
