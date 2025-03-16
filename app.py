# app.py
import streamlit as st
from groq import Groq
import time
import os



# Page Configuration
st.set_page_config(
    page_title="HealthAI Advisor",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize Groq client
with st.sidebar:
    # API key input for Groq
    st.session_state["GROQ_API_KEY"] = st.text_input("GROQ API Key", type="password")
    st.sidebar.markdown("🔑 [Get Groq API Key](https://console.groq.com/keys)")
   
   
   # Initialize Groq client
if st.session_state["GROQ_API_KEY"]:            
    client = Groq(api_key=st.session_state["GROQ_API_KEY"])
else :
    client = Groq(api_key=os.environ.get("GROQ_API_KEY", st.secrets.get("GROQ_API_KEY", "sk-your-key")))

# Custom CSS
st.markdown("""
<style>
    /* Base styles */
    .recommendation-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
        background-color: var(--background-color);
        border: 1px solid var(--secondary-background-color);
        color: var(--text-color);
    }
    
    /* Theme-aware text colors */
    .st-emotion-cache-10trblm {
        color: var(--text-color) !important;
    }
    
    /* Progress bar styling */
    .st-emotion-cache-1ii7l3v {
        background-color: var(--secondary-background-color) !important;
    }
    
    .st-emotion-cache-keje6w {
        background-color: var(--primary-color) !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
def get_groq_response(prompt, model="mixtral-8x7b-32768"):
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            temperature=0.3,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def calculate_bmi(weight, height):
    return weight / ((height / 100) ** 2)

# Main App
def main():
    st.sidebar.title("🌱 Navigation")
    page = st.sidebar.radio("Choose Section", 
        ["🏠 Dashboard", "🍎 Diet Planner", "💪 Workout Generator", "🧘 Yoga Advisor", "🤖 AI Coach"])

    # Dashboard
    if page == "🏠 Dashboard":
        st.header("🏠 HealthAI Dashboard")
        st.divider()
        
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Body Metrics")
                weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=65.0)
                height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0)
                
                if st.button("Calculate BMI"):
                    bmi = calculate_bmi(weight, height)
                    st.metric("BMI", f"{bmi:.1f}")
                    
                    # Calculate progress value (0-1 scale)
                    progress_value = min(max((bmi - 15)/(40 - 15), 0), 1)
                    
                    # Create a layout for the progress bar with label
                    col_a, col_b = st.columns([4, 1])
                    with col_a:
                        st.progress(progress_value)
                    with col_b:
                        st.caption("15 ⟷ 40")
                        
                        

            with col2:
                st.subheader("Daily Goals")
                st.metric("Water Intake", "2.4L", "+0.6L remaining")
                st.metric("Steps", "8,432", "12k goal")
                st.metric("Active Minutes", "45", "60min target")

        st.divider()
        st.subheader("Weekly Progress")
        col1, col2, col3 = st.columns(3)
        col1.metric("Calories Burned", "12,430", "1,234 today")
        col2.metric("Exercise Minutes", "324", "45 today")
        col3.metric("Sleep Average", "7.2h", "-0.8h from goal")

    # Diet Planner
    elif page == "🍎 Diet Planner":
        st.header("🍎 AI Nutritionist")
        st.divider()
        
        with st.form("diet_form"):
            col1, col2 = st.columns(2)
            with col1:
                diet_goal = st.selectbox("Primary Goal", 
                    ["Weight Loss", "Muscle Gain", "Maintenance", "Improve Digestion"])
                allergies = st.multiselect("Allergies/Dietary Restrictions",
                    ["Dairy", "Gluten", "Nuts", "Eggs", "Vegetarian", "Vegan"])
            
            with col2:
                calorie_target = st.slider("Daily Calorie Target", 1200, 3000, 2000)
                preferred_cuisine = st.selectbox("Preferred Cuisine",
                    ["Any", "Mediterranean", "Asian", "Mexican", "Continental"])
            
            if st.form_submit_button("🍳 Generate Meal Plan"):
                with st.spinner("Cooking up your personalized plan..."):
                    prompt = f"""Create a {diet_goal} meal plan for {calorie_target} calories, 
                        considering {allergies} restrictions and {preferred_cuisine} cuisine preference. 
                        Include breakfast, lunch, dinner, and snacks with macros with attractive emogies and attractive format"""
                    response = get_groq_response(prompt)
                    st.subheader("🍽️ Your Personalized Meal Plan")
                    st.markdown(f'<div class="recommendation-box">\n\n{response}</div>', unsafe_allow_html=True)
                    

    # Workout Generator
    elif page == "💪 Workout Generator":
        st.header("💪 AI Fitness Coacht")
        st.divider()
        
        with st.form("workout_form"):
            col1, col2 = st.columns(2)
            with col1:
                fitness_level = st.selectbox("Fitness Level", 
                    ["Beginner", "Intermediate", "Advanced"])
                workout_type = st.selectbox("Workout Type",
                    ["Full Body", "Upper Body", "Lower Body", "Cardio", "HIIT"])
            
            with col2:
                equipment = st.multiselect("Available Equipment",
                    ["Dumbbells", "Resistance Bands", "None", "Barbell", "Kettlebells"])
                duration = st.slider("Duration (minutes)", 15, 120, 45)
            
            if st.form_submit_button("🏋️ Generate Workout"):
                with st.spinner("Building your workout routine..."):
                    prompt = f"""Create a {duration}-minute {workout_type} workout for a {fitness_level} 
                        using {equipment}. Include warm-up, exercises with sets/reps, and cool-down with attractive emogies and attractive format"""
                    response = get_groq_response(prompt)
                    st.subheader("📝 Your Custom Workout Plan")
                    st.markdown(f'<div class="recommendation-box">\n\n{response}</div>', unsafe_allow_html=True)

    # Yoga Advisor
    elif page == "🧘 Yoga Advisor":
        st.header("🧘 AI Yoga Guide")
        st.divider()
        with st.form("yoga_form"):
            col1, col2 = st.columns(2)
            with col1:
                yoga_goal = st.selectbox("Session Focus",
                    ["Stress Relief", "Flexibility", "Strength", "Balance", "Morning Energy"])
                experience_level = st.selectbox("Experience Level",
                    ["Beginner", "Intermediate", "Advanced"])
            
            with col2:
                duration = st.slider("Session Duration (minutes)", 10, 90, 30)
                intensity = st.select_slider("Intensity", 
                    options=["Gentle", "Moderate", "Vigorous"])
            
            if st.form_submit_button("🧘 Generate Yoga Routine"):
                with st.spinner("Creating your zen session..."):
                    prompt = f"""Create a {duration}-minute {yoga_goal} yoga routine for {experience_level} 
                        practitioners with {intensity} intensity. Include warm-up, sequence of poses, 
                        and final relaxation with attractive emogies and attractive format"""
                    response = get_groq_response(prompt)
                    st.subheader("🌸 Your Yoga Sequence")
                    st.markdown(f'<div class="recommendation-box">\n\n{response}</div>', unsafe_allow_html=True)

    # AI Coach
    elif page == "🤖 AI Coach":
        st.markdown('<p class="header-text">AI Wellness Coach</p>', unsafe_allow_html=True)
        st.header("🤖 AI Wellness Coach")
        st.divider()
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("Ask about health, nutrition, or fitness..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    response = get_groq_response(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()