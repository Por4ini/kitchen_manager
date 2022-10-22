import json
import pandas as pd

with open('new_file.json', encoding='utf8') as file:
    data = json.load(file)

data_list = data['id']

df_m1 = pd.json_normalize(data_list, max_level=2)
df_m1.to_excel('my_book.xlsx')
