from typing import List, Optional
import models

def classify_restaurants_by_budget(restaurants: List[models.Restaurant], specified_budget: int, mode: Optional[str] = "best") -> List[models.Restaurant]:
    groups = {"budget_low": [], "budget_mid": [], "budget_high": []}
    
    for restaurant in restaurants:
        if restaurant.restaurant_details.budget <= specified_budget and restaurant.restaurant_details.budget >= specified_budget - 1000:
            groups["budget_low"].append(restaurant)
        elif restaurant.restaurant_details.budget <= specified_budget + 1500 and restaurant.restaurant_details.budget > specified_budget:
            groups["budget_mid"].append(restaurant)
        else:
            groups["budget_high"].append(restaurant)

     # 各グループを安い順に並べ替え
    for key in groups:
        groups[key].sort(key=lambda r: r.restaurant_details.budget)

    # デバッグ用に各グループの内容を表示
    for key, group in groups.items():
        print(f"グループ: {key}")
        for restaurant in group:
            print(f"レストラン名: {restaurant.restaurant_name}, 予算: {restaurant.restaurant_details.budget}")

    if mode == "best":
        if groups["budget_low"]:
            return groups["budget_low"]
        elif groups["budget_mid"]:
            return groups["budget_mid"]
        elif groups["budget_high"]:
            return groups["budget_high"]
    
    return {key: groups[key] for key in groups}