from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KE")


client = genai.Client(api_key=GEMINI_API_KEY)

def prompt(Input):
    
    response = client.models.generate_content(model="gemini-2.5-flash", contents=Input)
    print(response.text)
    return response

if __name__ == "__main__":
    Input = "Explain how AI works in a few words"
    prompt(Input)