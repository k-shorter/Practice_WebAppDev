import requests
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

# .envファイルから環境変数をロード
load_dotenv('.env.dev')

HP_API_KEY = os.getenv('HP_API_KEY')

# APIリクエストのURL
url = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
params = {
    "key": HP_API_KEY,  # APIキー
    "lat": "35.6951",
    "lng": "139.7536",
    "range": "5",
    "count": "100",
}

# HTTPリクエストを送信し、レスポンスを取得
response = requests.get(url, params=params)
print(HP_API_KEY)

import csv
import random
from faker import Faker

# Fakerのインスタンスを作成
fake = Faker()

# データを保持するリスト
data_list = []

if response.status_code == 200:
    root = ET.fromstring(response.content)
    namespaces = {'ns': 'http://webservice.recruit.co.jp/HotPepper/'}

    i=1
    for shop in root.findall('ns:shop', namespaces):
        shop_name = shop.find('ns:name', namespaces).text
        shop_address = shop.find('ns:address', namespaces).text
        shop_lat = shop.find('ns:lat', namespaces).text
        shop_lng = shop.find('ns:lng', namespaces).text
        shop_capacity = shop.find('ns:capacity', namespaces).text if shop.find('ns:capacity', namespaces) is not None else "50"        
        shop_budget = shop.find('ns:budget/ns:name', namespaces).text if shop.find('ns:budget/ns:name', namespaces) is not None else "N/A"
        shop_genre = shop.find('ns:genre/ns:name', namespaces).text
        shop_sub_genre = shop.find('ns:sub_genre/ns:name', namespaces).text if shop.find('ns:sub_genre/ns:name', namespaces) is not None else "N/A"
        shop_smoking = shop.find('ns:non_smoking', namespaces).text
        shop_info = shop.find('ns:catch', namespaces).text


        max_budget = 5000  # デフォルト値

        if shop_budget and "/" not in shop_budget:
            if "～" in shop_budget and "円" in shop_budget:
                budget_parts = shop_budget.split("～")
                if len(budget_parts) > 1:
                    max_budget = int(budget_parts[1].split("円")[0].strip())

        genre_map = {
            "居酒屋": "焼き鳥",
            "和食": "海鮮",
            "中華": "中華",
            "イタリアン・フレンチ": "イタリアン"
        }
        converted_genre = genre_map.get(shop_genre, "その他")

        # shop_capacityを整数に変換できるか確認し、不可能な場合はデフォルト値を設定
        try:
            shop_capacity_int = int(shop_capacity)
        except :
            shop_capacity_int = 50

        # shop_smokingが全面禁煙の場合はFalse、それ以外はTrue
        smoking_allowed = False if shop_smoking == '全面禁煙' else True

        # データをリストに追加
        data_list.append({
            "Name": shop_name,
            "Address": shop_address,
            "Lat": shop_lat,
            "Lng": shop_lng,
            "Capacity": shop_capacity_int,
            "Image": str(i)+".jpg",
            "Budget": max_budget,
            "Genre": converted_genre,
            "Smoking allowed": smoking_allowed,
            "Additional info": shop_info,
            "Available seats": random.randint(0, shop_capacity_int)
        })
        i+=1
else:
    print(f"Failed to retrieve data: {response.status_code}")


# データをCSVファイルに出力
csv_file = 'restaurants.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=data_list[0].keys())
    writer.writeheader()
    for data in data_list:
        writer.writerow(data)

print(f"Data has been written to {csv_file}")