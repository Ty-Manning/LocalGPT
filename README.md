# LocalGPT

LocalGPT is a web application that serves a local Large Language Model (LLM) using a Flask API. It interacts with the Ollama Python libraries and API to provide language processing capabilities.
**This project REQUIRES Ollama installed and running on your system. You must have at least one model installed. Place that model name in the API endpoint for models. Currently the models are hardcoded.**

## Project Structure


- `mainv1.py`: The main Flask application file and API.
- `templates/index.html`: The HTML for the web application.
- `static/scripts.js`: JavaScript file for handling client-side interactions.

## Features

- **Flask API**: Provides an interface for interacting with the local LLM.
- **Ollama Integration**: Uses Ollama Python libraries and API for language model functionality.
- **Real-Time Streaming**: Supports streaming responses in real-time from the LLM
## Models

- Default models: "qwen2" and "llama3". These models can be changed as needed.
- As stated before, currently these models are hardcoded in the `mainv1.py` in the /v1/models endpoint. I intend to change this.

## Disclaimer

**WARNING:** This project is intended for development, testing, and education purposes only. It should not be used in a production environment.

## Installation

1. Clone the repository. Install the required packages.
2. Change the "local_ip" variable in the scripts.js file to be the IP of the machine running the web app.
3. Run mainv1.py.
4. Open your web browser and navigate to `http://localhost:5000` or whatever local ip you set to access the web application.

## Future Work

- Image generation and Image recognition using Stable Diffusion.
- Create docker container to do everything in. 

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

