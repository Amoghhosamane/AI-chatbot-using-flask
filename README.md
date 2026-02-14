# AI Chatbot using Flask

A responsive, modern chatbot application built with Flask and TensorFlow.

## Features
- Deep Learning based intent classification using TensorFlow.
- Natural Language Processing with NLTK.
- Clean, ChatGPT-inspired user interface.
- Context-aware conversation handling.
- Mobile-friendly design.

## Prerequisites
- Python 3.x (Use `py` launcher on Windows)

## Installation
1. Clone the repository.
2. Install the required dependencies:
   ```bash
   py -m pip install -r requirements.txt
   ```

## Running the Application
1. Start the Flask server:
   ```bash
   py app.py
   ```
2. Open your browser and go to `http://127.0.0.1:5000`.

## Project Structure
- `app.py`: The main Flask application and routing.
- `chatbot_engine.py`: Logic for training the model and processing user input.
- `intents.json`: JSON file containing the training data (intents, patterns, and responses).
- `static/`: Frontend assets (CSS and JavaScript).
- `templates/`: HTML templates for the web interface.
- `requirements.txt`: Python package dependencies.
