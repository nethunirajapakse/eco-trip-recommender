# eco_recommender.py
# Rule-based recommendation engine for Eco-Trip Recommender 🌿

from eco_knowledge_base import knowledge_base

def recommend_destinations(preferred_activities, preferred_climate=None):
    """
    Recommend eco-tourism destinations based on user activities and optional climate.
    """
    recommendations = []

    for place in knowledge_base:
        # Check if at least one activity matches
        if any(activity in place["activities"] for activity in preferred_activities):
            # If a preferred climate is specified, check that too
            if preferred_climate:
                if place["climate"] == preferred_climate:
                    recommendations.append(place)
            else:
                recommendations.append(place)

    return recommendations


if __name__ == "__main__":
    print("🌿 Welcome to the Eco-Trip Recommender 🌿\n")

    # User input for activities
    user_activities = input("Enter your preferred activities (comma separated): ").lower().split(",")
    user_activities = [a.strip() for a in user_activities]

    # Optional climate input
    user_climate = input("Preferred climate (optional, e.g., rainforest, dry zone): ").lower().strip()
    user_climate = user_climate if user_climate else None

    # Get recommendations
    results = recommend_destinations(user_activities, user_climate)

    # Display results
    if results:
        print("\n🌏 Recommended Destinations:")
        for place in results:
            print(f"- {place['location']} ({place['region']}) — Activities: {', '.join(place['activities'])}")
    else:
        print("\nSorry, no matching eco-destinations found.")
