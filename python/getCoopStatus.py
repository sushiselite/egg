import requests
import ei_pb2
import base64
from google.protobuf.json_format import MessageToJson
from mitmproxy import http
import csv

# Define your identifiers
user_id = 'EI5582934564274175'

# Create a first contact request
first_contact_request = ei_pb2.EggIncFirstContactRequest()
first_contact_request.ei_user_id = user_id
first_contact_request.client_version = 60

# Define the URL and the encoded data
url = 'https://www.auxbrain.com/ei/bot_first_contact'
data = {'data': base64.b64encode(first_contact_request.SerializeToString()).decode('utf-8')}

# Make the POST request
response = requests.post(url, data=data)

# Parse the response
first_contact_response = ei_pb2.EggIncFirstContactResponse()
first_contact_response.ParseFromString(base64.b64decode(response.text))

print(first_contact_response.backup.game.unclaimed_eggs_of_prophecy)
print(first_contact_response.backup.game.total_time_cheats_detected)
print(first_contact_response.backup.game.unclaimed_soul_eggs_d)
