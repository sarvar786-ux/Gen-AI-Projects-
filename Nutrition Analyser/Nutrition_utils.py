import pandas as pd
from difflib import get_close_matches

# Load nutrition dataset
nutrition_df = pd.read_csv("sample_nutrition.csv")

def get_nutrition_info(food_items):
    """
    Returns nutrition details for a list of food items using fuzzy matching.
    """
    total_calories = 0
    total_protein = 0
    total_fat = 0
    total_carbs = 0
    details = []

    foods_list = nutrition_df['Food'].tolist()
    
    for food in food_items:
        # Find closest match in CSV
        match = get_close_matches(food, foods_list, n=1, cutoff=0.4)
        if match:
            matched_food = match[0]
            info = nutrition_df[nutrition_df['Food'] == matched_food].iloc[0]

            calories = info['Calories']
            protein = info['Protein']
            fat = info['Fat']
            carbs = info['Carbs']

            total_calories += calories
            total_protein += protein
            total_fat += fat
            total_carbs += carbs

            details.append({
                "Detected Food": food,
                "Matched Food": matched_food,
                "Calories": calories,
                "Protein": protein,
                "Fat": fat,
                "Carbs": carbs
            })
    
    summary = {
    "Total Calories": int(total_calories),
    "Total Protein": float(total_protein),
    "Total Fat": float(total_fat),
    "Total Carbs": float(total_carbs)
}


    return details, summary


def generate_diet_recommendations(summary):
    """
    Generates diet suggestions based on nutrition summary.
    """
    recommendations = []
    
    if summary['Total Calories'] > 2000:
        recommendations.append("Consider reducing portion sizes or high-calorie foods.")
    if summary['Total Protein'] < 50:
        recommendations.append("Add more protein-rich foods like eggs or chicken breast.")
    if summary['Total Fat'] > 70:
        recommendations.append("Reduce fatty foods and choose lean options.")
    if summary['Total Carbs'] > 300:
        recommendations.append("Reduce refined carbs and opt for whole grains.")
    
    if not recommendations:
        recommendations.append("Your meal looks balanced! Keep it up.")
    
    return recommendations
