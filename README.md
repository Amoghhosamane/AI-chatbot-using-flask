# Flask Chatbot - ChatGPT Style

This is a chatbot application built with Flask and TensorFlow, featuring a premium UI inspired by ChatGPT.

## Project Structure

- `app.py`: The Flask web server.
- `chatbot_engine.py`: Contains the NLP processing, model training, and prediction logic.
- `intents.json`: The knowledge base for the chatbot (intents and responses).
- `requirements.txt`: List of Python dependencies.
- `templates/`: HTML templates.
- `static/`: CSS and JavaScript files for the premium frontend.

## Setup Instructions

1. **Install Dependencies**:
   Open your terminal in the project directory and run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Train the Model**:
   The first time you run the application, it will automatically train the model based on `intents.json`.
   If you want to re-train after modifying intents, you can run:
   ```bash
   py chatbot_engine.py
   ```

3. **Run the Application**:
   Start the Flask server:
   ```bash
   py app.py
   ```

4. **Access the Chatbot**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

## Features

- **ChatGPT-like UI**: Sleek dark theme with a sidebar, message bubbles, and smooth animations.
- **Context-Aware**: Supports intent context handling (e.g., following up on food delivery).
- **Responsive**: Adapts to different screen sizes.
- **Interactive**: Real-time typing indicators and auto-resizing input box.
