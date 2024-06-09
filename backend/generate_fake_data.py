from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from models import Restaurant, RestaurantDetails, Availability,User ,Organizer,Event,Payment, PaymentMethod, Preference,Participant,Reservation, Base  # models.py での定義を使用
from faker import Faker
from random import randint, uniform

from dotenv import load_dotenv
import os

# 現在のスクリプトの絶対パスを取得
current_file_path = os.path.abspath(__file__)
# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(current_file_path)
# 環境に応じて.envファイルを読み込む
env = os.getenv('ENV', 'development')  # デフォルトを開発環境とする
if env == 'development':
    dotenv_path = os.path.join(current_dir, '.env.dev')
else:
    dotenv_path = os.path.join(current_dir, '.env.prod')
# 指定したパスから.envファイルを読み込む
load_dotenv(dotenv_path)

# imagesフォルダ内の画像ファイル名を取得
images_folder = os.path.join(current_dir, 'images')
image_files = [f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f))]

# ベースURLを設定
BASE_URL = os.getenv('BASE_URL')
base_image_url =   BASE_URL+"/images/"

# SQLAlchemyのセットアップ
DB_URL = os.getenv('DB_URL')
db_engine = create_engine(DB_URL, echo=True)
db_session = sessionmaker(bind=db_engine)

def generate_random_location(lat, lon, max_distance_km=3):
    # 緯度1度あたりの距離（約111km）
    one_degree_km = 111

    # 最大距離を度数で計算
    max_degree = max_distance_km / one_degree_km

    # ランダムなオフセットを生成
    random_lat_offset = uniform(-max_degree, max_degree)
    random_lon_offset = uniform(-max_degree, max_degree)

    # 新しい緯度と経度を計算
    new_lat = lat + random_lat_offset
    new_lon = lon + random_lon_offset

    return new_lat, new_lon

# カスタムプロバイダーを定義
class RestaurantProvider(BaseProvider):
    def restaurant_name(self):
        prefixes = ['和食', '寿司', '居酒屋', '焼肉', 'ラーメン', 'カフェ']
        suffixes = ['屋', '亭', '本店', '堂', '家', '庵', '処', '酒場']
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        return f"{prefix}{suffix}"

# Fakerを使用して仮想のデータを生成する関数
def generate_fake_data():
    session = db_session()
    fake = Faker('ja_JP')

    for i in range(100):
        # 特定の地点から3km圏内のランダムな緯度と経度を生成
        latitude, longitude = generate_random_location(35.6951, 139.7536, 3)

        image_url = base_image_url + image_files[i % len(image_files)]

        restaurant = Restaurant(
            restaurant_name=fake.company(),
            address=fake.address(),
            contact=fake.phone_number(),
            total_seats=randint(10, 50),
            latitude=latitude,
            longitude=longitude,
            image=image_url  
        )
        session.add(restaurant)
        session.commit()

        restaurant_details = RestaurantDetails(
            restaurant_id=restaurant.restaurant_id,
            genre=fake.random_element(elements=("中華", "イタリアン", "焼き鳥", "海鮮")),
            smoking_allowed=fake.boolean(),
            budget=fake.random_int(min=2000, max=12000),  # 修正された部分,
            additional_info=fake.text()
        )
        session.add(restaurant_details)
        session.commit()

        availability = Availability(
            restaurant_id=restaurant.restaurant_id,
            available_seats=randint(0, restaurant.total_seats),
            updated_at=fake.date_time_between(start_date="-1d", end_date="now")
        )
        session.add(availability)
        session.commit()
        print("レストランの擬似データが追加されました。")

    session.close()

def generate_payment_method_data():
    session = db_session()

    # 支払い方法のリスト
    payment_methods = [
        {"method_name": "現金"},
        {"method_name": "電子決済"},
        {"method_name": "後払い"},
    ]

    # 各支払い方法をデータベースに追加
    for method in payment_methods:
        new_method = PaymentMethod(**method)
        session.add(new_method)

    # 変更をコミット
    session.commit()
    print("支払い方法が追加されました。")

    # セッションをクローズ
    session.close()


# 生成したデータを削除する関数
def delete_fake_data():
    session = db_session()

    # Availability, RestaurantDetails, Restaurantsの順番で削除していく
    # これは、外部キー制約により依存関係があるため
    session.query(Availability).delete()
    session.query(RestaurantDetails).delete()
    session.query(Restaurant).delete()
    # オートインクリメントをリセット
    session.execute(text("ALTER TABLE availability AUTO_INCREMENT = 1;"))
    session.execute(text("ALTER TABLE restaurant_details AUTO_INCREMENT = 1;"))
    session.execute(text("ALTER TABLE restaurant AUTO_INCREMENT = 1;"))

    session.commit()
    session.close()

# 生成したデータを削除する関数
def delete_event_data():
    session = db_session()

    # 1. 子テーブルから削除
    session.query(Reservation).delete()
    session.query(Payment).delete()
    session.query(Participant).delete()
    
    # 依存するテーブルが削除された後に、親テーブルを削除
    session.query(Event).delete()
    session.query(Organizer).delete()
    session.query(Preference).delete()

    # 最後に、依存関係のないテーブルを削除
    session.query(User).delete()

    # オートインクリメントをリセット
    session.execute(text("ALTER TABLE user AUTO_INCREMENT = 1;"))
    session.execute(text("ALTER TABLE event AUTO_INCREMENT = 1;"))
    session.execute(text("ALTER TABLE organizer AUTO_INCREMENT = 1;"))
    session.execute(text("ALTER TABLE preference AUTO_INCREMENT = 1;"))
    session.execute(text("ALTER TABLE Reservation AUTO_INCREMENT = 1;"))
    session.execute(text("ALTER TABLE payment AUTO_INCREMENT = 1;"))
    session.execute(text("ALTER TABLE participant AUTO_INCREMENT = 1;"))


    session.commit()
    session.close()

# 実行例
generate_fake_data()  # データ生成
#generate_payment_method_data()
#delete_fake_data()    # データ削除
#delete_event_data()