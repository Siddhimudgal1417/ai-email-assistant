import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# Scopes stay the same
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.send'
]

def get_creds():
    # Force the path to the current script's directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    creds_path = os.path.join(base_dir, 'credentials.json')
    token_path = os.path.join(base_dir, 'token.json')

    # 1. Start the OAuth Flow
    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
    creds = flow.run_local_server(port=0)

    # 2. Write the token file
    with open(token_path, 'w') as token:
        token.write(creds.to_json())
    
    # 3. Confirm EXACTLY where it went
    print("-" * 30)
    print(f"SUCCESS!")
    print(f"token.json created at: {token_path}")
    print("-" * 30)

if __name__ == "__main__":
    get_creds()