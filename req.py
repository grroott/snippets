import requests
import os
from requests.auth import HTTPBasicAuth
import json

# === Configuration ===
site_url = "https://yourtenant.sharepoint.com/sites/yoursite"
folder_url = "/sites/yoursite/Shared Documents/Folder/Subfolder"  # Server-relative path
local_file_path = r"C:\local\file.txt"
username = "your.email@yourtenant.com"
password = "your_password"

# === Setup session ===
session = requests.Session()
session.auth = HTTPBasicAuth(username, password)
session.verify = False  # ⚠️ Ignore SSL certs (unsafe for production)
requests.packages.urllib3.disable_warnings()

# === Get form digest ===
headers = {
    "Accept": "application/json;odata=verbose",
    "Content-Type": "application/json;odata=verbose"
}
digest_url = f"{site_url}/_api/contextinfo"
response = session.post(digest_url, headers=headers)
response.raise_for_status()
digest_value = response.json()['d']['GetContextWebInformation']['FormDigestValue']

# === Upload the file ===
file_name = os.path.basename(local_file_path)
upload_url = f"{site_url}/_api/web/GetFolderByServerRelativeUrl('{folder_url}')/Files/add(url='{file_name}',overwrite=true)"

with open(local_file_path, 'rb') as f:
    file_content = f.read()

upload_headers = {
    "Accept": "application/json;odata=verbose",
    "X-RequestDigest": digest_value
}

upload_response = session.post(upload_url, data=file_content, headers=upload_headers)
upload_response.raise_for_status()

print(f"✅ File uploaded successfully: {upload_response.json()['d']['ServerRelativeUrl']}")
