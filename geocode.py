from __future__ import print_function
import httplib2
import json

def getGeocodeLocation(input_string):
    google_api_key = 'xxxx'
    location_string = input_string.replace(' ', '+')
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(location_string, google_api_key)
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content.decode())
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return latitude, longitude
