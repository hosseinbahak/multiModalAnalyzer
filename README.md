# Multimodal Analysis System

A comprehensive system for analyzing images and PDF documents using advanced AI models with a user-friendly web interface.

## Features

- **Image Analysis**: Analyze and describe image content using the LLaVA model
- **PDF Analysis**: Extract and analyze content from PDF documents
- **Interactive Web Interface**: User-friendly interface for uploading files and asking questions
- **Modular Architecture**: Cleanly separated backend and frontend components

## Project Structure

```
multimodal-analysis-app/
├── backend/               # Backend logic and AI processing
│   ├── agent/             # AI agent implementations
│   ├── tools/             # Analysis tools
│   ├── utils/             # Helper utilities
│   ├── workflow.py        # LangGraph workflow setup
│   └── main.py            # Backend entry point
├── frontend/              # Flask web application
│   ├── static/            # Static assets (CSS, JS)
│   ├── templates/         # HTML templates
│   └── app.py             # Flask application
├── uploads/               # Directory for uploaded files
├── temp/                  # Temporary processing directory
├── requirements.txt       # Project dependencies
└── run.py                 # Main application entry point
```

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/multimodal-analysis-app.git
   cd multimodal-analysis-app
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Install Ollama and required models (if not already installed)
   ```bash
   # Follow Ollama installation instructions at https://ollama.ai/
   
   # Pull required models
   ollama pull gemma2:27b
   ollama pull llava:13b
   ```

## Usage

1. Start the application
   ```bash
   python run.py
   ```

2. Open your web browser and navigate to http://127.0.0.1:5000

3. Upload an image or PDF file and ask questions about the content

## For Developers

### Adding New Tools

To add a new tool:

1. Create a new function in the appropriate file in `backend/tools/`
2. Decorate it with the `@tool` decorator
3. Document the function with docstrings

Example:
```python
@tool
def my_new_tool(param1: str, param2: int = 0) -> str:
    """
    Description of what my new tool does.
    
    :function: my_new_tool
    :param str param1: Description of param1
    :param int param2: Description of param2
    :return: What the tool returns
    """
    # Implementation
    return result
```

### Extending the Frontend

The frontend is built with Flask, HTML, CSS, and JavaScript. To extend it:

1. Add new routes in `frontend/app.py`
2. Create new templates in `frontend/templates/`
3. Modify CSS in `frontend/static/css/style.css`
4. Add JavaScript functionality in `frontend/static/js/main.js`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Uses [Ollama](https://ollama.ai/) for running local AI models
- PDF processing with [pdf2image](https://github.com/Belval/pdf2image)