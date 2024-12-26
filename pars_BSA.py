from pyrogram import Client
import datetime
import re
from pyrogram.types import InputMediaPhoto
import time
from pyrogram.errors import FloodWait
import pandas as pd
import random
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
api_id = 24373411
api_hash = '195b8f73d79491b07e658b1ca6dae0c9'

colors = [
    "Red",
    "Blue",
    "Green",
    "Yellow",
    "Orange",
    "Purple",
    "Pink",
    "Brown",
    "Black",
    "White",
    "Gray",  # или "Grey"
    "Cyan",
    "Grey",
    "Magenta",
    "Turquoise",
    "Indigo",
    "Violet",
    "Beige",
    "Maroon",
    "Olive",
    "Navy"
]


message_ids = [10982, 10983, 10991, 11186, 11187, 12064, 11198, 11193, 11194, 11197, 11199, 11200, 11384, 11510, 12116, 12117, 12118, 12119, 12149]
chat_id = '@BigSaleApple'
catalog = []


df1 = pd.DataFrame()

# Запись пустого датафрейма в файл xlsx
df1.to_excel('Price_of_product.xlsx', index=False)


start_date = datetime.datetime(2023, 4, 10)
pattern_andoid = r'(?P<product>.+?)\s(?P<price>\d+\.\d{3})'


def product_price_andoind(message_split, plus):
    pattern_android = r'(?P<product>.+?)\s(?P<price>\d+\.\d{3})'
    match = re.search(pattern_android, message_split)
    if match:
        product = match.group('product').strip()
        price = int(match.group('price').strip().replace('-', '').replace('.',''))
        price_plus = price + int(plus)
    return product, price, price_plus
id = 0
def create_catalog(articul,category,postcategory,name, price, new_price, description, photo):
    catalog.append({
    '_id': id,
    'category':category,
    'postcategory':postcategory,
    'name':name,
    'price':price,
    'new_price':new_price,
    'description':description,
    'photo':photo
    })
    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(catalog, json_file, ensure_ascii=False, indent=4)
def generate_article_code():
    global id
    id += 1
    return id
   

