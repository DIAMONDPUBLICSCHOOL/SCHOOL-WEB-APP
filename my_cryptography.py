from cryptography.fernet import Fernet
import os

def log_pin_decypt(PWD):
    return Fernet(os.environ.get('LOGIN_KEY').encode()).decrypt(PWD.encode()).decode()
def log_pin_encrypt(PWD):
    return Fernet(os.environ.get('LOGIN_KEY').encode()).encrypt(PWD.encode()).decode()
def admin_log_pass():
    return os.environ.get('ADMIN_PASS')
def universal_admin_log_pass():
    return os.environ.get('UNIVERSAL_ADMIN_PASS')
def report_data_decrypt(data):
    return Fernet(os.environ.get('REPORT_KEY').encode()).decrypt(data.encode()).decode()
def report_data_encrypt(data):
    return Fernet(os.environ.get('REPORT_KEY').encode()).encrypt(data.encode()).decode()

