from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import speech_recognition as sr

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load dataset
with open('dataset.json') as f:
    dataset = json.load(f)

# Speech recognition setup
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        user_input = r.recognize_google(audio)
        print("You said: " + user_input)
        return user_input
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return ""

# Define route for chatbot
@app.route('/chat', methods=['POST', 'OPTIONS'])  # Allow OPTIONS method explicitly
def chat():
    if request.method == 'OPTIONS':
        return '', 200  # Handle preflight request
    user_message = request.json.get('message')
    if user_message.strip() == "":
        user_message = recognize_speech()  # Attempt to recognize speech if text is empty
    
    if user_message.strip() == "":
        response = "I'm sorry, I didn't catch that."
    else:
        response = get_response(user_message.lower())  # Function to get response based on user input
    
    return jsonify({"response": response})

# Function to get response from dataset based on user input
def get_response(user_input):
    for intent in dataset['intents']:
        for pattern in intent['patterns']:
            if user_input in pattern.lower():
                return intent['responses'][0]  # Assuming first response for simplicity
    return "I'm sorry, I didn't understand that."

if __name__ == '__main__':
    app.run(debug=True)

