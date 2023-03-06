import requests
import mysql.connector
from bs4 import BeautifulSoup
import traceback


def get_kitchen():
    try:
        # conn = mysql.connector.connect(host='localhost',
        #                                database='h54453c_MyData',
        #                                user='h54453c_por4ini',
        #                                password='Itred19841', )
        conn = mysql.connector.connect(host='195.54.163.133',
                                       database='h54453c_MyData',
                                       user='h54453c_por4ini',
                                       password='Itred19841', )


        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS kitchens 
                     (id int(11) NOT NULL AUTO_INCREMENT, title varchar(60), address varchar(60), Technical_Information varchar(60), PRIMARY KEY (id))''')

        c.execute('DELETE FROM kitchens;')
        c.execute('DELETE FROM neworder;')
        response = requests.get(
            'https://card.iiko.co.uk/api/0/auth/access_token?user_id=bagatolososia&user_secret=ewn934wffwhyA').text
        token = response.replace('"', '')  # iko_biz api

        res = requests.get("https://card.iiko.co.uk/api/0/deliverySettings/getDeliveryTerminals",
                           params={"access_token": token,
                                   'organization': 'b2320000-3838-06a2-edca-08d919d0bc83'}).json()


        for item in res['deliveryTerminals']:
            title = item['deliveryRestaurantName']
            address = item['address']
            technicalInformation = item['technicalInformation']
            print(title, address, technicalInformation)

            c.execute(
                f'''INSERT INTO kitchens (title, address, Technical_Information) VALUES ('{title}', '{address}', '{technicalInformation}');''')

        conn.commit()
        conn.close()
        print('True')
        return True

    except:
        print('False')
        return False


def get_provider():
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='h54453c_MyData',
                                       user='h54453c_por4ini',
                                       password='Itred19841')
        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS provider
                    (id int(11) NOT NULL AUTO_INCREMENT, title varchar(60), code varchar(60), email varchar(60), have_price bool, PRIMARY KEY (id))""")
        c.execute("""CREATE TABLE IF NOT EXISTS price_list
                    (id int(11) NOT NULL AUTO_INCREMENT, article varchar(60), item_title varchar(60), unit varchar(60), price varchar(60),
                    provider_id integer,   PRIMARY KEY (id),  FOREIGN KEY  (provider_id) REFERENCES provider(id))""")
        c.execute("""CREATE TABLE IF NOT EXISTS product_list
                            (id int(11) NOT NULL AUTO_INCREMENT, title varchar(60), PRIMARY KEY (id))""")
        c.execute("""CREATE TABLE IF NOT EXISTS unit
                                    (id int(11) NOT NULL AUTO_INCREMENT, title varchar(60), PRIMARY KEY (id))""")

        c.execute('DELETE FROM provider;')
        c.execute('DELETE FROM price_list;')
        c.execute('DELETE FROM product_list;')
        c.execute('DELETE FROM unit;')
        a = requests.get(
            'https://bagatolososya-chain-co.iiko.it/resto/api/auth?login=Pavel_B&pass=cd58fb308d0118ea4108da526d8f345e65590205')  # Get token for postavshil
        a = a.text.replace('"', '')
        b = requests.get(f'https://bagatolososya-chain-co.iiko.it/resto/api/suppliers?key={a}').text
        root = BeautifulSoup(b, 'html.parser')
        # print(root.find_all('name'))

        for data in root.find_all():
            title = data.find('name')
            code = data.find('code')
            email = data.find('email')

            try:

                c.execute(
                    f'''INSERT INTO provider (title, code, email, have_price) VALUES ('{title.string}', '{code.string}', '{email.string}', '0');''')


                price_list = requests.get(
                    f'https://bagatolososya-chain-co.iiko.it/resto/api/suppliers/{code.string}/pricelist?key={a}').text

                c.execute("SELECT * FROM provider")
                rows = c.fetchall()

                for item in rows:
                    if item[2] == str(code.string):
                        pk = item[0]
                        data_item = BeautifulSoup(price_list, 'html.parser')

                        for item_price in data_item.find_all():
                            article = item_price.find('nativeproductnum')
                            item_title = item_price.find('nativeproductname')
                            unit = item_price.find('name')
                            price = item_price.find('costprice')
                           
                            try:
                        
                                c.execute(
                                    f'''INSERT INTO price_list (article, item_title, unit, price, provider_id) VALUES ('{article.string}', '{item_title.string}', '{unit.string}', '{price.string}', '{pk}');''')
                                c.execute(
                                    f'''UPDATE provider SET have_price='1' WHERE id="{pk}"''')
                                c.execute('''ALTER IGNORE TABLE price_list ADD UNIQUE INDEX(article, price, provider_id);''')
                              
                                conn.commit()
                         
                       
                            except:
                                continue
                 
            except:
                continue
        a = []
        unit = []
        c.execute("SELECT * FROM price_list")
        data = c.fetchall()
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
        print('true')
        return True
    except:

        print('false')
        return False
