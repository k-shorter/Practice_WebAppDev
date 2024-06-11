from typing import List, Dict, Optional
from collections import Counter
import models

def evaluate_preferences(restaurant: models.Restaurant, participant_preferences: List[models.Preference]) -> float:
    # 参加者の好みからsmoking_allowedの平均値を計算
    smoking_allowed_avg = sum(p.smoking_allowed for p in participant_preferences) / len(participant_preferences)

    # 定義されたジャンルリスト
    defined_genres = ["海鮮", "中華", "イタリアン", "焼き鳥"]

    # 参加者の好みからジャンルを取得し、カンマで分割
    genres = []
    for preference in participant_preferences:
        genres.extend([genre.strip() for genre in preference.genre.split(',')])

    # ジャンルの出現回数をカウント
    genre_count = Counter(genres)

    # 参加人数からジャンルの選好数を引く
    total_count = len(participant_preferences)
    genre_balance_ratio = {genre: ((total_count - genre_count.get(genre, 0)) / total_count) * 100 for genre in defined_genres}

    # 禁煙・喫煙評価
    if restaurant.restaurant_details.smoking_allowed == 0:
        smoking_evaluation = smoking_allowed_avg * 100
    else:
        smoking_evaluation = (1 - smoking_allowed_avg) * 100

    # 好みの評価
    restaurant_genre = restaurant.restaurant_details.genre
    preference_evaluation = genre_balance_ratio.get(restaurant_genre, 0)

    # 最終評価（禁煙・喫煙評価と好みの評価の平均）
    final_evaluation = (float(smoking_evaluation) + preference_evaluation*4) / 5

    return final_evaluation

def classify_restaurants_by_preferences(restaurants: List[models.Restaurant], participant_preferences: List[models.Preference], mode: Optional[str] = "best") -> List[models.Restaurant]:
    groups = {
        "80%以上": [],
        "40~80%": [],
        "40%以下": []
    }

    for restaurant in restaurants:
        evaluation = evaluate_preferences(restaurant, participant_preferences)
        restaurant.evaluation = evaluation  # レストランに評価スコアを追加
        if evaluation >= 80:
            restaurant.evaluation_eval = 1
            groups["80%以上"].append(restaurant)
        elif 40 <= evaluation < 80:
            restaurant.evaluation_eval = 2
            groups["40~80%"].append(restaurant)
        else:
            restaurant.evaluation_eval = 3
            groups["40%以下"].append(restaurant)

    # 各グループを評価スコアの高い順に並べ替え
    for key in groups:
        groups[key].sort(key=lambda r: r.evaluation, reverse=True)

    # デバッグ用に各グループの内容を表示
    for key, group in groups.items():
        print(f"グループ: {key}")
        for restaurant in group:
            print(f"レストラン名: {restaurant.restaurant_name}, 評価: {restaurant.evaluation}")

    if mode == "best":
        if groups["80%以上"]:
            return groups["80%以上"]
        elif groups["40~80%"]:
            return groups["40~80%"]
        elif groups["40%以下"]:
            return groups["40%以下"]

    return {key: groups[key] for key in groups}