import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker,declarative_base

load_dotenv()

USER =os.getenv("POSTGRES_USER")
PASSWORD =os.getenv("POSTGRES_PASSWORD")
HOST =os.getenv("POSTGRES_HOST")
PORT =os.getenv("POSTGRES_PORT")
DB  =os.getenv("POSTGRES_DB")

# DB_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
DB_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"


engine = create_engine (DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Test connection 
if __name__ == "__main__":
     
     # obtenir la session
     def get_db():
        db = SessionLocal()
        try:
             yield db
        finally:
          db.close()
     

     print(" Test de connexion à la base de données...")
     print(f"DB: {DB} | User: {USER} | Host: {HOST}:{PORT}")
     try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print(" Connexion réussie à la base de données !")
     except Exception as e:
        print(" Échec de la connexion :", e)