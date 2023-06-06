import hashlib
import requests



def get_kitchen(Kitchens):
    try:
        response = requests.get(
    'https://loyalty.syrve.live:443/api/0/auth/access_token?user_id=bagatolososia&user_secret=ewn934wffwhyA').text

        token = response.replace('"', '')  # iko_biz api
        res = requests.get("https://loyalty.syrve.live:443/api/0/deliverySettings/getDeliveryTerminals",
                   params={"access_token": token,
                           'organization': 'b2320000-3838-06a2-edca-08d919d0bc83'}).json()


        for item in res['deliveryTerminals']:
            organizationId = item['organizationId']
            kit4en_id = int(hashlib.sha256(organizationId.encode()).hexdigest(), 16) % 10 ** 8
            kitchen_data = {
                'id': kit4en_id,
                'title': item['deliveryRestaurantName'],
                'address': item['address'],
                'technical_information': item['technicalInformation']
            }
            try:
                # Спробуємо знайти об'єкт Kitchens за допомогою унікального ідентифікатора.
                # Якщо він існує, то оновлюємо його поля за допомогою методу .update()
                # Інакше створюємо новий об'єкт за допомогою методу .create()
                kitchen = Kitchens.objects.get(id=kit4en_id)
                kitchen.title = item['deliveryRestaurantName']
                kitchen.address = item['address']
                kitchen.technical_information = item['technicalInformation']
                kitchen.save()
            except Kitchens.DoesNotExist:
                Kitchens.objects.create(**kitchen_data)
        return True
    except:
        return False