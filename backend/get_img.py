import requests
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

# imagesフォルダが存在しない場合は作成
if not os.path.exists('images'):
    os.makedirs('images')


# 現在の環境を取得
env = os.getenv('ENV', 'development') # デフォルトを開発環境とする
# 環境に応じて.envファイルを読み込む
if env == 'development':
   dotenv_path = '.env.dev'
else:
    dotenv_path = '.env.prod'
load_dotenv(dotenv_path)

HP_API_KEY = os.getenv('HP_API_KEY')

# APIリクエストのURL
url = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
params = {
    "key": HP_API_KEY,  # APIキー
    "lat": "34.67",
    "lng": "135.52",
    "range": "5",
    "count": "100",
}

# HTTPリクエストを送信し、レスポンスを取得
response = requests.get(url, params=params)

# レスポンスのXMLデータを解析
root = ET.fromstring(response.content)

# 名前空間
namespaces = {'ns': 'http://webservice.recruit.co.jp/HotPepper/'}

# 画像ファイルのインデックス番号
img_index = 1

# 'photo'情報を含む全ての'shop'エレメントを抽出
for shop in root.findall('ns:shop', namespaces):
    # 'photo'エレメントを探す
    photo = shop.find('ns:photo', namespaces)
    if photo is not None:
        # PC用の写真URLを取得
        pc_photo = photo.find('ns:pc', namespaces)
        if pc_photo is not None:
            large = pc_photo.find('ns:l', namespaces).text
            if large:
                # 画像をダウンロードして保存
                img_response = requests.get(large)
                if img_response.status_code == 200:
                    # 画像ファイルのパスを指定
                    img_path = f'images/{img_index}.jpg'
                    with open(img_path, 'wb') as img_file:
                        img_file.write(img_response.content)
                        print(f'Image saved: {img_path}')
                    img_index += 1