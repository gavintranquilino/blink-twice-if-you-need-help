from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import requests
import time
import json

def entered(string, twiml):
    for i in string:
        twiml.say(i)

def get_country_name(country_code):
    try:
        response = requests.get(f"https://restcountries.com/v3.1/alpha/{country_code}")
        data = response.json()
        country_name = data[0].get('name', {}).get('common', 'N/A')
        return country_name
    except Exception as e:
        print(f"Error fetching country name: {e}")
        return 'N/A'

def get_ip_info():
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        ip_address = data.get('ip', 'N/A')
        city = data.get('city', 'N/A')
        country_code = data.get('country', 'N/A')
        coordinates = data.get('loc', 'N/A').split(',')
        country_name = get_country_name(country_code)
        return ip_address, city, country_name, coordinates[0], coordinates[1]
    except Exception as e:
        print(f"Error: {e}")

def make_emergency_call():
    with open("config.json") as f:
        config_data = json.load(f)

    account_sid = config_data["account_sid"]
    auth_token = config_data["auth_token"]
    twilio_phone_number = config_data["twilio_phone_number"]
    temp_number = config_data["temp_number"]

    temp_number = "+1" + temp_number
    recipient_phone_number = int(temp_number)

    client = Client(account_sid, auth_token)

    location_information = get_ip_info()

    longitude_sign = "negative" if "-" in location_information[4] else "positive"
    longitude_coordinate = location_information[4].strip("-")

    latitude_sign = "negative" if "-" in location_information[3] else "positive"
    latitude_coordinate = location_information[3].strip("-")

    try:
        twiml = VoiceResponse()
        twiml.say("Hello. This is a pre-recorded emergency message. A user has called for assistance")
        twiml.pause(length=0.5)
        twiml.say("Please respond to the following location, which will be read in 3 seconds")
        twiml.pause(length=3)
        twiml.say("The IP address of the user is ")
        entered(location_information[0], twiml)
        twiml.pause(length=0.5)
        twiml.say("The IP address is located in")
        twiml.say(location_information[1])
        twiml.pause(length=0.1)
        twiml.say(location_information[2])
        twiml.pause(length=0.5)
        twiml.say("The coordinates of longitude are")
        twiml.say(longitude_sign)
        entered(longitude_coordinate, twiml)
        twiml.pause(length=0.5)
        twiml.say("The coordinates of latitude are")
        twiml.say(latitude_sign)
        entered(latitude_coordinate, twiml)
        twiml.say("Please respond promptly.  Thank you.")

        call = client.calls.create(
            to=recipient_phone_number,
            from_=twilio_phone_number,
            twiml=str(twiml)
        )

        print(f"Call SID: {call.sid}")
    except Exception as e:
        print(f"Error: {e}")