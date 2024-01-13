from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client

# Twilio credentials
account_sid = 'AC5c67855eab53a5b01debe4b3e813ee69'
auth_token = '74d9aa52db3663eb6bc28500e337436a'
twilio_phone_number = +12159774320
recipient_phone_number = +5195055856

# Create a Twilio client
client = Client(account_sid, auth_token)

try:
    # Create TwiML for a voice call with a custom message
    twiml = VoiceResponse()
    twiml.say("Hello! This is a custom message from your Python script using Twilio.")
    twiml.pause(length=1)  # Add a pause for better clarity
    twiml.say("Thank you for using Twilio!")

    # Make a phone call
    call = client.calls.create(
        to=recipient_phone_number,
        from_=twilio_phone_number,
        twiml=str(twiml)  # Use the TwiML string as instructions
    )

    print(f"Call SID: {call.sid}")
except Exception as e:
    print(f"Error: {e}")