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

# レスポンスのステータスコードをチェック
if response.status_code == 200:
    # レスポンスの内容をXMLとして解析
    root = ET.fromstring(response.content)
    
    # 名前空間の定義
    namespaces = {'ns': 'http://webservice.recruit.co.jp/HotPepper/'}

    i=1
    # 各レストランの情報を抽出して表示
    for shop in root.findall('ns:shop', namespaces):
        shop_name = shop.find('ns:name', namespaces).text
        shop_address = shop.find('ns:address', namespaces).text
        shop_lat = shop.find('ns:lat', namespaces).text
        shop_lng = shop.find('ns:lng', namespaces).text
        shop_capacity = shop.find('ns:capacity', namespaces).text
        shop_budget = shop.find('ns:budget/ns:name', namespaces).text if shop.find('ns:budget/ns:name', namespaces) is not None else "N/A"
        shop_genre = shop.find('ns:genre/ns:name', namespaces).text
        shop_sub_genre = shop.find('ns:sub_genre/ns:name', namespaces).text if shop.find('ns:sub_genre/ns:name', namespaces) is not None else "N/A"
        shop_smoking = shop.find('ns:non_smoking', namespaces).text

        max_budget = 5000  # デフォルト値

        # 予算に"/"が含まれているものを省く
        if shop_budget and "/" not in shop_budget:
            # 予算情報から「～」と「円」の間の金額を抽出
            if "～" in shop_budget and "円" in shop_budget:
                budget_parts = shop_budget.split("～")
                if len(budget_parts) > 1:
                    max_budget = int(budget_parts[1].split("円")[0].strip())

        
        # ジャンルの変換ロジック
        genre_map = {
            "居酒屋": "焼き鳥",
            "和食": "海鮮",
            "中華": "中華",
            "イタリアン・フレンチ": "イタリアン"
        }
        converted_genre = genre_map.get(shop_genre, "その他")


        
        print(f"Name: {shop_name}")
        print(f"Address: {shop_address}")
        print(f"Contact: contact")
        print(f"Lat: {shop_lat}")
        print(f"Lng: {shop_lng}")
        print(f"Capacity: {shop_capacity}")
        print(f"Image: img")
        print(f"Budget: {max_budget}")
        print(f"Genre: {converted_genre}")
        print(f"Smoking: {shop_smoking}")
        print(f"Additional info: additional_info")
        print(f"Available seats: available_seats")

        print(i)
        print("-" * 40)
        i += 1

else:
    print(f"Failed to retrieve data: {response.status_code}")
