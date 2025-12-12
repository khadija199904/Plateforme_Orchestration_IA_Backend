import os 
from dotenv import load_dotenv

load_dotenv()

USER =os.getenv("POSTGRES_USER")
PASSWORD =os.getenv("POSTGRES_PASSWORD","secret")
HOST =os.getenv("POSTGRES_HOST", "db")
PORT =os.getenv("POSTGRES_PORT")
DB  =os.getenv("POSTGRES_DB")

HF_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
 # Configuration de JWT
SECRET_KEY = os.getenv("SECRET_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KE")