import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Set up credentials using client secret JSON file
# Make sure you have downloaded the client secret JSON file from the Google Cloud Console
# and placed it in the same directory as this script.
client_secret_path = 'Client_secret1.json'  # Replace with the actual path to your client secret JSON file

# Set up credentials
credentials = None
if os.path.exists('token.json'):
    credentials = Credentials.from_authorized_user_file('token.json', scopes=['https://www.googleapis.com/auth/documents'])
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, scopes=['https://www.googleapis.com/auth/documents'])
        credentials = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(credentials.to_json())

# Build the Google Docs API service
service = build('docs', 'v1', credentials=credentials)

def create_google_doc(title, content):
    # Create a new Google Docs document with the specified title
    document = service.documents().create(body={'title': title}).execute()

    # Set the content of the document
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': content,
            }
        }
    ]
    batch_update_response = service.documents().batchUpdate(documentId=document['documentId'], body={'requests': requests}).execute()

    print(f"Google Docs document created with ID: {document['documentId']}")
    print("Content inserted into the document.")