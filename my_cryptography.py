from cryptography.fernet import Fernet
import os

def log_pin_decypt(PWD):
    return Fernet(b'JxFCiezevkVZNmHWTFRztjSg8lREGJY5HGqtMar1Rq4=').decrypt(PWD.encode()).decode()
def log_pin_encrypt(PWD):
    return Fernet(b'JxFCiezevkVZNmHWTFRztjSg8lREGJY5HGqtMar1Rq4=').encrypt(PWD.encode()).decode()
def admin_log_pass():
    return 'gAAAAABqLWceZUHHlvqBKqDWnt1XKjkgkcenQ7izVQ1smPQfsqTPO08TSPlLX9DDX7WkvhOhLFOl1Tr7px_5g0vTNjUKGFpSHg=='
def report_data_decrypt(data):
    return Fernet(b'edstR0wyJqRsouXQhcBA5feoTOtNP34psaoMJdh6CM8=').decrypt(data.encode()).decode()
def report_data_encrypt(data):
    return Fernet(b'edstR0wyJqRsouXQhcBA5feoTOtNP34psaoMJdh6CM8=').encrypt(data.encode()).decode()

