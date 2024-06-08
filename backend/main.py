import os
from math import ceil, radians, cos, sin, sqrt, atan2
from typing import List, Tuple

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session, joinedload

import models
import schemas
from db import get_db

# 現在の環境を取得
env = os.getenv('ENV', 'development') # デフォルトを開発環境とする
# 環境に応じて.envファイルを読み込む
if env == 'development':
   dotenv_path = '.env.dev'
else:
    dotenv_path = '.env.prod'
load_dotenv(dotenv_path)

REACT_URL = os.getenv('REACT_URL')

app = FastAPI()
# 静的ファイルのディレクトリを指定
app.mount("/images", StaticFiles(directory="images"), name="images")

origins = [
    REACT_URL,
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
async def hello():
 return {"message": "Hello World!"}

#################################################

#イベント作成
@app.post("/events/", response_model=schemas.Event)
def create_event(event_data: schemas.EventCreate, db: Session = Depends(get_db)):
    try:
        # Create event
        new_event = models.Event(**event_data.dict(exclude={"organizer"}))
        db.add(new_event)
        
        # Create organizer (user)
        organizer_data = event_data.organizer
        organizer_user = models.User(**organizer_data.user.dict())
        db.add(organizer_user)
        
        # Link event and organizer
        new_organizer = models.Organizer(user=organizer_user, event=new_event)
        db.add(new_organizer)
        
        db.commit()
        db.refresh(new_event)
        return new_event
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")

#参加者追加
@app.post("/participants/")
def create_participant(participant_data: schemas.ParticipantCreate, db: Session = Depends(get_db)):
    try:
        # ユーザーの作成
        new_user = models.User(**participant_data.user.dict())
        db.add(new_user)
        db.flush() 
        
        # イベント情報の確認
        event = db.query(models.Event).filter(models.Event.event_id == participant_data.event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found.")
        
        # 参加者の作成
        new_participant = models.Participant(
            is_attending=participant_data.is_attending,
            user_id=new_user.user_id,
            event_id=event.event_id,
        )
        db.add(new_participant)
        db.flush() 

        # 支払い情報の計算と登録
        amount = round(event.total_cost / max(event.primary_participant_count, 1))
        new_payment = models.Payment(
            **participant_data.payment.dict(exclude={"amount"}),
            amount=ceil(amount),
            participant_id=new_participant.participant_id
        )
        db.add(new_payment)

        # 好みの登録
        new_preference = models.Preference(**participant_data.preference.dict(), user_id=new_user.user_id)
        db.add(new_preference)
        db.commit()
        db.refresh(new_participant)

        participant_with_relations = db.query(models.Participant).options(
            joinedload(models.Participant.user).joinedload(models.User.preference),
            joinedload(models.Participant.event),
            joinedload(models.Participant.payment)
        ).filter(models.Participant.participant_id == new_participant.participant_id).first()

        return participant_with_relations
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

#二次会参加者数追加
@app.post("/adjust_participants/", response_model=schemas.Event)
def adjust_participants(data: schemas.AdjustParticipants, db: Session = Depends(get_db)):
    try:
        # イベント情報を取得
        event = db.query(models.Event).filter(models.Event.event_id == data.event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found.")
        
        # イベントに紐づく参加者の合計数を取得し、num_people_adjustmentを考慮して更新
        participant_count = db.query(models.Participant).filter(models.Participant.event_id == event.event_id).count()
        total_count = participant_count + data.num_people_adjustment
        event.secondary_participant_count = total_count
        db.commit()

        return event
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

#レストラン検索用　距離
def calculate_distance(origin: Tuple[float, float], destination: Tuple[float, float]) -> float:
    # 地球の半径（km）
    R = 6371.0

    lat1, lon1 = origin
    lat2, lon2 = destination

    # 緯度経度をラジアンに変換
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # 緯度と経度の差
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # ハーバーサイン公式
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    print(distance)

    return distance

def classify_restaurants_by_walking_time(user_location: Tuple[float, float], restaurants: List[models.Restaurant]) -> dict:
    groups = {"3~10分": [], "11~15分": [], "15分~": []}
    for restaurant in restaurants:
        # 距離を計算（calculate_distance関数を使用）
        distance_km = calculate_distance(user_location, (restaurant.latitude, restaurant.longitude))
        # 距雦から徒歩時間を推定
        walking_time_min = (distance_km * 1000) / 83  # 分速83mで計算

        # 徒歩時間に基づいてグループ分け
        if walking_time_min <= 10:
            groups["3~10分"].append(restaurant)
        elif walking_time_min <= 15:
            groups["11~15分"].append(restaurant)
        else:
            groups["15分~"].append(restaurant)

    return groups

@app.get("/search/restaurants_by_walking_time/")
def get_restaurants_by_walking_time(event_id: int = Query(..., description="Event ID"), db: Session = Depends(get_db)):
    # イベント情報を取得
    event = db.query(models.Event).filter(models.Event.event_id ==event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")
    pass
    
    # secondary_participant_countに基づいて予約可能なレストランを検索
    available_restaurants = db.query(models.Restaurant).join(
        models.Availability,
        models.Restaurant.restaurant_id == models.Availability.restaurant_id
    ).filter(
        models.Availability.available_seats >= event.secondary_participant_count
    )

    
    # ユーザーの位置
    user_location = (event.latitude, event.longitude, )
    
    # レストランを徒歩時間で分類
    restaurants_grouped_by_walking_time = classify_restaurants_by_walking_time(user_location, available_restaurants)
    
    return {"grouped_restaurants": restaurants_grouped_by_walking_time}


#レストラン検索用　金額
def classify_restaurants_by_budget(restaurants: List[models.Restaurant], specified_budget: int) -> dict:
    groups = {"budget_low": [], "budget_mid": [], "budget_high": []}
    
    for restaurant in restaurants:
        if restaurant.restaurant_details.budget <= specified_budget and restaurant.restaurant_details.budget >= specified_budget - 1000:
            groups["budget_low"].append(restaurant)
        elif restaurant.restaurant_details.budget <= specified_budget + 1500 and restaurant.restaurant_details.budget > specified_budget:
            groups["budget_mid"].append(restaurant)
        else:
            groups["budget_high"].append(restaurant)
    
    return groups

@app.get("/search/restaurants_by_budget/")
def get_restaurants_by_budget(event_id: int = Query(..., description="Event ID"),
    budget: int = Query(..., description="Specified budget"), db: Session = Depends(get_db)):
    # イベント情報を取得
    event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")
    
    # secondary_participant_countに基づいて予約可能なレストランを検索
    available_restaurants = db.query(models.Restaurant).join(
        models.Availability,
        models.Restaurant.restaurant_id == models.Availability.restaurant_id
    ).filter(
        models.Availability.available_seats >= event.secondary_participant_count
    ).all()
    
    # レストランを予算に基づいて分類
    restaurants_grouped_by_budget = classify_restaurants_by_budget(available_restaurants, budget)
    
    return {"grouped_restaurants": restaurants_grouped_by_budget}

# @app.post("/test/", response_model=schemas.User)
# def test(reservation_data: schemas.ReservationCreate, db: Session = Depends(get_db)):

#     return None

# @app.post("/reservations/", response_model=schemas.Reservation)
# def create_reservation(reservation_data: schemas.ReservationCreate, db: Session = Depends(get_db)):
#     # 利用可能席数を取得
#     availability = db.query(models.Availability).filter(models.Availability.restaurant_id == reservation_data.restaurant_id).first()
#     if not availability or availability.available_seats < reservation_data.reserved_seats:
#         raise HTTPException(status_code=400, detail="利用可能な席数が足りません。")

#     # 予約を作成
#     db_reservation = models.Reservation(
#         reservation_date=reservation_data.reservation_date,
#         reserved_seats=reservation_data.reserved_seats,
#         reservation_status=reservation_data.reservation_status,
#         arrival_time=reservation_data.arrival_time,
#         updated_at=reservation_data.updated_at,
#         restaurant_id=reservation_data.restaurant_id,
#         organizer_id=reservation_data.organizer_id
#     )
#     db.add(db_reservation)

#     # 利用可能席数を更新
#     availability.available_seats -= reservation_data.reserved_seats
#     db.add(availability)

#     db.commit()
#     db.refresh(db_reservation)
#     return db_reservation

# @app.post("/search/")
# def search_restaurant(search_data: schemas.SearchRestaurant, db: Session = Depends(get_db)):
#     # イベント情報を取得
#     event = db.query(models.Event).filter(models.Event.event_id == search_data.event_id).first()
#     if not event:
#         raise HTTPException(status_code=404, detail="Event not found.")
#     pass

#     # イベントに紐づく参加者の合計数を取得し、num_people_adjustmentを考慮して更新
#     participant_count = db.query(models.Participant).filter(models.Participant.event_id == event.event_id).count()
#     total_count = participant_count + search_data.num_people_adjustment
#     event.secondary_participant_count = total_count
#     db.commit()

#     # secondary_participant_countに基づいて予約可能なレストランを検索
#     available_restaurants = db.query(models.Restaurant).join(
#         models.Availability,
#         models.Restaurant.restaurant_id == models.Availability.restaurant_id
#     ).filter(
#         models.Availability.available_seats >= total_count
#     )

#     user_location = func.Point(event.longitude, event.latitude)
#     nearby_restaurants=available_restaurants.order_by(
#         func.ST_Distance_Sphere(
#             func.Point(models.Restaurant.longitude, models.Restaurant.latitude),
#             user_location
#         )
#     ).limit(5).all()

#     affordable_restaurants=available_restaurants.join(
#     models.RestaurantDetails,  # 予算情報を含むテーブルとの結合
#     models.RestaurantDetails.restaurant_id == models.Restaurant.restaurant_id
#     ).filter(
#         models.RestaurantDetails.budget <= search_data.budget,  # 予算以下のレストランに絞り込む
#     ).order_by(
#     models.RestaurantDetails.budget.asc()  # 予算が低い順にソート
#     ).limit(5).all()
    
#     # イベントに参加しているユーザーのIDを取得
#     participant_ids = db.query(models.Participant.user_id).filter(models.Participant.event_id == search_data.event_id).all()
#     participant_ids = [id[0] for id in participant_ids]  # 結果をリストに変換

#     # 参加者の好みからsmoking_allowedの平均値を計算
#     if participant_ids:  # 参加者がいる場合にのみ計算
#         smoking_allowed_avg = db.query(func.avg(models.Preference.smoking_allowed)).filter(models.Preference.user_id.in_(participant_ids)).scalar()
#     else:
#         return {"error": "No participants found for the given event_id"}

#     # 定義されたジャンルリスト
#     defined_genres = ["海鮮", "中華", "イタリアン", "焼き鳥"]

#     # 参加者の好みからジャンルを取得し、カンマで分割
#     genres = []
#     if participant_ids:
#         preferences = db.query(models.Preference.genre).filter(models.Preference.user_id.in_(participant_ids)).all()
#         for preference in preferences:
#             genres.extend(preference[0].split(','))  # カンマで分割してリストに追加

#     # ジャンルの出現回数をカウント
#     genre_count = Counter(genres)

#     # 参加人数からジャンルの選好数を引く
#     genre_balance_ratio = {genre: ((total_count - genre_count.get(genre, 0)) / total_count) * 100 for genre in defined_genres}
#     # 集計結果を返す

#     restaurant_evaluations = []
#     for restaurant in available_restaurants:
#         # 禁煙・喫煙評価
#         if restaurant.restaurant_details.smoking_allowed == 0:
#             smoking_evaluation = smoking_allowed_avg *100
#         else:
#             smoking_evaluation = (1 - smoking_allowed_avg)*100

#         # 好みの評価
#         restaurant_genre = restaurant.restaurant_details.genre
#         preference_evaluation = genre_balance_ratio.get(restaurant_genre, 0)

#         # 最終評価（禁煙・喫煙評価と好みの評価の平均）
#         final_evaluation = (float(smoking_evaluation) + preference_evaluation) / 2

#         restaurant_evaluations.append({
#             "restaurant_id": restaurant.restaurant_id,
#             "s":smoking_evaluation,
#             "p":preference_evaluation,
#             "evaluation": final_evaluation
#         })

#     # 評価の高い順にレストラン情報をソート
#     sorted_evaluations = sorted(restaurant_evaluations, key=lambda x: x['evaluation'], reverse=True)

#     # ソートされたレストラン情報を含むリストを返す
#     evaluated_restaurants = []
#     for eval_info in sorted_evaluations:
#         restaurant = db.query(models.Restaurant).filter(models.Restaurant.restaurant_id == eval_info["restaurant_id"]).first()
#         evaluated_restaurants.append({
#             "restaurant_id": restaurant.restaurant_id,
#             "restaurant_name": restaurant.restaurant_name,
#             "genre": restaurant.restaurant_details.genre,
#             "smoking_allowed": restaurant.restaurant_details.smoking_allowed,
#             "evaluation": eval_info["evaluation"]
#         })
#     return {"evaluated_restaurants": evaluated_restaurants}

# from typing import Tuple
# from math import radians, cos, sin, sqrt, atan2

# def calculate_distance(origin: Tuple[float, float], destination: Tuple[float, float]) -> float:
#     # 地球の半径（km）
#     R = 6371.0

#     lat1, lon1 = origin
#     lat2, lon2 = destination

#     # 緯度経度をラジアンに変換
#     lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

#     # 緯度と経度の差
#     dlon = lon2 - lon1
#     dlat = lat2 - lat1

#     # ハーバーサイン公式
#     a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
#     c = 2 * atan2(sqrt(a), sqrt(1 - a))

#     distance = R * c
#     print(distance)

#     return distance

# def classify_restaurants_by_walking_time(user_location: Tuple[float, float], restaurants: List[models.Restaurant]) -> dict:
#     groups = {"3~10分": [], "11~15分": [], "15分~": []}
#     for restaurant in restaurants:
#         # 距離を計算（calculate_distance関数を使用）
#         distance_km = calculate_distance(user_location, (restaurant.latitude, restaurant.longitude))
#         # 距雦から徒歩時間を推定
#         walking_time_min = (distance_km * 1000) / 83  # 分速83mで計算

#         # 徒歩時間に基づいてグループ分け
#         if walking_time_min <= 10:
#             groups["3~10分"].append(restaurant)
#         elif walking_time_min <= 15:
#             groups["11~15分"].append(restaurant)
#         else:
#             groups["15分~"].append(restaurant)

#     return groups

# @app.post("/search/restaurants_by_walking_time/")
# def get_restaurants_by_walking_time(search_data: schemas.SearchRestaurant, db: Session = Depends(get_db)):
#     # イベント情報を取得
#     event = db.query(models.Event).filter(models.Event.event_id == search_data.event_id).first()
#     if not event:
#         raise HTTPException(status_code=404, detail="Event not found.")
#     pass
    
#     # イベントに紐づく参加者の合計数を取得し、num_people_adjustmentを考慮して更新
#     participant_count = db.query(models.Participant).filter(models.Participant.event_id == event.event_id).count()
#     total_count = participant_count + search_data.num_people_adjustment
#     event.secondary_participant_count = total_count
#     db.commit()

#     # secondary_participant_countに基づいて予約可能なレストランを検索
#     available_restaurants = db.query(models.Restaurant).join(
#         models.Availability,
#         models.Restaurant.restaurant_id == models.Availability.restaurant_id
#     ).filter(
#         models.Availability.available_seats >= total_count
#     )

    
#     # ユーザーの位置
#     user_location = (event.latitude, event.longitude, )
    
#     # レストランを徒歩時間で分類
#     restaurants_grouped_by_walking_time = classify_restaurants_by_walking_time(user_location, available_restaurants)
    
#     # 分類されたレストランの情報を整理してレスポンスに含める
#     # この部分では、各グループ内のレストラン情報を整理し、必要な情報を抽出してレスポンスに追加する処理を行います
#     # 例えば、レストランのID、名前、ジャンルなどの情報を含めることが考えられます
#     # 詳細な実装は省略しますが、必要に応じて追加してください

#     return {"grouped_restaurants": restaurants_grouped_by_walking_time}




# def classify_restaurants_by_budget(restaurants: List[models.Restaurant], specified_budget: int) -> dict:
#     groups = {"budget_low": [], "budget_mid": [], "budget_high": []}
    
#     for restaurant in restaurants:
#         if restaurant.restaurant_details.budget <= specified_budget and restaurant.restaurant_details.budget >= specified_budget - 1000:
#             groups["budget_low"].append(restaurant)
#         elif restaurant.restaurant_details.budget <= specified_budget + 1500 and restaurant.restaurant_details.budget > specified_budget:
#             groups["budget_mid"].append(restaurant)
#         else:
#             groups["budget_high"].append(restaurant)
    
#     return groups

# @app.post("/search/restaurants_by_budget/")
# def get_restaurants_by_budget(search_data: schemas.SearchRestaurant, db: Session = Depends(get_db)):
#     # イベント情報を取得
#     event = db.query(models.Event).filter(models.Event.event_id == search_data.event_id).first()
#     if not event:
#         raise HTTPException(status_code=404, detail="Event not found.")
#     pass
    
#     # イベントに紐づく参加者の合計数を取得し、num_people_adjustmentを考慮して更新
#     participant_count = db.query(models.Participant).filter(models.Participant.event_id == event.event_id).count()
#     total_count = participant_count + search_data.num_people_adjustment
#     event.secondary_participant_count = total_count
#     db.commit()

#     # secondary_participant_countに基づいて予約可能なレストランを検索
#     available_restaurants = db.query(models.Restaurant).join(
#         models.Availability,
#         models.Restaurant.restaurant_id == models.Availability.restaurant_id
#     ).filter(
#         models.Availability.available_seats >= total_count
#     )
    
#     # レストランを予算に基づいて分類
#     restaurants_grouped_by_budget = classify_restaurants_by_budget(available_restaurants, search_data.budget)
    
#     # 分類されたレストランの情報を整理してレスポンスに含める
#     # この部分では、各グループ内のレストラン情報を整理し、必要な情報を抽出してレスポンスに追加する処理を行います
#     # 例えば、レストランのID、名前、ジャンル、予算などの情報を含めることが考えられます
#     # 詳細な実装は省略しますが、必要に応じて追加してください

#     return {"grouped_restaurants": restaurants_grouped_by_budget}

# # @app.post("/test/", response_model=schemas.User)
# # def test(reservation_data: schemas.ReservationCreate, db: Session = Depends(get_db)):

# #     return None