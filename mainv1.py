from flask import Flask, jsonify, request, Response, render_template
from flask_cors import CORS
import requests
import ollama  

app = Flask(__name__) 
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
chat_history = []  # This will store chat history

@app.route('/') 
def index():  
    return render_template('index.html')  # Renders the HTML
@app.route('/v1/stream/chat', methods=['POST'])
def streamed_chat():
    def generate():
        data = request.get_json()  
        model = data['model']  
        prompt = data['prompt']
        
        url = "http://localhost:11434/api/generate"  # Local Ollama API endpoint URL
        headers = {
            "Content-Type": "application/json",
        }
        response = requests.post(url, json={'model': model, 'prompt': prompt}, headers=headers, stream=True)  
        
        for chunk in response.iter_lines():
            if chunk:
                yield f"data: {chunk.decode('utf-8')}\n\n"
                
    return Response(generate(), mimetype='text/event-stream')

@app.route('/v1/models', methods=['GET'])
def get_models():
    return jsonify({
        "status": "success",
        "message": "Models retrieved successfully",
        "data": ["qwen2", "llama3"]
    })

@app.route('/v1/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data['message']
        
        response = ollama.chat(model=data['model'], messages=[
            {'role': 'user', 'content': message},
        ])
        result = response['message']['content']

        return jsonify({
            "status": "success",
            "message": "Response from model",
            "data": {
                "model": data['model'],
                "response": result
            }
        })
    except Exception as e:
        return jsonify({
             "status": "error",
             "message": str(e)
        })

@app.route('/v1/history', methods=['POST'])
def history():
    data = request.get_json()
    chat_history.append({"role": "system", "content": data['message']})
    return jsonify({
        "status": "success",
        "message": "Message saved to chat history",
        "data": {"history": chat_history}
    })

@app.route('/v1/clear_history', methods=['POST'])
def clear_history():
    chat_history.clear()
    return jsonify({
        "status": "success",
        "message": "Chat history cleared",
        "data": {"history": chat_history}
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
