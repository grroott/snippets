import os
import requests
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

# === Configuration ===
site_url = "https://yourtenant.sharepoint.com/sites/yoursite"
username = "your.email@yourtenant.com"
password = "your_password"
local_file_path = r"C:\local\file.txt"
target_folder_url = "Shared Documents/Folder/Subfolder"

# === Create a custom requests session with SSL verification disabled ===
session = requests.Session()
session.verify = False  # 🔥 DISABLE SSL VERIFY - Not safe for production

# Suppress only the specific SSL warning if needed
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# === Auth + Upload ===
ctx_auth = AuthenticationContext(site_url, session=session)
if ctx_auth.acquire_token_for_user(username, password):
    ctx = ClientContext(site_url, ctx_auth)
    ctx.session = session  # force using the same session for all SharePoint operations

    with open(local_file_path, 'rb') as file_content:
        filename = os.path.basename(local_file_path)
        target_folder = ctx.web.get_folder_by_server_relative_url(target_folder_url)
        target_folder.upload_file(filename, file_content).execute_query()
        print(f"Uploaded: {filename}")
else:
    print("Authentication failed")
