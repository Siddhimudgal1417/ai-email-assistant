from google import genai
import os
import json
from dotenv import load_dotenv

# --- 1. PATH RESOLUTION ---
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
dotenv_path = os.path.join(root_dir, '.env')
load_dotenv(dotenv_path)

# --- 2. API KEY PICKUP ---
api_key = os.getenv("GOOGLE_API_KEY")

# --- 3. INITIALIZE CLIENT ---
client = None
if api_key:
    # We explicitly set the client to use the Gemini 2.0 series
    client = genai.Client(api_key=api_key)
else:
    print(f"⚠️ WARNING: No GOOGLE_API_KEY found at {dotenv_path}")

def process_email_with_ai(email_body):
    """
    Analyzes email text using the modern Gemini 2.0 Flash model.
    """
    if not client:
        return {"intent": "ERROR", "message": "API Key missing in .env"}

    if not email_body or len(email_body.strip()) < 5:
        return {"intent": "UNKNOWN", "message": "Body too short"}

    try:
        # Define the system instructions clearly
        system_instruction = "You are an AI Executive Assistant. Return ONLY a JSON object."
        
        prompt = f"""
        Analyze this email and return a JSON object.
        If it's a meeting request, set intent to 'SCHEDULING'.
        Otherwise, set intent to 'UPDATE'.
        
        EMAIL CONTENT: {email_body}
        
        FORMAT: {{ "intent": "SCHEDULING", "summary": "...", "slots": [] }}
        """

        # We use 'gemini-2.0-flash' which is more robust and widely available
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt,
            config={'response_mime_type': 'application/json'} # Forces JSON output
        )
        
        # The new SDK has a direct .text property or a parsed response
        return json.loads(response.text)

    except Exception as e:
        # If 2.0 is not available, try the 1.5-flash-latest alias as a fallback
        try:
            response = client.models.generate_content(model='gemini-1.5-flash-latest', contents=prompt)
            return json.loads(response.text.replace('```json', '').replace('```', '').strip())
        except:
            return {"intent": "ERROR", "message": f"AI Engine Error: {str(e)}"}

if __name__ == "__main__":
    print("Testing Modern AI Engine...")
    print(process_email_with_ai("Meeting tomorrow at 5 PM"))