with Client("IZ", api_id, api_hash) as app:
    messages = app.get_chat_history(chat_id)
    
    for message in list(messages):
        if message.date>start_date:
            # Sumsung
            if message.id == 10982:
                msq = message.text.split('\n')
                for i in msq:
                    if 'A' in i or 'S' in i and 'Блок' not in i:
                        pattern_android = r'(?P<product>.+?)\s(?P<price>\d+\.\d{3})'
                        match = re.search(pattern_android, i)
                        if match:
                            product = f'Sumsung {match.group('product').strip()}'
                            price = int(match.group('price').strip().replace('-', '').replace('.',''))
                            price_plus = price + int(2000)
                            create_catalog(articul=generate_article_code(),category='Andrioid', postcategory='Устройства Sumsung', name=product, price=price, new_price=price_plus, description='', photo='')
                    #Зарядка на Sumsung
                    if 'Блок' in i:
                        pattern_android = r'(?P<product>.+?)\s(?P<price>\d+\.\d{3})'
                        match = re.search(pattern_android, i)
                        if match:
                            product = match.group('product').strip()
                            price = int(match.group('price').strip().replace('-', '').replace('.',''))
                            price_plus = price + int(2000)
                            create_catalog(articul=generate_article_code(),category='Зарядные устройства', postcategory='Зарядные устройства Sumsung', name=product, price=price, new_price=price_plus, description='', photo='')
            if message.id == 10983:
                msq = message.text.split('\n')
                for i in msq:
                    if 'Poco' in i:
                        pattern_android = r'(?P<product>.+?)\s(?P<price>\d+\.\d{3})'
                        match = re.search(pattern_android, i)
                        if match:
                            product = match.group('product').strip()
                            price = int(match.group('price').strip().replace('-', '').replace('.',''))
                            price_plus = price + int(2000)
                            create_catalog(articul=generate_article_code(),category='Andrioid', postcategory='Устройства Poco', name=product, price=price, new_price=price_plus, description='', photo='')
                    if 'Honor' in i or 'Huawei' in i:
                        pattern_android = r'(?P<product>.+?)\s(?P<price>\d+\.\d{3})'
                        match = re.search(pattern_android, i)
                        if match:
                            product = match.group('product').strip()
                            price = int(match.group('price').strip().replace('-', '').replace('.',''))
                            price_plus = price + int(2000)
                            create_catalog(articul=generate_article_code(),category='Andrioid', postcategory='Устройства Huawei', name=product, price=price, new_price=price_plus, description='', photo='')
                    if 'Redmi' in i or 'Note' in i or 'Xiaomi' in i:
                        pattern_android = r'(?P<product>.+?)\s(?P<price>\d+\.\d{3})'
                        match = re.search(pattern_android, i)
                        if match:
                            product = match.group('product').strip()
                            price = int(match.group('price').strip().replace('-', '').replace('.',''))
                            price_plus = price + int(2000)
                            create_catalog(articul=generate_article_code(),category='Andrioid', postcategory='Устройства Xiaomi', name=product, price=price, new_price=price_plus, description='', photo='')
            if message.id == 10991:
                msq = message.text.split('\n')
                for i in msq:
                    #Дайсон
                    if 'Ontrac' in i:
                        pattern = r'(.+?)\s*🇪🇺\s*(\d+\.\d+)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))
                            price_plus = price + int(1500)
                            create_catalog(articul=generate_article_code(),category='Dyson', postcategory='Беспроводные наушники Dyson', name=product, price=price, new_price=price_plus, description='', photo='')
                    #Стиллер
                    elif 'hs' in i.lower():
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))
                            price_plus = price + int(1500)
                            create_catalog(articul=generate_article_code(),category='Dyson', postcategory='Стилер Dyson', name=product, price=price, new_price=price_plus, description='', photo='')
                    #Выпрямитель
                    elif 'ht' in i.lower():
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))
                            price_plus = price + int(1500)
                            create_catalog(articul=generate_article_code(),category='Dyson', postcategory='Стилер Dyson', name=product, price=price, new_price=price_plus, description='', photo='')
                    #Фен
                    elif 'hd' in i.lower():
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))
                            price_plus = price + int(1500)
                            create_catalog(articul=generate_article_code(),category='Dyson', postcategory='Фен Dyson', name=product, price=price, new_price=price_plus, description='', photo='')
                    #Пылесос
                    elif 'sv' in i.lower():
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))
                            price_plus = price + int(1500)
                            create_catalog(articul=generate_article_code(),category='Dyson', postcategory='Пылесос Dyson', name=product, price=price, new_price=price_plus, description='', photo='')
                    #Всякая херня для дайсонов
                    else:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))
                            price_plus = price + int(1500)
                            create_catalog(articul=generate_article_code(),category='Dyson', postcategory='Прочее Dyson', name=product, price=price, new_price=price_plus, description='', photo='')
            # iMac
            if message.id == 11186:
                hhq = []
                msq = message.text.split('iMac 24” 4.5K Retina')
                for i in msq[1:]:
                    tovati = i.split('\n')
                    for j in tovati:
                        for c in colors:
                            if c in j and len(j)<30:
                                pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                                match = re.match(pattern, j)
                                if match:
                                    product = f'iMac 24” 4.5K Retina, Apple M3{tovati[0].replace(',','')}{match.group(1)}'
                                    price = int(match.group(2).replace('-','').replace('.',''))
                                    price_plus = price + int(5000)
                                    create_catalog(articul=generate_article_code(),category='iMac', postcategory='iMac M3', name=product, price=price, new_price=price_plus, description='', photo='')
                            elif c in j and len(j)>30:
                                l = j.split('_')[-1]
                                j = j.replace(f'_{l}','')
                                pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                                match = re.match(pattern, l)
                                if match:
                                    product = f'iMac 24” 4.5K Retina, Apple M1{tovati[0].replace(',','')}{match.group(1)}'
                                    price = int(match.group(2).replace('-','').replace('.',''))
                                    price_plus = price + int(5000)
                                    create_catalog(articul=generate_article_code(),category='iMac', postcategory='iMac M3', name=product, price=price, new_price=price_plus, description='', photo='')
            if message.id == 11187:
                hhq = []
                msq = message.text.split('M1')
                for i in msq[1:]:
                    tovati = i.split('\n')
                    for j in tovati:
                        for c in colors:
                            if c in j and len(j)<30:
                                pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                                match = re.match(pattern, j)
                                if match:
                                    product = f'iMac 24” 4.5K Retina, Apple M1{tovati[0].replace(',','')}{match.group(1)}'
                                    price = int(match.group(2).replace('-','').replace('.',''))
                                    price_plus = price + int(5000)
                                    create_catalog(articul=generate_article_code(),category='iMac', postcategory='iMac M1', name=product, price=price, new_price=price_plus, description='', photo='')
                            elif c in j and len(j)>30:
                                l = j.split('_')[-1]
                                j = j.replace(f'_{l}','')
                                pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                                match = re.match(pattern, l)
                                if match:
                                    product = f'iMac 24” 4.5K Retina, Apple M1{tovati[0].replace(',','')}{match.group(1)}'
                                    price = int(match.group(2).replace('-','').replace('.',''))
                                    price_plus = price + int(5000)
                                    create_catalog(articul=generate_article_code(),category='iMac', postcategory='iMac M1', name=product, price=price, new_price=price_plus, description='', photo='')
            
            if message.id == 11193:                        
                msq = message.text.split('\n')
                for i in msq:
                    #PS DISK
                    if 'PlayStation 5 Slim' in i or 'Xbox Series S' in i or 'Ps portal' in i:
                        pattern = r'([A-Za-z0-9\s\(\)]+)[\s-]+([\d.,]+)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))
                            price_plus = price + int(3000)
                            create_catalog(articul=generate_article_code(),category='Аксессуары', postcategory='PS5|Xbox PS Disk', name=product, price=price, new_price=price_plus, description='', photo='')
                    #Геймпад PS 5        
                    if 'Sony DualSense' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))
                            price_plus = price + int(3000)
                            create_catalog(articul=generate_article_code(),category='Аксессуары', postcategory='PS5|Xbox Геймпад PS5', name=product, price=price, new_price=price_plus, description='', photo='')
                    #Геймпад Xbox        
                    if 'Wireless Controller' in i or 'Геймпад Xbox Elite' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))
                            price_plus = price + int(3000)
                            create_catalog(articul=generate_article_code(),category='Аксессуары', postcategory='PS5|Xbox Геймпад Xbox', name=product, price=price, new_price=price_plus, description='', photo='')
                    #колонки JBL        
                    if 'CLIP' in i or 'XTREME' in i or 'JBL' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'Колонка JBL {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.',''))
                            price_plus = price + int(3000)
                            create_catalog(articul=generate_article_code(),category='Аксессуары', postcategory='Колонки JBL', name=product, price=price, new_price=price_plus, description='', photo='')
                    #Виртуальные Очки        
                    if 'Meta Quest' in i :
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'Виртуальные очки {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.',''))
                            price_plus = price + int(3000)
                            create_catalog(articul=generate_article_code(),category='Аксессуары', postcategory='Виртуальные очки', name=product, price=price, new_price=price_plus, description='', photo='')
                            
                    #GoPro       
                    if 'hero' in i.lower() or 'insta' in i.lower() :
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))
                            price_plus = price + int(5000)
                            create_catalog(articul=generate_article_code(),category='Аксессуары', postcategory='Go PRO', name=product, price=price, new_price=price_plus, description='', photo='')
            if message.id == 11194:                        
                msq = message.text.split('\n')
                for i in msq:
                    #Watch 10 (2024)
                    if 'S10' in i :
                        pattern = r'([A-Za-z0-9\s\(\)]+)[\s-]+([\d.,]+)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'Apple Watch {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.',''))   
                            price_plus = price + int(5000)
                            create_catalog(articul=generate_article_code(),category='Watch', postcategory='Apple Watch 10 (2024)', name=product, price=price, new_price=price_plus, description='', photo='')

                    #Watch SE 2 40(2022_23)
                    if 'Watch SE 40' in i or 'Watch SE 2023 40' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'Apple Watch {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.',''))   
                            price_plus = price + int(5000)
                            create_catalog(articul=generate_article_code(),category='Watch', postcategory='Watch SE 2 40(2022_23)', name=product, price=price, new_price=price_plus, description='', photo='')
                    #Watch SE 2 44(2022_23)        
                    if 'Watch SE 44' in i or 'Watch SE 2023 44' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'Apple Watch {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.',''))   
                            price_plus = price + int(5000)
                            create_catalog(articul=generate_article_code(),category='Watch', postcategory='Apple Watch SE 2 44(2022_23)', name=product, price=price, new_price=price_plus, description='', photo='')
                    #Watch Series 8 45 VIP        
                    if 'S8' in i :
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'Apple Watch {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.',''))   
                            price_plus = price + int(5000)
                            create_catalog(articul=generate_article_code(),category='Watch', postcategory='Apple Watch Series 8 45 VIP', name=product, price=price, new_price=price_plus, description='', photo='')
                    #Watch Series 9 41        
                    if 'S9 41' in i :
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'Apple Watch {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.',''))   
                            price_plus = price + int(5000)
                            create_catalog(articul=generate_article_code(),category='Watch', postcategory='Apple Watch Series 9 41', name=product, price=price, new_price=price_plus, description='', photo='')
                            
                    #Watch Series 9 45        
                    if 's9 45' in i.lower() :
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'Apple Watch {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.',''))   
                            price_plus = price + int(5000)
                            create_catalog(articul=generate_article_code(),category='Watch', postcategory='Apple Watch Series 9 45', name=product, price=price, new_price=price_plus, description='', photo='')
            #Watch 2 49 ULTRA 2024
            if message.id == 11196:                        
                msq = message.text.split('\n')
                for i in msq:
                    #Watch 2 49 ULTRA 2024
                    if 'Watch 49' in i or 'Ultra' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))   
                            price_plus = price + int(5000)
                            create_catalog(articul=generate_article_code(),category='Watch', postcategory='Apple Watch 2 49 ULTRA 2024', name=product, price=price, new_price=price_plus, description='', photo='')
            #Watch Garmin               
            if message.id == 11197:                        
                msq = message.text.split('\n')
                for i in msq:
                    if 'Garmin' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'Watch {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.',''))   
                            price_plus = price + int(5000)
                            create_catalog(articul=generate_article_code(),category='Watch', postcategory='Watch Garmin', name=product, price=price, new_price=price_plus, description='', photo='')
            #AirPods          
            if message.id == 11198:                        
                msq = message.text.split('\n')
                for i in msq:
                    #AirPods Max
                    if 'Max' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))   
                            price_plus = price + int(7000)
                            create_catalog(articul=generate_article_code(),category='AirPods', postcategory='AirPods Max', name=product, price=price, new_price=price_plus, description='', photo='')
                    #AirPods
                    if 'AirPods' in i and 'Max' not in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))   
                            price_plus = price + int(5000)
                            create_catalog(articul=generate_article_code(),category='AirPods', postcategory='AirPods', name=product, price=price, new_price=price_plus, description='', photo='')
                            
                    #Яндекс станция
                    if 'Яндекс' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))   
                            price_plus = price + int(15000)
                            create_catalog(articul=generate_article_code(),category='Аксессуары', postcategory='Яндекс станция', name=product, price=price, new_price=price_plus, description='', photo='')
            #iPad               
            if message.id == 11199:                        
                msq = message.text.split('\n')
                for i in msq:
                    #Pencil
                    if 'Magic Keyboard' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))   
                            price_plus = price + int(1000)
                            create_catalog(articul=generate_article_code(),category='iPad', postcategory='Pencil', name=product, price=price, new_price=price_plus, description='', photo='')
                    #iPad Air 11" (M2)
                    if 'iPad Air 11' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))   
                            price_plus = price + int(10000)
                            create_catalog(articul=generate_article_code(),category='iPad', postcategory='iPad Air 11" (M2)', name=product, price=price, new_price=price_plus, description='', photo='')
                            
                    #iPad Air 13" (M2) 2024
                    if 'iPad Air 13' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))   
                            price_plus = price + int(10000)
                            create_catalog(articul=generate_article_code(),category='iPad', postcategory='iPad Air 13" (M2) 2024', name=product, price=price, new_price=price_plus, description='', photo='')
                            
                    #iPad Pro 11" (M4) 2024
                    if 'iPad Pro 11' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))   
                            price_plus = price + int(10000)
                            create_catalog(articul=generate_article_code(),category='iPad', postcategory='iPad Pro 11" (M4) 2024', name=product, price=price, new_price=price_plus, description='', photo='')
                    #iPad Pro 13" (M4) 2024
                    if 'iPad Pro 13' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))   
                            price_plus = price + int(10000)
                            create_catalog(articul=generate_article_code(),category='iPad', postcategory='iPad Pro 13" (M4) 2024', name=product, price=price, new_price=price_plus, description='', photo='')
                            
            #iPad               
            if message.id == 11200:                        
                msq = message.text.split('\n')
                for i in msq:
                    #Pencil
                    if 'Magic Keyboard' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(1000)
                            create_catalog(articul=generate_article_code(),category='iPad', postcategory='Pencil', name=product, price=price, new_price=price_plus, description='', photo='')
                    #iPad 9
                    if 'IPad 9' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(10000)
                            create_catalog(articul=generate_article_code(),category='iPad', postcategory='iPad 9', name=product, price=price, new_price=price_plus, description='', photo='')
                    # iPad MINI 6_7
                    if 'mini 7' in i.lower() or 'mini 6' in i.lower():
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPad {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(10000)
                            create_catalog(articul=generate_article_code(),category='iPad', postcategory='iPad MINI 6 7', name=product, price=price, new_price=price_plus, description='', photo='')
                    #iPad 10
                    if 'ipad 10' in i.lower():
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(10000)
                            create_catalog(articul=generate_article_code(),category='iPad', postcategory='iPad 10', name=product, price=price, new_price=price_plus, description='', photo='')
                    #iPad Pro 12.9 RFB
                    if 'IPad Pro 12.9' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPad {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(10000)
                            create_catalog(articul=generate_article_code(),category='iPad', postcategory='iPad Pro 12.9 RFB', name=product, price=price, new_price=price_plus, description='', photo='')
            #MacBook        
            if message.id == 11384:                        
                msq = message.text.split('\n')
                for i in msq:
                    #Magic Mouse
                    if 'Magic Mouse' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(1000)
                            create_catalog(articul=generate_article_code(),category='MacBook', postcategory='Magic Mouse', name=product, price=price, new_price=price_plus, description='', photo='')
                            
                    #MacBook Air М1 13 (2020)
                    if 'Air 13 MGN' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(15000)
                            create_catalog(articul=generate_article_code(),category='MacBook', postcategory='MacBook Air М1 13 (2020)', name=product, price=price, new_price=price_plus, description='', photo='')
                    #MacBook Air М2 13 (2022)
                    if 'Air 13' in i and 'ML' in i or 'MacBook Air 13 M2' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(15000)
                            create_catalog(articul=generate_article_code(),category='MacBook', postcategory='MacBook Air М2 13 (2022)', name=product, price=price, new_price=price_plus, description='', photo='')
                    #MacBook Air М3 13 (2024)
                    if 'Air 13 M3' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(15000)
                            create_catalog(articul=generate_article_code(),category='MacBook', postcategory='MacBook Air М3 13 (2024)', name=product, price=price, new_price=price_plus, description='', photo='')
                            
            #MacBook        
            if message.id == 11510:                        
                msq = message.text.split('\n')
                for i in msq:
                    #Magic Mouse
                    if 'Magic Mouse' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(1000)
                            create_catalog(articul=generate_article_code(),category='MacBook', postcategory='Magic Mouse', name=product, price=price, new_price=price_plus, description='', photo='')
                    #MacBook Pro 13 М2 2022
                    if 'Pro 13 (M2,24_1TB)' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(15000)
                            create_catalog(articul=generate_article_code(),category='MacBook', postcategory='MacBook Pro 13 М2 2022', name=product, price=price, new_price=price_plus, description='', photo='')

                    #MacBook Pro 14 M3 (2023)
                    if 'MacBook Pro (M' in i and 'M3 , 8 Gb' in i or 'MacBook (MRX' in i or 'MacBook Pro 14 (M3 Pro' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(15000)
                            create_catalog(articul=generate_article_code(),category='MacBook', postcategory='MacBook Pro 14 M3 (2023)', name=product, price=price, new_price=price_plus, description='', photo='')

                    #MacBook Pro 13 М2 2022
                    if 'Apple MacBook Pro 16' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = match.group(1)
                            price = int(match.group(2).replace('-','').replace('.',''))
                            price_plus = price + int(15000)
                            create_catalog(articul=generate_article_code(),category='MacBook', postcategory='MacBook Pro 13 М2 2022', name=product, price=price, new_price=price_plus, description='', photo='')
                            
            #📱iPhone 11_12_SE         
            if message.id == 12116:                        
                msq = message.text.split('\n')
                for i in msq:
                    if 'меся' in i or 'От' in i or 'блок' in i:
                        continue
                    elif '12 Mini' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(5000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone 12 Mini', name=product, price=price, new_price=price_plus, description='', photo='')
                    elif '12 Pro' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(5000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone 12 Pro', name=product, price=price, new_price=price_plus, description='', photo='')
                    elif 'SE' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(5000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone SE', name=product, price=price, new_price=price_plus, description='', photo='')
                    elif '12 ' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(5000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone 12', name=product, price=price, new_price=price_plus, description='', photo='')
                    elif '11' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(5000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone 11', name=product, price=price, new_price=price_plus, description='', photo='')
                    
            #📱iPhone 13       
            if message.id == 12117:                        
                msq = message.text.split('\n')
                for i in msq:
                    if 'меся' in i or 'От' in i or 'блок' in i or '0w' in i or 'DEPPO' in i:
                        continue
                    else:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(6000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone 13', name=product, price=price, new_price=price_plus, description='', photo='')

            #📱iPhone 14      
            if message.id == 12118:                        
                msq = message.text.split('\n')
                for i in msq:
                    if 'меся' in i or 'От' in i or 'блок' in i or '0w' in i or 'DEPPO' in i:
                        continue
                    elif '14 Pro Max' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(8000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone 14 Pro Max', name=product, price=price, new_price=price_plus, description='', photo='')
                    elif '14 Pro' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(8000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone 14 Pro', name=product, price=price, new_price=price_plus, description='', photo='')
                    elif '14 Plus' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(8000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone 14 Pro Max', name=product, price=price, new_price=price_plus, description='', photo='')
                    elif '14' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(8000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone 14 Pro Max', name=product, price=price, new_price=price_plus, description='', photo='')

            #📱iPhone 15   
            if message.id == 12119:                        
                msq = message.text.split('\n')
                for i in msq:
                    if 'меся' in i or 'От' in i or 'блок' in i or '0w' in i or 'DEPPO' in i:
                        continue
                    elif '15 Plus' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(10000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone 15 Plus', name=product, price=price, new_price=price_plus, description='', photo='')
                    elif '15' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(10000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone 15', name=product, price=price, new_price=price_plus, description='', photo='')
                            
            #📱iPhone 15   
            if message.id == 12149:                        
                msq = message.text.split('\n')
                for i in msq:
                    if 'меся' in i or 'От' in i or 'блок' in i or '0w' in i or 'DEPPO' in i:
                        continue
                    elif '15 Pro Max' in i:
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(10000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone 15 Pro Max', name=product, price=price, new_price=price_plus, description='', photo='')
                    elif '15 pro' in i.lower():
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(10000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone 15 Pro', name=product, price=price, new_price=price_plus, description='', photo='')

            #📱iPhone 16
            if message.id == 12253:                        
                msq = message.text.split('\n')
                for i in msq:
                    if 'меся' in i or 'От' in i or 'блок' in i or '0w' in i or 'DEPPO' in i:
                        continue
                    elif '16 plus' in i.lower():
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(15000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone 16 Plus', name=product, price=price, new_price=price_plus, description='', photo='')
                    elif '16' in i.lower():
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(15000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone 16', name=product, price=price, new_price=price_plus, description='', photo='')
            if message.id == 12254:                      
                msq = message.text.split('\n')
                for i in msq:
                    if 'меся' in i or 'От' in i or 'блок' in i or '0w' in i or 'DEPPO' in i:
                        continue
                    elif '16 pro max' in i.lower():
                        print('16 pro max')
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(15000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone 16 Pro Max', name=product, price=price, new_price=price_plus, description='', photo='')
                    elif '16 pro' in i.lower():
                        print('16 pro')
                        pattern = r'(.+?)\s*(-?\d+\.\d+)\s*([^\w\s]|$)'
                        match = re.match(pattern, i)
                        if match:
                            product = f'iPhone {match.group(1)}'
                            price = int(match.group(2).replace('-','').replace('.','')) 
                            price_plus = price + int(15000)
                            create_catalog(articul=generate_article_code(),category='iPhone', postcategory='iPhone 16 Pro', name=product, price=price, new_price=price_plus, description='', photo='')
                        
