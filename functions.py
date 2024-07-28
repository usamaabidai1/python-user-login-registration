import mysql.connector
from mysql.connector import Error
from hashlib import sha256
from configuration import DB_CONFIG  # Import database configuration

top_level_domains = ['.org', '.net', '.edu', '.ac', '.uk', '.com']


def validate_name(name: str) -> bool:
    return isinstance(name, str) and len(name) > 2


def validate_email(email: str) -> bool:
    if not isinstance(email, str) or '@' not in email:
        return False

    username, domain = email.split('@', 1)
    return len(username) > 1 and any(domain.endswith(tld) for tld in top_level_domains)


def validate_password(password: str) -> bool:
    if not isinstance(password, str) or len(password) <= 8:
        return False

    has_upper = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)

    return has_upper and has_digit


def hash_password(password: str) -> str:
    """Hash the password using SHA-256."""
    return sha256(password.encode()).hexdigest()


def create_connection():
    """Create a database connection using the configuration from configuration.py."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None


def user_exists(email: str) -> bool:
    """Check if a user exists in the database by email."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            return result[0] > 0
        except Error as e:
            print(f"Error: {e}")
        finally:
            connection.close()
    return False


def register_user_in_db(name: str, email: str, password: str) -> bool:
    """Register a new user in the database."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            hashed_password = hash_password(password)
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                           (name, email, hashed_password))
            connection.commit()
            return True
        except Error as e:
            print(f"Error: {e}")
        finally:
            connection.close()
    return False


def validate_user(name: str, email: str, password: str) -> bool:
    """Validate the user name, email and password."""
    if not validate_name(name):
        raise ValueError("Please make sure your name is greater than 2 characters!")

    if not validate_email(email):
        raise ValueError("Your email address is in the incorrect format, enter a valid email.")

    if not validate_password(password):
        raise ValueError(
            "Your password is too weak, ensure that your password is greater than 8 characters, contains a capital letter and a number.")

    return True


def register_user(name: str, email: str, password: str) -> bool:
    """Attempt to register the user if they pass validation."""
    if not validate_user(name, email, password):
        return False

    if user_exists(email):
        print("Error: User with this email already exists.")
        return False

    return register_user_in_db(name, email, password)


def login_user(email: str, password: str) -> bool:
    """Authenticate a user by email and password."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            hashed_password = hash_password(password)
            cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s AND password = %s", (email, hashed_password))
            result = cursor.fetchone()
            return result[0] > 0
        except Error as e:
            print(f"Error: {e}")
        finally:
            connection.close()
    return False
