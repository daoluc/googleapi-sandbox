import os
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata'
]

def authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_google_doc(drive_service, folder_id = None):
    file_metadata = {
        'name': 'Hello World Document',
        'mimeType': 'application/vnd.google-apps.document',
        'parents': [folder_id]
    }
    file = drive_service.files().create(body=file_metadata, fields='id').execute()
    document_id = file.get('id')
    return document_id

def copy_template(drive_service, template_id, folder_id= None):
    copied_file_metadata = {
        'name': 'Copied Template Document',
        'parents': [folder_id] if folder_id else []
    }
    copied_file = drive_service.files().copy(fileId=template_id, body=copied_file_metadata).execute()
    return copied_file.get('id')

def replace_placeholder(docs_service, document_id, placeholder, new_text):
    requests = [
        {
            'replaceAllText': {
                'containsText': {
                    'text': placeholder,
                    'matchCase': True
                },
                'replaceText': new_text
            }
        }
    ]
    result = docs_service.documents().batchUpdate(
        documentId=document_id, body={'requests': requests}).execute()
    return result

def write_content(service, document_id):
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': 'Hello World!'
            }
        }
    ]
    result = service.documents().batchUpdate(
        documentId=document_id, body={'requests': requests}).execute()
    return result

def main():
    creds = authenticate()
    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)
    
    template_id = ''
    
    copied_document_id = copy_template(drive_service, template_id)
    replace_placeholder(docs_service, copied_document_id, '{{learnings}}', 'Important Lessons!')
    print(f'Document created with ID: {copied_document_id}')

    # document_id = create_google_doc(drive_service)
    # write_content(docs_service, document_id)
    # print(f'Document created with ID: {document_id}')

if __name__ == '__main__':
    main()
