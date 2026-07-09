from cryptography.fernet import Fernet
import os
# print(Fernet.generate_key().decode())
def log_pin_decypt(PWD):
    return Fernet(b'JxFCiezevkVZNmHWTFRztjSg8lREGJY5HGqtMar1Rq4=').decrypt(PWD.encode()).decode()
def log_pin_encrypt(PWD):
    return Fernet(b'JxFCiezevkVZNmHWTFRztjSg8lREGJY5HGqtMar1Rq4=').encrypt(PWD.encode()).decode()
def admin_log_pass():
    return 'gAAAAABqLWceZUHHlvqBKqDWnt1XKjkgkcenQ7izVQ1smPQfsqTPO08TSPlLX9DDX7WkvhOhLFOl1Tr7px_5g0vTNjUKGFpSHg=='



