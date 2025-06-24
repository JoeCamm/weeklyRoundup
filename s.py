# encode_cookies.py

import base64

# Input and output file paths
input_path = 'auth/cookies.txt'
output_path = 'encoded.txt'

# Read and encode the file
with open(input_path, 'rb') as infile:
    encoded_bytes = base64.b64encode(infile.read())

# Write to output file
with open(output_path, 'wb') as outfile:
    outfile.write(encoded_bytes)

print("✅ cookies.txt encoded to encoded.txt")

