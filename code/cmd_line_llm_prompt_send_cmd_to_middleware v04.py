import requests
import json
import re

# Define API endpoints
OLLAMA_CHAT_API = "http://192.168.255.57:11434/api/chat"
MIDDLEWARE_API = "http://192.168.255.57:5001/execute"

# Function to query LLM for a security-related command
def get_llm_generated_command(target, user_request):
    """Requests a properly formatted command from the LLM, ensuring the target is included."""
    prompt_content = (
        f"Generate a JSON payload for a security assessment command targeting {target}. "
        f"The JSON format should be: {{ 'command': '<bash_command>' }}. "
        f"Ensure the command explicitly includes {target} as the target. "
        f"User's security request: '{user_request}'."
    )

    payload = {
        "model": "llama3",
        "messages": [{"role": "user", "content": prompt_content}],
        "stream": False
    }

    try:
        print("\n📡 Sending request to Ollama LLM...\n")
        response = requests.post(OLLAMA_CHAT_API, json=payload)
        response.raise_for_status()
        data = response.json()

        generated_text = data.get("message", {}).get("content", "").strip()

        # Extract JSON from response using regex
        match = re.search(r"\{.*?\}", generated_text, re.DOTALL)
        if match:
            command_payload = json.loads(match.group(0))
            print("\n✅ LLM Generated Command Payload:\n", json.dumps(command_payload, indent=4, sort_keys=True))
            return command_payload
        else:
            print("\n❌ Error: LLM response does not contain valid JSON.\n")
            return None

    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"\n🚨 Error in LLM command generation: {e}\n")
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
    """Requests an explanation from the LLM for the command output."""
    payload = {
        "model": "llama3",
        "messages": [
            {
                "role": "user",
                "content": f"Explain the security implications of the following results:\n{json.dumps(api_response, indent=4)}"
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
def get_next_security_command(api_response, target):
    """Requests the next logical security assessment command from the LLM, ensuring the target is included."""
    payload = {
        "model": "llama3",
        "messages": [
            {
                "role": "user",
                "content": f"Based on the security assessment results, suggest the next command to further analyze the target {target}. "
                           f"The response should be in strict JSON format with double quotes: {{ \"command\": \"<bash_command>\" }}.\n"
                           f"Do NOT include any text outside the JSON response.\n\n{json.dumps(api_response, indent=4)}"
            }
        ],
        "stream": False
    }

    try:
        print("\n📡 Asking Ollama LLM for next suggested command...\n")
        response = requests.post(OLLAMA_CHAT_API, json=payload)
        response.raise_for_status()
        data = response.json()

        # Extract JSON strictly
        generated_text = data.get("message", {}).get("content", "").strip()
        match = re.search(r"\{.*?\}", generated_text, re.DOTALL)

        if match:
            json_str = match.group(0)
            try:
                suggested_command = json.loads(json_str)
                print("\n🔍 Suggested Next Command:\n", json.dumps(suggested_command, indent=4, sort_keys=True))
                return suggested_command
            except json.JSONDecodeError as e:
                print(f"\n🚨 JSON decoding error: {e}\nRaw LLM response:\n{generated_text}\n")
                return None
        else:
            print("\n⚠️ No valid JSON found in LLM response. Raw response:\n", generated_text)
            return None

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
    
    target = input("\n🎯 Enter the target IP or domain for security assessment: ").strip()
    if not target:
        print("\n⚠️ No valid target entered. Exiting...\n")
        exit()

    user_request = input("\n📝 Enter the initial security command request (e.g., 'List open ports'): ").strip()

    while True:
        command_payload = get_llm_generated_command(target, user_request)
        
        if command_payload:
            execution_response = execute_command_on_middleware(command_payload)
            
            if execution_response:
                get_llm_explanation(execution_response)

                suggested_command = get_next_security_command(execution_response, target)

                if suggested_command:
                    print("\n🔄 Do you want to execute the suggested command? (yes/no/exit)")
                    user_choice = input("> ").strip().lower()

                    if user_choice == "yes":
                        user_request = suggested_command['command']
                        continue  # Skip user input and continue execution
                    elif user_choice == "no":
                        user_request = input("\n📝 Enter your own next security command: ").strip()
                    elif user_choice == "exit":
                        print("\n👋 Exiting security assessment loop...\n")
                        break
                else:
                    print("\n⚠️ No valid next command suggested. Please enter a new command manually.")
                    user_request = input("\n📝 Enter a security command: ").strip()
            else:
                print("\n⚠️ **Execution Failed at Middleware API Stage.**\n")
                user_request = input("\n📝 Enter a new security command: ").strip()
        else:
            print("\n⚠️ **LLM Did Not Generate a Valid Command.**\n")
            user_request = input("\n📝 Enter a new security command: ").strip()

    print("\n✅ **Process Completed.**\n")
