# LocalGPT

LocalGPT is a web application that serves a local Large Language Model (LLM) using a Flask API. It interacts with the Ollama Python libraries and API to provide language processing capabilities.

## Project Structure


- `mainv1.py`: The main Flask application file and API.
- `templates/index.html`: The HTML for the web application.
- `static/scripts.js`: JavaScript file for handling client-side interactions.

## Features

- **Flask API**: Provides an interface for interacting with the local LLM.
- **Ollama Integration**: Uses Ollama Python libraries and API for language model functionality.
- **Real-Time Streaming**: Supports streaming responses in real-time from the LLM, although this feature is not yet integrated into the web app. As a result, the LLM may be slow with large responses.

## Models

- Default models: "qwen2" and "llama3". These models can be changed as needed.

## Disclaimer

**WARNING:** This project is intended for development, testing, and education purposes only. It should not be used in a production environment.

## Installation

1. Clone the repository. Install the required packages. Run mainv1.py.
2. Open your web browser and navigate to `http://localhost:5000` to access the web application.

## Future Work

- Integration of real-time streaming responses into the web app.
- Add CSS for better user experience

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

