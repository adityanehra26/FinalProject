from database_handler import DatabaseHandler

class Recommendation:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def calculate_sentiment_score(self, comment):
        positive_words = ["delicious", "fantastic", "excellent", "superb", "enjoyed"]
        negative_words = ["bad", "poor", "disappointing", "awful", "not good"]

        positive_score = sum(comment.lower().count(word) for word in positive_words)
        negative_score = sum(comment.lower().count(word) for word in negative_words)
        return positive_score - negative_score

    def recommend_food_items(self):
        avg_ratings = self.db_handler.calculate_average_ratings()
        recommendations = {"Breakfast": [], "Lunch": [], "Dinner": []}
        seen_items = {"Breakfast": set(), "Lunch": set(), "Dinner": set()}

        for item in avg_ratings:
            menu_item_id = item["MenuItemID"]
            menu_item_name = item["MenuItem"]
            avg_rating = item["AvgRating"]
            comment = item.get("Comment", "")  # Fetching comment, if available
            sentiment_score = self.calculate_sentiment_score(comment)

            combined_score = avg_rating + sentiment_score

            meal_type = item["MealTypeID"]
            recommendation = {"MenuItemID": menu_item_id, "MenuItem": menu_item_name, "Score": combined_score}

            category = ""
            if meal_type == 1:
                category = "Breakfast"
            elif meal_type == 2:
                category = "Lunch"
            elif meal_type == 3:
                category = "Dinner"

            if menu_item_id not in seen_items[category]:
                recommendations[category].append(recommendation)
                seen_items[category].add(menu_item_id)

        # Sort recommendations by score in descending order and keep only top 3 recommendations
        for category in recommendations:
            recommendations[category].sort(key=lambda x: x["Score"], reverse=True)
            recommendations[category] = recommendations[category][:3]

        # Extract menu item IDs and names from recommendations
        for category in recommendations:
            recommendations[category] = [{"ID": rec["MenuItemID"], "Name": rec["MenuItem"]} for rec in recommendations[category]]

        return recommendations


if __name__ == "__main__":
    # Replace with your actual database connection details
    db_handler = DatabaseHandler(host="localhost", user="root", password="12345678", database="cafeteria")
    
    # Connect to the database
    db_handler.connect()
    
    # Create an instance of Recommendation
    recommendation = Recommendation(db_handler)
    
    # Example: Get recommendations
    recommendations = recommendation.recommend_food_items()
    print("Recommendations:")
    print(f"Breakfast: {recommendations['Breakfast']}")
    print(f"Lunch: {recommendations['Lunch']}")
    print(f"Dinner: {recommendations['Dinner']}")
    
    # Close the database connection
    db_handler.close()
