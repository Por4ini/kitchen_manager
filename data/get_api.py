import requests
import sqlite3
from bs4 import BeautifulSoup


def get_kitchen():
    # AUTH_PARAMS = {
    #     'host': 'https://card.iiko.co.uk:9900/api/0/',
    #     'user': 'bagatolososia',
    #     'password': 'ewn934wffwhyA',
    #     'organizationID': 'b2320000-3838-06a2-edca-08d919d0bc83',
    # }  #Params to biz_api
    try:
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS kitchens
                     (id integer primary key, title varchar(60), address varchar(60), Technical_Information varchar(60))''')
        c.execute('DELETE FROM kitchens;')
        response = requests.get(
            'https://card.iiko.co.uk:9900/api/0/auth/access_token?user_id=bagatolososia&user_secret=ewn934wffwhyA').text
        token = response.replace('"', '')  # iko_biz api

        res = requests.get("https://card.iiko.co.uk:9900/api/0/deliverySettings/getDeliveryTerminals", params={"access_token": token, 'organization': 'b2320000-3838-06a2-edca-08d919d0bc83'}).json()

        for item in res['deliveryTerminals']:
            title = item['deliveryRestaurantName']
            address = item['address']
            technicalInformation = item['technicalInformation']
            print(title, address)
            c.execute(f'''INSERT INTO kitchens (title, address, Technical_Information) VALUES ('{title}', '{address}', '{technicalInformation}');''')
        conn.commit()
        conn.close()
        print('True')
        return True

    except:
        print('False')
        return False



def get_provider():
    try:
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()


        c.execute("""CREATE TABLE IF NOT EXISTS provider
                    (id integer primary key, title varchar(60), code varchar(60), email varchar(60), have_price bool)""")
        c.execute("""CREATE TABLE IF NOT EXISTS price_list
                    (id integer primary key, article varchar(60), item_title varchar(60), unit varchar(60), price varchar(60),
                    provider_id integer,  FOREIGN KEY (provider_id) REFERENCES provider(id))""")
        c.execute("""CREATE TABLE IF NOT EXISTS product_list
                            (id integer primary key, title varchar(60))""")
        c.execute("""CREATE TABLE IF NOT EXISTS unit
                                    (id integer primary key, title varchar(60))""")

        c.execute('DELETE FROM provider;')
        c.execute('DELETE FROM price_list;')
        c.execute('DELETE FROM product_list;')
        c.execute('DELETE FROM unit;')

        a = requests.get(
            'https://bagatolososya-chain-co.iiko.it/resto/api/auth?login=Pavel_B&pass=cd58fb308d0118ea4108da526d8f345e65590205')  # Get token for postavshil
        a = a.text.replace('"', '')
        b = requests.get(f'https://bagatolososya-chain-co.iiko.it/resto/api/suppliers?key={a}').text
        root = BeautifulSoup (b, 'html.parser')
        # print(root.find_all('name'))
        for data in root.find_all():
            title = data.find('name')
            code = data.find('code')
            email = data.find('email')
            try:
                print(title.string, code.string, email.string)
                c.execute(
                    f'''INSERT INTO provider (title, code, email, have_price) VALUES ('{title.string}', '{code.string}', '{email.string}', '0');''')
                price_list = requests.get(
                    f'https://bagatolososya-chain-co.iiko.it/resto/api/suppliers/{code.string}/pricelist?key={a}').text
                data_pk = c.execute('SELECT * FROM provider;')
                for item in data_pk:
                    if item[1] == title.string:
                        pk = item[0]
                        data_item = BeautifulSoup(price_list, 'html.parser')
                        for item_price in data_item.find_all():
                            article = item_price.find('nativeproductnum')
                            item_title = item_price.find('nativeproductname')
                            unit = item_price.find('name')
                            price = item_price.find('costprice')

                            try:

                                print(article.string, item_title.string, unit.string, price.string, pk)
                                c.execute(
                                    f'''INSERT INTO price_list (article, item_title, unit, price, provider_id) VALUES ('{article.string}', '{item_title.string}', '{unit.string}', '{price.string}', '{pk}');''')
                                c.execute(
                                    f'''UPDATE provider SET have_price='1' WHERE id="{pk}"''')
                                conn.commit()
                            except:
                                continue
            except:
                continue
        a = []
        unit = []
        data = c.execute('SELECT * FROM price_list;')
        for item in data:
            a.append(item[2])
            unit.append(item[3])
        for prod in set(a):
            c.execute(
                f'''INSERT INTO product_list (title) VALUES ('{prod}');''')
        for u in set(unit):
            c.execute(
                f'''INSERT INTO unit (title) VALUES ('{u}');''')
        requests.get(f'https://bagatolososya-chain-co.iiko.it/resto/api/logout?key={a}')
        conn.commit()
        conn.close()
        return True
    except:
        return False
