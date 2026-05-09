import json
import os.path
import base64
import streamlit as st
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/gmail.compose'
]

class GoogleWorkspaceManager:
    def __init__(self):
        self.creds = self._authenticate()
        if not self.creds:
            raise Exception("No valid Google credentials found. Cloud deployments require GOOGLE_TOKEN_JSON in secrets.")
        
    def _authenticate(self):
        creds = None
        # 1. Try Pre-authorized Token from Streamlit Secrets (Best for Cloud)
        token_data = None
        try:
            if "GOOGLE_TOKEN_JSON" in st.secrets:
                token_data = json.loads(st.secrets["GOOGLE_TOKEN_JSON"])
        except Exception:
            pass
            
        if token_data:
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            return creds

        # 2. Try Local Token File (Local Dev)
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
        # 3. If no valid creds, handle local vs cloud flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # ONLY try browser flow if we are local AND have the file
                is_local = os.path.exists('credentials.json') and not os.getenv("STREAMLIT_CLOUD_DEPLOYMENT")
                if is_local:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                    with open('token.json', 'w') as token:
                        token.write(creds.to_json())
                else:
                    # In cloud, we can't open a browser popup.
                    # We just return None and let the app handle it gracefully.
                    return None
        return creds

    def create_google_doc(self, title: str, content: str):
        """Creates a Google Doc with the specified title and content."""
        try:
            service = build('docs', 'v1', credentials=self.creds)
            # Create a blank doc
            doc = service.documents().create(body={'title': title}).execute()
            doc_id = doc.get('documentId')
            
            # Insert the content
            requests = [
                {
                    'insertText': {
                        'location': {'index': 1},
                        'text': content
                    }
                }
            ]
            
            # Find and bold headers (lines that are ALL CAPS)
            lines = content.split('\n')
            current_index = 1
            for line in lines:
                if line.strip() and line.strip().isupper() and len(line.strip()) > 3:
                    requests.append({
                        'updateTextStyle': {
                            'range': {
                                'startIndex': current_index,
                                'endIndex': current_index + len(line)
                            },
                            'textStyle': {
                                'bold': True,
                                'fontSize': {'magnitude': 12, 'unit': 'PT'}
                            },
                            'fields': 'bold,fontSize'
                        }
                    })
                current_index += len(line) + 1 # +1 for the newline
                
            service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
            return f"https://docs.google.com/document/d/{doc_id}/edit"
        except HttpError as err:
            return f"An error occurred: {err}"

    def upload_to_drive(self, file_path: str, folder_id: str = None):
        """Uploads a file to Google Drive."""
        try:
            service = build('drive', 'v3', credentials=self.creds)
            file_metadata = {'name': os.path.basename(file_path)}
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            media = MediaFileUpload(file_path, mimetype='text/csv')
            file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
            return file.get('webViewLink')
        except HttpError as err:
            return f"An error occurred: {err}"

    def create_gmail_draft(self, subject: str, body_text: str):
        """Creates a Gmail draft with the specified subject and body."""
        try:
            service = build('gmail', 'v1', credentials=self.creds)
            message = EmailMessage()
            message.set_content(body_text)
            message['Subject'] = subject
            
            # Encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {'message': {'raw': encoded_message}}
            
            draft = service.users().drafts().create(userId="me", body=create_message).execute()
            return f"Draft created with ID: {draft.get('id')}"
        except HttpError as err:
            return f"An error occurred: {err}"

if __name__ == "__main__":
    # Test (requires credentials.json)
    print("Testing Google Workspace Manager...")
    # manager = GoogleWorkspaceManager()
