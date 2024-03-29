import requests
from bs4 import BeautifulSoup


def get_price_list(Provider, PriceList, ProductList):
    print('update price list')
    try:
        key = requests.get('https://bagatolososya-chain-co.iiko.it/resto/api/auth?login=Pavel_B&pass=cd58fb308d0118ea4108da526d8f345e65590205')  # Get token for postavshil
        key = key.text.replace('"', '')
        providers = Provider.objects.all()

        for provider in providers:
            price_data = requests.get(f'https://bagatolososya-chain-co.iiko.it/resto/api/suppliers/{provider.pk}/pricelist?key={key}').text
            new_price_data = BeautifulSoup(price_data, 'html.parser')
            print(new_price_data)
            print(provider)
            for price_item in new_price_data.find_all():
                article = price_item.find('nativeproductnum')
                item_title = price_item.find('nativeproductname')
                unit = price_item.find('name')
                price = price_item.find('costprice')
                try:
                    try:
                        price_list = PriceList.objects.get(
                            article=article.string,
                            item_title=item_title.string,
                            unit=unit.string,
                            provider_id=provider.pk
                        )
                        if price_list.price != float(price.string):
                            price_list.price = float(price.string)
                            price_list.save()
                    except PriceList.DoesNotExist:
                        price_list = PriceList.objects.create(
                            article=article.string,
                            item_title=item_title.string,
                            unit=unit.string,
                            price=float(price.string),
                            provider_id=provider.pk
                        )

                    provider = Provider.objects.get(id=provider.pk)
                    provider.have_price = 1
                    provider.save()
                    unique_items = PriceList.objects.values('item_title', 'unit').distinct()
                    for item in unique_items:
                        item_title = item['item_title']
                        unit = item['unit']
                        product_list, created = ProductList.objects.get_or_create(title=item['item_title'], unit=item['unit'])

                except Exception as e:
                    # print(f'Неповна інформація по товару: \n {e}')
                    continue
        return True
    except Exception as e:
        print(f'Помилка... : \n {e}')
