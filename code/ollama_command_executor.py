from flask import Flask, request, jsonify
import subprocess
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/execute', methods=['POST'])
def execute_command():
    try:
        data = request.get_json()
        if not data or 'command' not in data:
            logging.warning("Received request with missing 'command' key")
            return jsonify({"error": "Missing 'command' key in request"}), 400
        
        command = data['command']
        logging.info(f"Received command: {command}")
        
        # Execute the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            output = result.stdout.strip()
            logging.info(f"Command executed successfully: {output}")
        else:
            output = result.stderr.strip()
            logging.error(f"Command execution failed: {output}")
        
        return jsonify({"output": output, "return_code": result.returncode})
    except Exception as e:
        logging.exception("Unexpected error occurred")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logging.info("Starting Middleware on port 5001...")
    app.run(host='0.0.0.0', port=5001, debug=True)