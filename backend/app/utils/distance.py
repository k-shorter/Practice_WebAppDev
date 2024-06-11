from math import radians, cos, sin, sqrt, atan2
from typing import Tuple, List, Optional
import models

def calculate_distance(origin: Tuple[float, float], destination: Tuple[float, float]) -> float:
    R = 6371.0  # 地球の半径（km）
    lat1, lon1 = origin
    lat2, lon2 = destination

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def classify_restaurants_by_walking_time(user_location: Tuple[float, float], restaurants: List[models.Restaurant], mode: Optional[str] = "best") -> List[models.Restaurant]:
    groups = {"3~10分": [], "11~15分": [], "15分~": []}
    restaurant_distances = []

    for restaurant in restaurants:
        distance_km = calculate_distance(user_location, (restaurant.latitude, restaurant.longitude))
        walking_time_min = (distance_km * 1000) / 83  # 分速83mで計算
        restaurant.walking_time_min = walking_time_min  # レストランに評価スコアを追加

        if walking_time_min <= 10:
            restaurant.walking_time_min_eval = 1  
            groups["3~10分"].append(restaurant)
        elif walking_time_min <= 15:
            restaurant.walking_time_min_eval = 2  
            groups["11~15分"].append(restaurant)
        else:
            restaurant.walking_time_min_eval = 3  
            groups["15分~"].append(restaurant)

    # 各グループを近い順に並べ替え
    for key in groups:
        groups[key].sort(key=lambda r: r.walking_time_min)


    # デバッグ用に各グループの内容を表示
    for key, group in groups.items():
        print(f"グループ: {key}")
        for restaurant in group:
            print(f"レストラン名: {restaurant.restaurant_name}, 徒歩時間: {restaurant.walking_time_min}分")

    if mode == "best":
        if groups["3~10分"]:
            return groups["3~10分"]
        elif groups["11~15分"]:
            return groups["11~15分"]
        elif groups["15分~"]:
            return groups["15分~"]

    return {key: groups[key] for key in groups}
