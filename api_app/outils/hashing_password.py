from passlib.context import CryptContext

# On configure l'outil qui va crypter les mots de passe
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)