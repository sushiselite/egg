import requests
import base64
import hashlib
import binascii
import ei_pb2  # Assuming ei_pb2 is generated from the provided proto file
from google.protobuf.json_format import MessageToJson

# sha256 bytes string, lowercase no spaces
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
first_contact_response.ParseFromString(base64.b64decode(response.text))

first_contact_response.backup.game.unclaimed_eggs_of_prophecy = 150
first_contact_response.backup.game.total_time_cheats_detected = 0
first_contact_response.backup.game.soul_eggs_d = 12000000000000000000
first_contact_response.backup.force_backup = True
first_contact_response.backup.force_offer_backup = True

# Ensure the ei_user_id is set in the backup
first_contact_response.backup.ei_user_id = user_id  # Set the user ID here

# Serialize the modified response
serialized_response = first_contact_response.SerializeToString()

# Recalculate the code
new_code = hashexample(serialized_response)

# Define the URL for the save_backup_secure endpoint
save_backup_url = 'https://www.auxbrain.com/ei/save_backup_secure'

# Create a new authenticated message for save_backup_secure, if needed
save_backup_auth_message = ei_pb2.AuthenticatedMessage()

# Serialize the modified first_contact_response.backup
serialized_backup = first_contact_response.backup.SerializeToString()

# Set the message, version, and code fields for the authenticated message
save_backup_auth_message.message = serialized_backup
save_backup_auth_message.code = new_code  # Recalculate if needed

# Serialize the authenticated message for save_backup_secure
serialized_save_backup_auth_message = save_backup_auth_message.SerializeToString()

# Encode the authenticated message for sending
encoded_save_backup_data = {'data': base64.b64encode(serialized_save_backup_auth_message).decode('utf-8')}

# Make a POST request to the save_backup_secure endpoint with the authenticated message
save_backup_response = requests.post(save_backup_url, data=encoded_save_backup_data)

print("Response from save_backup_secure:")
print(save_backup_response.text)
