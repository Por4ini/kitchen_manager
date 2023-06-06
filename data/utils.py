import string
import random
from bs4 import BeautifulSoup
import requests
from django.utils.crypto import get_random_string
from django.shortcuts import redirect

def generate():
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    username = get_random_string(length=10, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return username, password

#def test():
#    a = 
requests.get('https://bagatolososya-chain-co.iiko.it/resto/api/auth?login=Pavel_B&pass=cd58fb308d0118ea4108da526d8f345e65590205')  
# Get token for postavshil
#    a = a.text.replace('"', '')
#    b = requests.get(f'https://bagatolososya-chain-co.iiko.it/resto/api/suppliers?key={a}').text
#    root = BeautifulSoup(b, 'html.parser')
#    for data in root.find_all():
#        if data.find('name'):
#            try:
#                title = data.find('name').string
#                code = data.find('code').string
#                if '@' in str(title):
#                    try:
#                        email = data.find('email').string
#                    except:
#                        email = 'None'
#                    provider = {
#                        'title': title,
#                        'id': int(code),
#                        'email': email,
              
