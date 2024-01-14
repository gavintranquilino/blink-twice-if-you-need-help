import requests
import time

def entered(string):
    for i in string:
        print(i)
        time.sleep(0.75)

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

        print(country_name)

        # Print information
        print(f"IP Address: {ip_address}")
        print(f"City: {city}")
        print(f"Latitude: {coordinates[0]}")
        print(f"Longitude: {coordinates[1]}")

        # save to variables

        print("among us")
        print(coordinates[0])

        print("The user's IP Address is")
        entered(ip_address)
        print("the IP Address' city is", city)
        print("the coordinates of latitude are ")
        entered(coordinates[0])
        print("the coordinates of longitude are ")
        entered(coordinates[1])

        print(country)



    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_ip_info()