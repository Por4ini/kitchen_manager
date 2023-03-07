import requests
from bs4 import BeautifulSoup


def get_provider(Provider):
    try:
        a = requests.get(
            'https://bagatolososya-chain-co.iiko.it/resto/api/auth?login=Pavel_B&pass=cd58fb308d0118ea4108da526d8f345e65590205')  # Get token for postavshil
        a = a.text.replace('"', '')
        b = requests.get(f'https://bagatolososya-chain-co.iiko.it/resto/api/suppliers?key={a}').text
        root = BeautifulSoup(b, 'html.parser')

        for data in root.find_all():
            if data.find('name'):
                try:
                    title = data.find('name').string
                    code = data.find('code').string
                    email = data.find('email').string

                    provider = {
                        'title': title,
                        'id': int(code),
                        'email': email,
                    }
                    try:
                        provider = Provider.objects.get(id=int(code))
                        provider.title = title
                        provider.email = email
                        provider.save()
                    except Provider.DoesNotExist:
                        Provider.objects.create(**provider)
                except Exception as e:
                    print(f'Відсутні дані на постачальника в айко {e}')
        return True
    except Exception as e:
        print(f'Помилка оновлення таблиці постачальників: \n {e}')