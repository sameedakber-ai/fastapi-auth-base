# --- MODULE IMPORTS ---
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated="auto"
)

# --- PASSWORD ENCRYPTION FUNCTIONS ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password by comparing it against the stored hash
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Returns the bcrypt hash of a password
    """
    
    return pwd_context.hash(password)