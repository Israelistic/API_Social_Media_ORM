from passlib.context import CryptContext
#Define the password algorithm 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)