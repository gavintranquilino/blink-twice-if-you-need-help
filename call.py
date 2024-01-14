from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import requests
import time

def entered(string):
    for i in string:
        twiml.say(i)
        #twiml.pause(length=0.1)

def get_country_name(country_code):
    try:
        # Fetch country information from restcountries.com
        response = requests.get(f"https://restcountries.com/v3.1/alpha/{country_code}")
        data = response.json()

        # Extract country name
        country_name = data[0].get('name', {}).get('common', 'N/A')

        return country_name

    except Exception as e:
        print(f"Error fetching country name: {e}")
        return 'N/A'

def get_ip_info():
    try:
        # Fetch IP information from ipinfo.io
        response = requests.get("https://ipinfo.io")
        data = response.json()

        # Extract relevant information
        ip_address = data.get('ip', 'N/A')
        city = data.get('city', 'N/A')
        country_code = data.get('country', 'N/A')
        coordinates = data.get('loc', 'N/A').split(',')

        country_name = get_country_name(country_code)

        return ip_address, city, country_name, coordinates[0], coordinates[1]


    except Exception as e:
        print(f"Error: {e}")

# Twilio credentials
account_sid = "your key"
auth_token = "your key"
twilio_phone_number = "your number [int]"
print(twilio_phone_number)


# simple number entry for what number you want to call - simple boolean done system

done = False

while not done:
    print("Please enter a ten digit phone number to call in emergency situations")
    temp_number = input("do NOT include any dashes in the phone number")

    if len(temp_number) == 10:
        for i in range(len(temp_number)):
            if not temp_number[i].isnumeric():
                print("NUMBER DECLINED")
            else:
                done = True
    else:
        print("NUMBER DECLINED")


temp_number = "+1" + temp_number
recipient_phone_number = int(temp_number)

# Create a Twilio client
client = Client(account_sid, auth_token)

location_information = get_ip_info()

# longitude (change it to negative)

if "-" in location_information[4]:
    
    longitude_sign = "negative"
    longitude_coordinate = location_information[4].strip("-")

else:
    longitude_coordinate = location_information[4]
    latitude_sign = "positive"


if "-" in location_information[3]:

    latitude_coordinate = location_information[3].strip("-")
    latitude_sign = "negative"

else:
    latitude_coordinate = location_information[3]
    latitude_sign = "positive"


try:
    # Create TwiML for a voice call with a custom message
    twiml = VoiceResponse()
    twiml.say("Hello. This is a pre-recorded emergency message. A user has called for assistance")
    twiml.pause(length=0.5)
    twiml.say("Please respond to the following location, which will be read in 3 seconds")
    twiml.pause(length=3)  # Add a pause for better clarity
    twiml.say("The IP address of the user is ")
    entered(location_information[0])
    twiml.pause(length=0.5)
    twiml.say("The IP address is located in")
    twiml.say(location_information[1])
    twiml.pause(length=0.1)
    twiml.say(location_information[2])
    twiml.pause(length=0.5)
    twiml.say("The coordinates of longitude are")
    twiml.say(longitude_sign)
    entered(longitude_coordinate)
    twiml.pause(length=0.5)
    twiml.say("The coordinates of latitude are")
    twiml.say(latitude_sign)
    entered(latitude_coordinate)
    twiml.say("Please respond promptly.  Thank you.")

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