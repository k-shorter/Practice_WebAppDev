from typing import List, Optional, Tuple, Dict
import models

from .distance import classify_restaurants_by_walking_time 
from .budget import classify_restaurants_by_budget
from .preferences import classify_restaurants_by_preferences

def find_best_restaurant(user_location: Tuple[float, float], restaurants: List[models.Restaurant], specified_budget: int, participant_preferences: List[models.Preference]) -> List[models.Restaurant]:
    # それぞれの評価を取得
    walking_time_group = classify_restaurants_by_walking_time(user_location, restaurants, mode="best")
    budget_group = classify_restaurants_by_budget(restaurants, specified_budget, mode="best")
    preferences_group = classify_restaurants_by_preferences(restaurants, participant_preferences, mode="best")

    # 各グループの中で最も高い評価のレストランを選択
    best_walking_time_restaurant = None
    best_budget_restaurant = None
    best_preferences_restaurant = None

    if walking_time_group:
        # 近いグループの中で安いかつ好み
        best_walking_time_restaurant = classify_restaurants_by_preferences(
            classify_restaurants_by_budget(walking_time_group, specified_budget, mode="best"),
            participant_preferences,
            mode="best"
        )[0]

    if budget_group:
        # すでに選ばれたレストランを除外
        budget_group = [r for r in budget_group if r != best_walking_time_restaurant]
        if budget_group:
            # 安いグループの中で好みかつ近い
            best_budget_restaurant = classify_restaurants_by_walking_time(
                user_location,
                classify_restaurants_by_preferences(budget_group, participant_preferences, mode="best"),
                mode="best"
            )[0]

    if preferences_group:
        # すでに選ばれたレストランを除外
        preferences_group = [r for r in preferences_group if r != best_walking_time_restaurant and r != best_budget_restaurant]
        if preferences_group:
            # 好みのグループの中で近いかつ安い
            best_preferences_restaurant = classify_restaurants_by_budget(
                classify_restaurants_by_walking_time(user_location, preferences_group, mode="best"),
                specified_budget,
                mode="best"
            )[0]

    return [best_walking_time_restaurant, best_budget_restaurant, best_preferences_restaurant]
