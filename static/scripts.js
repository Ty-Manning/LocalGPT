// Define the local IP address at the top of the file
const local_ip = 'http://76.30.77.113:5000';

// Function to send a message to the server
async function sendMessage() {
    const message = document.getElementById('input').value;
    const model = document.getElementById('model').value;
    const responseDiv = document.getElementById('response');
    const apiVersion = "v1";

    try {
        // Send a POST request to initiate streaming
        const response = await fetch(`${local_ip}/${apiVersion}/stream/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: model,
                messages: [
                    { role: 'user', content: message }
                ]
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Read and process the streaming response
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let accumulatedData = '';
        let responseStarted = false;

        // Create a new div for the current chat response
        const newChatDiv = document.createElement('div');
        responseDiv.insertBefore(newChatDiv, responseDiv.firstChild); // Insert at the top

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            // Process each chunk of data
            const chunk = decoder.decode(value, { stream: true });
            chunk.split('\n\n').forEach(line => {
                if (line.trim()) {
                    try {
                        const data = JSON.parse(line.replace(/^data: /, ''));
                        if (data.response) {
                            accumulatedData = data.response;
                            // Append the accumulated data to the newChatDiv
                            newChatDiv.innerHTML = `<p><strong>Response:</strong> ${accumulatedData}</p>`;
                        }

                        if (data.done) {
                            // Mark response as complete
                            responseStarted = false;
                            return; // Exit the loop and function
                        }
                    } catch (e) {
                        console.error('Error parsing JSON:', e);
                    }
                }
            });
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

// Function to clear chat history and clear the chat window
async function clearHistory() {
    const responseDiv = document.getElementById('response');

    try {
        const response = await fetch(`${local_ip}/v1/clear_history`, {
            method: 'POST'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Clear chat window
        responseDiv.innerHTML = '';

        console.log('Chat history cleared');
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

// Function to get the list of models from the server
async function getModels() {
    try {
        const response = await fetch(`${local_ip}/v1/models`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        const modelSelect = document.getElementById('model');
        modelSelect.innerHTML = data.data.map(model => `<option value="${model}">${model}</option>`).join('');
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

// Initialize the page by loading the models
window.onload = getModels;
