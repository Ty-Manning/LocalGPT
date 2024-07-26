async function sendMessage() {
    const message = document.getElementById('input').value;
    const model = document.getElementById('model').value;
    const responseDiv = document.getElementById('response');
    const apiVersion = "v1";

    const body = JSON.stringify({ model, message });
    const response = await fetch(`http://localhost:5000/${apiVersion}/chat`, {
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

async function getModels() {
    const response = await fetch('http://localhost:5000/v1/models');
    const data = await response.json();
    const modelSelect = document.getElementById('model');
    modelSelect.innerHTML = data.data.map(model => `<option value="${model}">${model}</option>`).join('');
}

window.onload = getModels;
