import yagmail
import random
import bcrypt


# dotenv_path='../config/.env'
#
# load_dotenv(dotenv_path)

# Function to generate a 4-digit verification code
def generate_verification_code():
    return '{:04d}'.format(random.randint(0, 9999))



# Function to send verification code to an email address
def send_verification_code(email_address):
    # Generate a verification code
    verification_code = generate_verification_code()

    # Email credentials
    email_user = "xiaochenliang666@qq.com"
    email_password = "nrynrexvokmhbicc"

    # Initialize yagmail.SMTP object
    yag = yagmail.SMTP(email_user, email_password, host='smtp.qq.com', port=465)

    # Define the email content in Chinese
    subject = '您的验证码'
    html_template = f"""
        <html>
        <body>
            <h1>西南林学保研评分系统</h1>
            <h2 style="color: #2e6c80;">验证码</h2>
            <p style="font-size: 18px;">您的验证码是：<strong>{verification_code}</strong></p>
            <p style="font-size: 14px; color: #888;">此验证码将在10分钟内过期。</p>
        </body>
        </html>
        """

    # Send the email with HTML content
    yag.send(to=email_address, subject=subject, contents=html_template)

    print('Verification code sent successfully.')

    # Return the verification code
    return verification_code

def hash_password(password: str, salt: bytes = None) -> (str, str):
    """
    Hash a password using bcrypt.

    Args:
    password (str): The password to hash.
    salt (bytes, optional): The salt to use for hashing. If not provided, a new salt will be generated.

    Returns:
    tuple: A tuple containing the hashed password and its salt.
    """
    if salt is None:
        # Generate a new salt if not provided
        salt = bcrypt.gensalt()
    # Hash the password using the salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    # Return the hashed password and its salt
    return hashed_password.decode(), salt.decode()

# # Example usage with password and salt
# plain_password = "my_secure_password"
# custom_salt = "custom_salt_here"  # You can provide your own salt
# hashed_password, salt = hash_password(plain_password, custom_salt)
# print(f"Hashed password: {hashed_password}")
# print(f"Salt: {salt}")
#
# # Example usage with password only
# hashed_password, salt = hash_password(plain_password)
# print(f"Hashed password: {hashed_password}")
# print(f"Salt: {salt}")
#
# # Example usage
# plain_password = "my_secure_password"
# hashed_password = hash_password(plain_password)
# print(f"Hashed password: {hashed_password}")

# Example usage
if __name__ == "__main__":
    recipient_email = 'xiaochenliang666@163.com'  # Replace with the recipient's email address
    code = send_verification_code(recipient_email)
    print(f'The verification code sent to {recipient_email} is {code}')