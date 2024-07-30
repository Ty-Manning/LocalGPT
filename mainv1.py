from flask import Flask, jsonify, request, Response, render_template, stream_with_context
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
history_file = 'chat_history.json'

def load_history():
    """Load chat history from the JSON file."""
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            return json.load(f)
    return []

def save_history(message):
    """Append a message to the chat history file."""
    history = load_history()
    history.append(message)
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=4)
    print(f"History saved: {message}")  # Debug print

def clear_history_file():
    """Clear the chat history file."""
    if os.path.exists(history_file):
        os.remove(history_file)
        print("History file cleared")  # Debug print

@app.route('/')
def index():
    """Render the HTML page."""
    return render_template('index.html')

@app.route('/v1/stream/chat', methods=['POST'])
def streamed_chat():
    @stream_with_context
    def generate():
        data = request.get_json()
        model = data['model']
        user_message = data['messages'][0]  # The new user message

        # Load chat history and add the new user message
        chat_history = load_history()
        chat_history.append(user_message)

        url = "http://localhost:11434/api/chat"  # Local Ollama API endpoint URL 
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            'model': model,
            'messages': chat_history
        }
        response = requests.post(url, json=payload, headers=headers, stream=True)

        accumulated_response = ''
        
        for chunk in response.iter_lines():
            if chunk:
                try:
                    # Decode the chunk and load as JSON
                    chunk_data = json.loads(chunk.decode('utf-8'))
                    
                    # Extract the 'content' and 'done' fields
                    response_content = chunk_data.get('message', {}).get('content', '')
                    done = chunk_data.get('done', False)
                    
                    # Accumulate the response
                    accumulated_response += response_content
                    
                    # Yield the accumulated response in SSE format
                    yield f"data:  {json.dumps({'role': 'assistant', 'response': accumulated_response, 'done': done})}\n\n"
                    
                    # Break out of the loop if 'done' is True
                    if done:
                        # Save user message and assistant response to history file
                        save_history({'role': 'user', 'content': user_message.get('content')})
                        save_history({'role': 'assistant', 'content': accumulated_response})
                except json.JSONDecodeError:
                    continue

    return Response(generate(), mimetype='text/event-stream')

@app.route('/v1/models', methods=['GET'])
def get_models():
    """Return the list of models."""
    return jsonify({
        "status": "success",
        "message": "Models retrieved successfully",
        "data": ["qwen2", "llama3", "llama2-uncensored"]
    })

@app.route('/v1/clear_history', methods=['POST'])
def clear_history():
    """Clear chat history."""
    clear_history_file()
    return jsonify({
        "status": "success",
        "message": "Chat history cleared",
        "data": {"history": []}
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)