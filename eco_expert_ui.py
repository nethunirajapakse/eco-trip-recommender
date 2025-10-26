import streamlit as st
from eco_expert_system import recommend

st.set_page_config(page_title="Eco-Trip Recommender", page_icon="🌿")

st.title("🌿 Eco-Trip Expert System 🌿")
st.write("Get eco-tourism destination recommendations based on your preferred activities.")

# Input: activities
user_activities = st.text_input(
    "Enter your preferred activities (comma separated):", "hiking, photography"
)
activities = [a.strip().lower() for a in user_activities.split(",") if a.strip()]

if st.button("Get Recommendations"):
    if activities:
        st.write("🔍 Running inference engine...")
        results = recommend(activities)

        if results:
            st.success("✅ Recommended Destinations:")
            for place in results:
                st.write(f"- {place['name']}")
        else:
            st.warning("😕 No matching destinations found.")
