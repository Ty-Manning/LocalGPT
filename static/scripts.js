// Define the local IP address at the top of the file
const local_ip = 'http://10.0.0.135:5000';

// Function to send a message to the server
async function sendMessage() {
    const message = document.getElementById('input').value;
    const model = document.getElementById('model').value;
    const responseDiv = document.getElementById('response');
    const apiVersion = "v1";

    const body = JSON.stringify({ model, message });
    const response = await fetch(`${local_ip}/${apiVersion}/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: body
    });

    const data = await response.json();
    if (data.status === "success") {
        const p = document.createElement("p");
        p.appendChild(document.createTextNode(`Response: ${data.data.response}`));
        responseDiv.appendChild(p);
    } else {
        console.error('Error:', data.message);
    }
}

// Function to get the list of models from the server
async function getModels() {
    const response = await fetch(`${local_ip}/v1/models`);
    const data = await response.json();
    const modelSelect = document.getElementById('model');
    modelSelect.innerHTML = data.data.map(model => `<option value="${model}">${model}</option>`).join('');
}

// Initialize the page by loading the models
window.onload = getModels;
