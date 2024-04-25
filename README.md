# Emotion Bot
## Project Description
This is a web-based application that allows users to record videos and perform real-time emotion detection on both facial expressions and voice recordings. The application analyze facial expressions and audio features to recognize emotions such as happiness, sadness, anger, and more. Users can interact with the application through a user-friendly web interface, record videos, and receive feedback on the emotions detected in the recordings.

## Features
1. Real-time emotion detection: The application uses deepl learning models to analyze facial expressions and audio features for real-time emotion recognition.
2. User-friendly interface: The web interface provides an intuitive user experience for recording videos and viewing emotion detection results.
3. Multi-modal emotion recognition: Emotions are detected from both facial expressions and voice recordings, providing comprehensive insights into the user's emotional state.

## How to run the project
### Pre-requisites
<ul>
  <li>Python 3.x installed on your system</li>
  <li>Required Python packages installed (Flask, OpenCV, keras, numpy, librosa, tensorflow)</li>
</ul>

### Steps
1. Clone or download the project repository from GitHub.
2. Navigate to the project directory in your terminal or command prompt.
3. Install the required Python packages by running:
   
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask application by executing the following command:

   ```bash
   python app.py
   ```
5. Open a web browser and navigate to http://localhost:5000 to access the Emotion Recognition App.
6. Use the web interface to record videos and view the detected emotions in real-time.
