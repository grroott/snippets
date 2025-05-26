import requests
import json

# --- Assuming you have these from your existing setup ---
access_token = "YOUR_ACQUIRED_GRAPH_API_ACCESS_TOKEN"  # You already have this
group_chat_id = "YOUR_GROUP_CHAT_ID"  # e.g., "19:xxxxxxxxxxx@thread.v2"

# 1. SharePoint Image URL (from your upload response)
# Replace this with the actual 'media_src' or 'LinkingUrl'
sharepoint_image_url = "https://yourtenant.sharepoint.com/sites/yoursite/Shared Documents/Folder/Subfolder/image.png"
image_filename = sharepoint_image_url.split('/')[-1] # Get filename for display

# 2. Define the Adaptive Card content
adaptive_card_content = {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.5",  # Use a recent version
    "body": [
        {
            "type": "TextBlock",
            "text": "Check out this image from SharePoint:",
            "weight": "Bolder",
            "size": "Medium",
            "wrap": True
        },
        {
            "type": "Image",
            "url": sharepoint_image_url,
            "altText": f"Image: {image_filename}",
            "msTeams": { # Optional: for controlling width and allowing expansion in Teams
                "allowExpand": True,
                "width": "full" # Tries to make the image take the full width of the card
            },
            "selectAction": { # Makes the image itself clickable
                "type": "Action.OpenUrl",
                "url": sharepoint_image_url
            }
        },
        {
            "type": "TextBlock",
            "text": f"File: {image_filename}",
            "wrap": True,
            "spacing": "Small",
            "size": "Small"
        }
    ],
    "actions": [ # Optional: Add a button to open the SharePoint location
        {
            "type": "Action.OpenUrl",
            "title": "Open in SharePoint",
            # You might want to link to the folder containing the image
            # For now, it links directly to the image itself
            "url": sharepoint_image_url.rsplit('/', 1)[0] if '/' in sharepoint_image_url else sharepoint_image_url
        }
    ]
}

# 3. Construct the Graph API message payload
# The 'body.content' is a fallback/notification text.
# The actual rich content comes from the attachment.
message_payload = {
  "body": {
    "contentType": "html", # Or "text"
    # This content is often used for notifications or for clients that can't render the card.
    "content": f"An image '{image_filename}' has been shared from SharePoint. <attachment id=\"adaptivecardattachment\"></attachment>"
  },
  "attachments": [
    {
      "id": "adaptivecardattachment", # Needs to match the ID in body.content if you use the <attachment> tag
      "contentType": "application/vnd.microsoft.card.adaptive",
      "contentUrl": None, # Set to null if content is inline
      "content": json.dumps(adaptive_card_content) # The Adaptive Card JSON (as a string)
    }
  ]
}

# 4. Your Graph API endpoint for sending a message to a chat
graph_url = f"https://graph.microsoft.com/v1.0/chats/{group_chat_id}/messages"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# 5. Send the request (you likely have similar code already)
try:
    response = requests.post(graph_url, headers=headers, data=json.dumps(message_payload))
    response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)

    print("Message with image sent successfully to group chat!")
    # print(response.json()) # To see the full response from Graph API

except requests.exceptions.RequestException as e:
    print(f"Error sending message to Teams group chat: {e}")
    if e.response is not None:
        print(f"Graph API Error Response Status: {e.response.status_code}")
        try:
            print(f"Graph API Error Response Body: {e.response.json()}")
        except ValueError:
            print(f"Graph API Error Response Body: {e.response.text}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")