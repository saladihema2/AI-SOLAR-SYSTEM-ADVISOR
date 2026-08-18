import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Page configuration
st.set_page_config(
    page_title="AI Solar System Advisor",
    page_icon="☀️",
    layout="centered"
)

# Title
st.title("AI Solar System Advisor")
st.write("Get a simple solar system recommendation based on your electricity usage.")

# User inputs
st.header("Enter Your Electricity Details")

location = st.text_input(
    "Location",
    placeholder="Example: Vijayawada"
)

monthly_bill = st.number_input(
    "Average Monthly Electricity Bill (₹)",
    min_value=0,
    value=2000
)

sun_hours = st.number_input(
    "Average Sunlight Hours per Day",
    min_value=1.0,
    max_value=12.0,
    value=5.0
)

st.subheader("Appliances")

fans = st.number_input("Number of Fans", min_value=0, value=3)
lights = st.number_input("Number of Lights", min_value=0, value=5)
tv = st.number_input("Number of TVs", min_value=0, value=1)
refrigerator = st.number_input("Number of Refrigerators", min_value=0, value=1)
ac = st.number_input("Number of ACs", min_value=0, value=0)

daily_hours = st.number_input(
    "Average Appliance Usage per Day (hours)",
    min_value=1.0,
    max_value=24.0,
    value=6.0
)

# Calculate approximate load
estimated_load = (
    fans * 75 +
    lights * 15 +
    tv * 100 +
    refrigerator * 150 +
    ac * 1500
)

st.info(f"Estimated Connected Load: {estimated_load} Watts")

# Advisor button
if st.button("Get Solar Recommendation"):

    prompt = f"""
You are an AI Solar System Advisor.

Analyze the following household electricity information:

Location: {location}
Monthly Electricity Bill: ₹{monthly_bill}
Average Sunlight Hours: {sun_hours} hours/day

Appliances:
Fans: {fans}
Lights: {lights}
TVs: {tv}
Refrigerators: {refrigerator}
ACs: {ac}

Estimated Connected Load: {estimated_load} Watts
Average Usage: {daily_hours} hours/day

Provide a simple and easy-to-understand recommendation.

Include:
1. Estimated daily electricity consumption.
2. Approximate monthly electricity consumption.
3. Suggested solar system size in kW.
4. Approximate number of solar panels.
5. Suggested battery capacity if battery backup is required.
6. Approximate inverter capacity.
7. Estimated advantages of using solar power.
8. Energy-saving tips.

Clearly mention that these are approximate educational estimates
and a qualified solar professional should verify the final system design.
"""

    with st.spinner("Analyzing your solar requirements..."):

        response = client.chat.completions.create(
            model="meta-llama/llama-prompt-guard-2-22m",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        result = response.choices[0].message.content

    st.success("Solar recommendation generated!")

    st.subheader("☀️ Your Solar Recommendation")
    st.write(result)