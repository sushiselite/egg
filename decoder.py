import base64

# Base64 encoded string
encoded_data = "CgQIABAEEkBjZTdhMWE5ZThlMDRkMjAxMzNkZjA4YzEwYTU0OWJhMDgxOGNmMzA4ZWNlNTE0ZjNhMjliYzY1NDhmYWMwNTNiIAA="

# Decoding the base64 string
decoded_data = base64.b64decode(encoded_data)
print(decoded_data)
