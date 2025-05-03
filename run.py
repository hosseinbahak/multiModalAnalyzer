#!/usr/bin/env python3
"""
Main application entry point for the Multimodal Analysis System.
This script runs the frontend Flask application.
"""
import os
import sys
import argparse

# Add the current directory to the Python path to ensure local imports work correctly
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Now import the app from the local frontend package
from frontend.app import app as flask_app

def main():
    """
    Parse command line arguments and start the application.
    """
    parser = argparse.ArgumentParser(description='Run the Multimodal Analysis System')
    parser.add_argument('--host', default='127.0.0.1', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    
    # Create required directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('temp', exist_ok=True)
    
    # Run the Flask application
    flask_app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()