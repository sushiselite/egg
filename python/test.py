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

user_id = 'EI5582934564274176'

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
# Decode the base64 response
decoded_response = base64.b64decode(response.text)

# Decode as an authenticated message
auth_message = ei_pb2.AuthenticatedMessage()
auth_message.ParseFromString(decoded_response)

# Decode the message field as a Backup
backup = ei_pb2.Backup()
backup.ParseFromString(auth_message.message)

# Make changes to the backup
backup.game.unclaimed_eggs_of_prophecy = 150
backup.game.total_time_cheats_detected = 0
backup.game.soul_eggs_d = 1200000000000000000000000000000000
backup.force_backup = True
backup.force_offer_backup = True

# Serialize the modified backup
modified_backup = backup.SerializeToString()

# Create a new authenticated message with the same code from the original message
new_auth_message = ei_pb2.AuthenticatedMessage()
new_auth_message.message = modified_backup
new_auth_message.code = auth_message.code 

# Serialize the new authenticated message
serialized_new_auth_message = new_auth_message.SerializeToString()

# Create a final authenticated message setting compressed to true and original_size
final_auth_message = ei_pb2.AuthenticatedMessage()
final_auth_message.compressed = True
final_auth_message.original_size = len(serialized_new_auth_message)
final_auth_message.message = serialized_new_auth_message  # This is not compressed due to the absence of zlib

# Generate a new auth code using your method
new_code = hashexample(serialized_new_auth_message) 
final_auth_message.code = new_code

# Serialize the final authenticated message
serialized_final_auth_message = final_auth_message.SerializeToString()

# Base64 encode the final message
encoded_data = base64.b64encode(serialized_final_auth_message).decode('utf-8')

# Send the data back using the 'save_backup_secure' endpoint
response_data = {'data': encoded_data}
response = requests.post("https://www.auxbrain.com/ei/save_backup_secure", data=response_data)

print("Final Response:")
print(response.text)