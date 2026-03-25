import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    creds = None
    # Correct path to token.json assuming it's in the root
    token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'token.json')
    
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Look for credentials.json in the root
            auth_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'credentials.json')
            flow = InstalledAppFlow.from_client_secrets_file(auth_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def get_email_body(payload):
    """
    Recursively parses the email payload to extract the text body.
    Handles Single-part, Multi-part, and Nested MIME types.
    """
    body = ""
    
    # Case 1: The message has multiple parts (HTML and Plain Text)
    if 'parts' in payload:
        for part in payload['parts']:
            # Priority 1: Look for plain text
            if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break 
            # Priority 2: If no plain text, look for HTML
            elif part['mimeType'] == 'text/html' and 'data' in part['body']:
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            # Priority 3: If it's another nested multipart, recurse
            elif 'parts' in part:
                body = get_email_body(part)
                if body: break
    
    # Case 2: The message is a simple single-part email
    elif 'body' in payload and 'data' in payload['body']:
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        
    return body

def get_unread_emails():
    """
    Fetches unread emails and returns a list of dictionaries with subject, sender, and body.
    """
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', q='is:unread').execute()
    messages = results.get('messages', [])
    
    email_data = []
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        payload = msg['payload']
        headers = payload.get('headers', [])
        
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
        sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown Sender")
        
        body = get_email_body(payload)
        
        email_data.append({
            'id': message['id'],
            'subject': subject,
            'sender': sender,
            'body': body
        })
        
    return email_data

if __name__ == "__main__":
    # Test fetch
    emails = get_unread_emails()
    print(f"Found {len(emails)} unread emails.")
    for e in emails:
        print(f"Subject: {e['subject']}\nBody Snippet: {e['body'][:50]}...")