from database_handler import DatabaseHandler
import json

class Recommendation:
    def __init__(self, db_handler):
        self.db_handler = db_handler
    
    def endpointHandler(self, client_socket, request):
        endpoint = request.get("endpoint")
        if endpoint == "/view-recomendation":
            self.view_recomendation(client_socket, request)

    def view_recomendation(self, client_socket, request):
        role_name = request.get("RoleName")
        if role_name == "Chef":
            response = self.recommend_food_items()
            response = {"status": "success", "recomendations": response}
            client_socket.sendall(json.dumps(response).encode())  

    def calculate_sentiment_score(self, comment):
        if not comment:
            return 0
        positive_words = ["delicious", "fantastic", "excellent", "superb", "enjoyed", "good", "fantastic", 
                  "amazing", "awesome", "great", "wonderful", "tasty", "yummy", "perfect", 
                  "splendid", "fabulous", "pleasant", "terrific", "nice"]

        negative_words = ["bad", "poor", "disappointing", "awful", "not good", "horrible", 
                  "terrible", "disgusting", "displeasing", "gross", "bland", "mediocre", 
                  "unpleasant", "unsatisfactory", "underwhelming", "meh", "subpar"]

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
            comment = item.get("Comment", "")  
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
            else:
                item_index = None
                for index, item in enumerate(recommendations[category]):
                    if item.get("MenuItemID") == recommendation["MenuItemID"]:
                        item_index = index
                recommendations[category][item_index]["Score"] += combined_score
            


        # Sort recommendations by score in descending order and keep only top 3 recommendations
        for category in recommendations:
            recommendations[category].sort(key=lambda x: x["Score"], reverse=True)
            recommendations[category] = recommendations[category][:3]

        # Extract menu item IDs and names from recommendations
        for category in recommendations:
            recommendations[category] = [{"ID": rec["MenuItemID"], "Name": rec["MenuItem"]} for rec in recommendations[category]]

        return recommendations
    
    def find_low_rated_negative_sentiment(self):
        print("Fetching average ratings from the database...")
        avg_ratings = self.db_handler.calculate_average_ratings()
        print(f"Avg Ratings: {avg_ratings}")
        low_rated_negative_items = []

        for item in avg_ratings:
            avg_rating = item["AvgRating"]
            comment = item.get("Comment", "")
            sentiment_score = self.calculate_sentiment_score(comment)

            if avg_rating <= 2 and sentiment_score < 0:
                low_rated_negative_items.append({
                    "MenuItemID": item["MenuItemID"],
                    "MenuItem": item["MenuItem"],
                    "AvgRating": avg_rating,
                    "SentimentScore": sentiment_score
                })

        return low_rated_negative_items


