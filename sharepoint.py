from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.files.file import File
import os

# === Configuration ===
site_url = "https://yourtenant.sharepoint.com/sites/yoursite"
username = "your.email@yourtenant.com"
password = "your_password"
local_file_path = r"C:\local\file.txt"
target_folder_url = "Shared Documents/Folder/Subfolder"  # Relative to site

# === Authentication ===
ctx_auth = AuthenticationContext(site_url)
if ctx_auth.acquire_token_for_user(username, password):
    ctx = ClientContext(site_url, ctx_auth)
    
    with open(local_file_path, 'rb') as file_content:
        name = os.path.basename(local_file_path)
        target_folder = ctx.web.get_folder_by_server_relative_url(target_folder_url)
        target_file = target_folder.upload_file(name, file_content).execute_query()
        print(f"Uploaded to: {target_file.serverRelativeUrl}")
else:
    print("Authentication failed")
