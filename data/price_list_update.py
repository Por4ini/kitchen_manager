import requests
from bs4 import BeautifulSoup


def get_price_list(Provider, PriceList, ProductList):
    try:
        key = requests.get(
            'https://bagatolososya-chain-co.iiko.it/resto/api/auth?login=Pavel_B&pass=cd58fb308d0118ea4108da526d8f345e65590205')  # Get token for postavshil
        key = key.text.replace('"', '')
        providers = Provider.objects.all()
        product = ProductList.objects.all()
        product.delete()
        price = PriceList.objects.all()
        price.delete()

        for provider in providers:
            price_data = requests.get(
                f'https://bagatolososya-chain-co.iiko.it/resto/api/suppliers/{provider.pk}/pricelist?key={key}').text
            new_price_data = BeautifulSoup(price_data, 'html.parser')
            try:
                for price_item in new_price_data.find_all():

                        article = price_item.find('nativeproductnum').string
                        item_title = price_item.find('nativeproductname').string
                        unit = price_item.find('name').string
                        price = price_item.find('costprice').string

                        price_list = {
                            'article': article,
                            'item_title': item_title,
                            'unit': unit,
                            'price': price,
                            'provider_id': provider.pk,
                        }

                        PriceList.objects.create(**price_list)

                        provider = Provider.objects.get(id=provider.pk)
                        provider.have_price = 1
                        provider.save()
                        unique_items = PriceList.objects.values('item_title', 'unit').distinct()
                        for item in unique_items:
                            item_title = item['item_title']
                            unit = item['unit']
                            print(item_title, unit)
                            ProductList.objects.create(title=item['item_title'], unit=item['unit'])

            except Exception as e:
                print(f'Неповна інформація по товару: \n {e}')
                continue

            return True
    except Exception as e:
        print(f'Помилка... : \n {e}')