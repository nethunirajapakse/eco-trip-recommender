import streamlit as st
from eco_expert_system import recommend

# Page configuration
st.set_page_config(
    page_title="CeylonWild - Eco Tourism Expert",
    page_icon="🐘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #f0fdf4 0%, #ccfbf1 50%, #cffafe 100%);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(90deg, #059669 0%, #0d9488 100%);
        padding: 3rem 2rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
        margin: -6rem -1rem 2rem -1rem;
        color: white;
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.95;
        margin-bottom: 1.5rem;
    }
    
    .stats-container {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin-top: 1.5rem;
        font-size: 0.9rem;
    }
    
    .stat-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Input section styling */
    .input-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin-bottom: 1.5rem;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
        border: 2px solid #fbbf24;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .info-box h3 {
        color: #92400e;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .info-box ul {
        color: #78350f;
        margin-left: 1rem;
    }
    
    .eco-box {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 2px solid #10b981;
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    .eco-box h3 {
        color: #065f46;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .eco-box p {
        color: #047857;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #059669 0%, #0d9488 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(5, 150, 105, 0.4);
    }
    
    /* Results styling */
    .result-card {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 2px solid #10b981;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
    }
    
    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: start;
        margin-bottom: 1rem;
    }
    
    .result-name {
        font-size: 1.3rem;
        font-weight: 700;
        color: #065f46;
        flex: 1;
    }
    
    .score-badge {
        background: #059669;
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1rem;
    }
    
    .result-details {
        color: #047857;
        font-size: 0.95rem;
        line-height: 1.8;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #059669;
        box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.1);
    }
    
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    /* Label styling */
    .stTextInput > label, .stSelectbox > label {
        font-weight: 600;
        color: #374151;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    
    /* Footer */
    .custom-footer {
        background: #1f2937;
        color: #9ca3af;
        text-align: center;
        padding: 2rem;
        border-radius: 20px 20px 0 0;
        margin: 3rem -1rem -1rem -1rem;
    }
    
    /* Success/Warning messages */
    .stSuccess {
        background: #d1fae5;
        border-left: 4px solid #10b981;
        border-radius: 8px;
    }
    
    .stWarning {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🌿 CeylonWild 🐘</h1>
    <p>Discover Sri Lanka's pristine eco-destinations through our intelligent expert system</p>
    <div class="stats-container">
        <div class="stat-item">📍 26+ Destinations</div>
        <div class="stat-item">✨ AI-Powered Matching</div>
        <div class="stat-item">🎯 Personalized Results</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main layout with columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧭 Your Preferences</div>', unsafe_allow_html=True)
    
    # Activities Input
    st.markdown("##### 📸 Activities")
    user_activities_input = st.text_input(
        "Enter your preferred activities",
        "hiking, photography",
        label_visibility="collapsed",
        help="Comma separated values (e.g., hiking, photography, bird watching)"
    )
    activities = [a.strip().lower() for a in user_activities_input.split(",") if a.strip()]
    
    st.markdown("---")
    
    # Create two columns for the select boxes
    sel_col1, sel_col2 = st.columns(2)
    
    with sel_col1:
        st.markdown("##### ⛰️ Climate")
        climates = ["any", "dry zone", "cool highland", "wet zone"]
        user_climate = st.selectbox(
            "Climate preference",
            climates,
            label_visibility="collapsed"
        )
        
        st.markdown("##### 📊 Difficulty")
        difficulties = ["any", "easy", "moderate", "hard"]
        user_difficulty = st.selectbox(
            "Difficulty level",
            difficulties,
            label_visibility="collapsed"
        )
    
    with sel_col2:
        st.markdown("##### 📍 Region")
        regions = [
            "any", "southeast sri lanka", "central sri lanka", "southern sri lanka",
            "northwest sri lanka", "north central sri lanka", "southwest sri lanka",
            "eastern sri lanka"
        ]
        user_region = st.selectbox(
            "Region preference",
            regions,
            label_visibility="collapsed"
        )
        
        st.markdown("##### ⭐ Popularity")
        popularities = ["any", "high", "medium", "low"]
        user_popularity = st.selectbox(
            "Popularity level",
            popularities,
            label_visibility="collapsed"
        )
    
    st.markdown("---")
    
    # Submit button
    submit_button = st.button("🧭 Find My Perfect Destination", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Info boxes
    st.markdown("""
    <div class="info-box">
        <h3>💡 How It Works</h3>
        <ul>
            <li>Enter your preferred activities</li>
            <li>Select your climate preferences</li>
            <li>Choose difficulty and popularity</li>
            <li>Our AI matches you with ideal spots</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="eco-box">
        <h3>🌱 Eco-Friendly</h3>
        <p>All destinations promote sustainable tourism and conservation efforts across Sri Lanka's pristine wilderness.</p>
    </div>
    """, unsafe_allow_html=True)

# Results section
if submit_button:
    if not activities:
        st.warning("⚠️ Please enter at least one activity.")
    else:
        with st.spinner("🔍 Running CeylonWild inference engine..."):
            results = recommend(
                activities,
                user_climate,
                user_region,
                user_difficulty,
                user_popularity
            )
        
        st.markdown("---")
        
        if results:
            st.success(f"✅ Found {len(results)} perfect matches for you!")
            
            st.markdown('<div class="section-title">🎯 Your Ideal Eco-Destinations</div>', unsafe_allow_html=True)
            
            # Display results in grid
            cols_per_row = 2
            for i in range(0, len(results), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(cols):
                    if i + j < len(results):
                        place = results[i + j]
                        with col:
                            st.markdown(f"""
                            <div class="result-card">
                                <div class="result-header">
                                    <div class="result-name">{place['name'].title()}</div>
                                    <div class="score-badge">{place['score']}</div>
                                </div>
                                <div class="result-details">
                                    <strong>Suitability Score:</strong> {place['score']}/100<br>
                                    Higher scores indicate better matches with your preferences
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.info("💡 **Tip:** The score represents how well each destination matches your preferences. Higher is better!")
            
        else:
            st.warning("😕 No matching destinations found for your criteria. Try adjusting your preferences!")

# Footer
st.markdown("""
<div class="custom-footer">
    <p style="font-size: 0.9rem; margin-bottom: 0.5rem;">
        🌿 <strong>CeylonWild</strong> — Sri Lanka's Eco-Tourism Expert System © 2025
    </p>
    <p style="font-size: 0.8rem; color: #6b7280;">
        Powered by CLIPS Expert System | Built for Conservation & Discovery
    </p>
</div>
""", unsafe_allow_html=True)