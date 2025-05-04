"""
Flask application for the multimodal analysis frontend.
"""
import os
import sys
import uuid
import json

# Add parent directory to path more safely
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the backend processing function
from backend.main import process_question
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'multimodal_analysis_secret_key'

# Configure upload folders
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

def allowed_file(filename):
    """
    Check if the file extension is allowed.
    
    Args:
        filename: The name of the file to check
        
    Returns:
        True if the file extension is allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """
    Render the main application page.
    
    Returns:
        The rendered index.html template
    """
    # Initialize a session ID if not present
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    return render_template('index.html')

def extract_final_response(history):
    """
    Extract the final response from the history, handling JSON objects properly.
    
    Args:
        history: The full conversation history
        
    Returns:
        The processed final response
    """
    if not history:
        return 'No response available'
    
    # Split history into lines and find the last meaningful content
    lines = history.split('\n')
    
    # Go through lines in reverse to find the last non-JSON or processed result
    for line in reversed(lines):
        line = line.strip()
        if line and line.startswith('Executed'):
            # Found an execution result
            parts = line.split('with result: ')
            if len(parts) > 1:
                return parts[1]
        
        # Try to detect if it's a JSON output from an agent
        if line.startswith('{') and line.endswith('}'):
            try:
                # Parse the JSON
                data = json.loads(line)
                # If it's an agent response with a scenario field, return that
                if 'scenario' in data:
                    return data['scenario']
                # If it has a function field, this is a tool execution record
                elif 'function' in data:
                    continue
            except json.JSONDecodeError:
                # Not valid JSON, might be legitimate text response
                pass
    
    # If no specific response format was found, return the last line
    for line in reversed(lines):
        if line.strip() and not line.strip().startswith('{'):
            return line.strip()
            
    # Fallback
    return lines[-1] if lines else 'No response available'

@app.route('/process', methods=['POST'])
def process():
    """
    Process the user's query and files.
    
    Returns:
        JSON response with the processing result
    """
    # Get the user's query
    query = request.form.get('query', '')
    
    # Initialize file paths
    image_path = None
    pdf_path = None
    
    # Process image file if uploaded
    if 'image' in request.files:
        image_file = request.files['image']
        if image_file and image_file.filename != '' and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            # Add session ID to filename to prevent collisions
            unique_filename = f"{session['session_id']}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            image_file.save(file_path)
            image_path = file_path
    
    # Process PDF file if uploaded
    if 'pdf' in request.files:
        pdf_file = request.files['pdf']
        if pdf_file and pdf_file.filename != '' and allowed_file(pdf_file.filename):
            filename = secure_filename(pdf_file.filename)
            # Add session ID to filename to prevent collisions
            unique_filename = f"{session['session_id']}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            pdf_file.save(file_path)
            pdf_path = file_path
    
    # Process the query
    result = process_question(query, image_path, pdf_path)
    
    # Extract a meaningful response using our helper function
    response = extract_final_response(result.get('history', '')) if result else 'Error processing request'
    
    return jsonify({
        'response': response,
        'history': result.get('history', '') if result else ''
    })

@app.route('/clear', methods=['POST'])
def clear_session():
    """
    Clear the current session data.
    
    Returns:
        JSON response confirming the session was cleared
    """
    # Generate a new session ID
    session['session_id'] = str(uuid.uuid4())
    
    return jsonify({
        'status': 'success',
        'message': 'Session cleared'
    })

if __name__ == '__main__':
    app.run(debug=True)