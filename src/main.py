import time
import os
from gmail_service import get_unread_emails, send_reply
from agent import process_email_with_ai
from calendar_service import create_calendar_event

def main():
    print("--- AI Executive Assistant Started ---")
    print("Scanning for unread emails every 60 seconds...")
    
    while True:
        try:
            # 1. Fetch unread emails
            emails = get_unread_emails()
            
            if not emails:
                print(f"[{time.strftime('%H:%M:%S')}] No new emails.")
            else:
                for email in emails:
                    print(f"\nProcessing email from: {email['sender']}")
                    print(f"Subject: {email['subject']}")

                    # 2. Let Gemini analyze the intent and extract data
                    ai_response = process_email_with_ai(email['body'])
                    
                    # 3. Handle Scheduling requests
                    if ai_response.get("intent") == "SCHEDULING":
                        slots = ai_response.get("slots", [])
                        if slots:
                            # Use the first extracted slot to create a meeting
                            start_time = slots[0]['start']
                            end_time = slots[0]['end']
                            
                            print(f"Action: Scheduling meeting at {start_time}")
                            
                            event_link = create_calendar_event(
                                summary=f"Meeting: {email['subject']}",
                                start_time=start_time,
                                end_time=end_time,
                                attendees=ai_response.get("participants", [email['sender']])
                            )
                            
                            # Reply to the sender with the calendar link
                            reply_text = f"Hi! I've automatically scheduled this for you. You can find the invite here: {event_link}"
                            send_reply(email['id'], reply_text)
                            print("Result: Calendar event created and reply sent.")

                    # 4. Handle Update/Summary requests
                    elif ai_response.get("intent") == "UPDATE":
                        summary = ai_response.get("summary", "No summary provided.")
                        print(f"Action: Email Summarized: {summary}")
                        # You can choose to log this or send a summary to a 'Daily Digest'
                    
                    else:
                        print("Action: No clear intent found. Skipping.")

            # 5. Cooldown period to avoid API rate limits
            time.sleep(60)

        except Exception as e:
            print(f"Main Loop Error: {e}")
            time.sleep(10) # Wait a bit before retrying after an error

if __name__ == "__main__":
    main()