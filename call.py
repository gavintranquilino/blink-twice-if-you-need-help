from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client

# Twilio credentials
account_sid = "test"
auth_token = "test"
twilio_phone_number = +12159774320


# simple number entry for what number you want to call - simple boolean done system
recipient_phone_number = +5195055856

# Create a Twilio client
client = Client(account_sid, auth_token)

try:
    # Create TwiML for a voice call with a custom message
    twiml = VoiceResponse()
    twiml.say("You lost the game")
    twiml.pause(length=1)  # Add a pause for better clarity
    twiml.say("Thank you for using Twilio!")

    # their current location is (approx coordinates - put that in)

    # Make a phone call
    call = client.calls.create(
        to=recipient_phone_number,
        from_=twilio_phone_number,
        twiml=str(twiml)  # Use the TwiML string as instructions
    )

    print(f"Call SID: {call.sid}")
except Exception as e:
    print(f"Error: {e}")