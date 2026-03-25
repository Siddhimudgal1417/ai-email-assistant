import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_calendar_service():
    # Use the token.json we created earlier
    # Ensure this path points to where your token actually is
    token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'token.json')
    
    if not os.path.exists(token_path):
        raise FileNotFoundError("token.json not found. Run auth_setup.py first!")

    creds = Credentials.from_authorized_user_file(token_path)
    return build('calendar', 'v3', credentials=creds)

def create_calendar_event(summary, start_time, end_time, attendees=None):
    """
    Creates an event on the user's primary Google Calendar.
    start_time/end_time should be in ISO format: '2026-03-20T10:00:00Z'
    """
    service = get_calendar_service()
    
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'UTC'},
        'end': {'dateTime': end_time, 'timeZone': 'UTC'},
        'attendees': [{'email': email} for email in (attendees or [])],
    }

    try:
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event_result.get('htmlLink')}")
        return event_result.get('htmlLink')
    except Exception as e:
        print(f"Error creating calendar event: {e}")
        return None

if __name__ == "__main__":
    # Test locally
    print("Testing Calendar Service...")
    # Example: Tomorrow at 10 AM
    create_calendar_event("Test AI Meeting", "2026-03-19T10:00:00Z", "2026-03-19T11:00:00Z")