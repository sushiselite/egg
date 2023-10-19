import requests
import base64
import hashlib
import binascii
import requests
import ei_pb2
from google.protobuf.json_format import MessageToJson

# sha256 bytes string, lowercase no spaces
# ex: b"1af6ae16fd477587e25cbb70ed958253afcd0e60e77da3015a614cd25aaea2d8"
def sha256(bytes_obj):
    h = hashlib.sha256()
    h.update(bytes_obj)
    return binascii.hexlify(h.digest())

# returns hash string
def hashexample(message_bytes):
    data = bytearray(message_bytes)
    data[0x3b9af419 % len(data)] = 0x1b
    data.extend(sha256(b'THE SECRETS OF THE UNIVERSE WILL BE UNLOCKED'))
    return sha256(data).decode('ascii')

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

# Print the original values
print("Original Values:")
print(first_contact_response.backup.game.unclaimed_eggs_of_prophecy)
print(first_contact_response.backup.game.total_time_cheats_detected)
print(first_contact_response.backup.game.unclaimed_soul_eggs_d)

# Edit the backup values
first_contact_response.backup.game.unclaimed_eggs_of_prophecy = 150
first_contact_response.backup.game.total_time_cheats_detected = 0
first_contact_response.backup.game.unclaimed_soul_eggs_d = 12000000000000000000
first_contact_response.backup.force_backup = True
first_contact_response.backup.force_offer_backup = True

# Serialize the modified response
serialized_response = first_contact_response.SerializeToString()

# Recalculate the code
new_code = hashexample(serialized_response)

# Create an authenticated message
auth_message = ei_pb2.AuthenticatedMessage()

# Serialize the modified first_contact_response.backup
serialized_backup = first_contact_response.backup.SerializeToString()

# Set the message, version, and code fields for the authenticated message
auth_message.message = serialized_backup
auth_message.code = new_code

# Serialize the authenticated message
serialized_auth_message = auth_message.SerializeToString()

# Encode the authenticated message for sending
encoded_data = {'data': base64.b64encode(serialized_auth_message).decode('utf-8')}

# Make a POST request with the authenticated message
response = requests.post(url, data=encoded_data)

print("Response from Authenticated Message:")
print(response.text)