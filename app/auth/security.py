from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password(password: str) -> str:
    """
    Hashes the password using bcrypt.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies the password against the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)
