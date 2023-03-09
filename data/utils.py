import string
import random
from django.utils.crypto import get_random_string

def generate():
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    username = get_random_string(length=10, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return username, password



print(generate())