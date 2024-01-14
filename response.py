import subprocess
import re
import time
import json
import os
from flask import Flask, request
from twilio.twiml.voice_response import Gather, VoiceResponse
from twilio.rest import Client

app = Flask(__name__)

# Twilio Account SID and Auth Token (replace with your own)
with open("config.json") as f:
        config_data = json.load(f)

        account_sid = config_data["account_sid"]
        auth_token = config_data["auth_token"]
        twilio_phone_number = config_data["twilio_phone_number"]
        temp_number = config_data["temp_number"]

        temp_number = "+1" + temp_number
        recipient_phone_number = int(temp_number)

def get_ngrok_url():
    # Start Ngrok and get the public URL from the output
    ngrok_path = os.path.abspath(r'c:\Users\zokur\Downloads\ngrok-v3-stable-windows-amd64')
    ngrok_process = subprocess.Popen([ngrok_path, 'http', '8000'], stdout=subprocess.PIPE)
    time.sleep(2)  # Wait for Ngrok to start (adjust if needed)

    ngrok_output = ngrok_process.stdout.read().decode('utf-8')
    ngrok_url_match = re.search(r'https://\w+\.ngrok\.io', ngrok_output)

    if ngrok_url_match:
        return ngrok_url_match.group()

def handle_speech(user_speech):
    response = VoiceResponse()

    # Process user's speech and generate a response
    if 'hello' in user_speech.lower():
        response.say("Hello! You said hello.")

        # Send an SMS
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body="The user said hello!",
            from_=twilio_phone_number,
            to=recipient_phone_number
        )

        print(f"SMS SID: {message.sid}")
    else:
        response.say("I'm sorry, I didn't understand that.")

    return str(response)

@app.route('/handle-speech', methods=['POST'])
def handle_speech_route():
    user_speech = request.form['SpeechResult']
    return handle_speech(user_speech)

if __name__ == '__main__':
    ngrok_url = get_ngrok_url()

    if ngrok_url:
        print(f"Ngrok URL: {ngrok_url}")

        # Initialize Twilio client
        client = Client(account_sid, auth_token)

        # Create a TwiML response to gather user input through speech recognition
        response = VoiceResponse()
        with response.gather(input='speech', action=f'{ngrok_url}/handle-speech', timeout=5) as gather:
            gather.say("Hello! Please say something to continue.")

        # Make a phone call
        call = client.calls.create(
            to=recipient_phone_number,
            from_=twilio_phone_number,
            twiml=str(response)
        )

        print(f"Call SID: {call.sid}")

        # Run the Flask app to handle Twilio callbacks
        app.run(port=8000, debug=True)
    else:
        print("Error: Unable to retrieve Ngrok URL.")

