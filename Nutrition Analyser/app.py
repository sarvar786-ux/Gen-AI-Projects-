import streamlit as st
from PIL import Image
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from gemini_api import analyze_food_image, generate_health_summary
from nutrition_utils import get_nutrition_info, generate_diet_recommendations

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="Nutritionist GenAI Doctor", page_icon="🍏", layout="wide")

# ------------------- TITLE -------------------
st.title("🍏 Nutritionist GenAI Doctor")
st.write("Upload an image of your meal to get calorie and nutrition insights!")

# ------------------- FILE UPLOAD -------------------
uploaded_file = st.file_uploader("Choose a food image...", type=["jpg", "jpeg", "png"])

# ------------------- MAIN PROCESS -------------------
if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Food Image", use_container_width=True)

    st.write("Analyzing image... 🔍")

    image_path = "temp_food_image.jpg"
    image.save(image_path)

    # -------- Step 1: Detect Food --------
    food_items = analyze_food_image(image_path)

    if food_items:
        st.success(f"Detected food items: {', '.join(food_items)}")

        # -------- Step 2: Nutrition Info --------
        details, summary = get_nutrition_info(food_items)

        if details:

            # ------------------- Nutrition Table -------------------
            st.subheader("Nutrition Details per Food Item")
            st.table(pd.DataFrame(details))

            # ------------------- Meal Summary Metrics -------------------
            st.subheader("Meal Summary")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Calories", summary["Total Calories"])
            col2.metric("Protein (g)", summary["Total Protein"])
            col3.metric("Fat (g)", summary["Total Fat"])
            col4.metric("Carbs (g)", summary["Total Carbs"])

            # ------------------- Calorie Gauge Chart -------------------
            st.subheader("Calorie Intake Gauge")

            calories = summary["Total Calories"]

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=calories,
                title={'text': "Calories Consumed"},
                gauge={
                    'axis': {'range': [0, 2500]},
                    'bar': {'thickness': 0.3},
                    'steps': [
                        {'range': [0, 800], 'color': "lightgreen"},
                        {'range': [800, 1600], 'color': "yellow"},
                        {'range': [1600, 2500], 'color': "red"}
                    ],
                }
            ))

            st.plotly_chart(fig, use_container_width=True)

            # ------------------- Macronutrient Pie Chart -------------------
            st.subheader("Macronutrient Distribution")

            macro_data = {
                "Nutrient": ["Protein", "Fat", "Carbs"],
                "Value": [
                    summary["Total Protein"],
                    summary["Total Fat"],
                    summary["Total Carbs"]
                ]
            }

            pie_fig = px.pie(
                macro_data,
                names="Nutrient",
                values="Value",
                title="Macronutrient Breakdown"
            )

            st.plotly_chart(pie_fig, use_container_width=True)

            # ------------------- Diet Recommendations -------------------
            st.subheader("Diet Recommendations")

            recommendations = generate_diet_recommendations(summary)

            for rec in recommendations:
                st.write(f"• {rec}")

            # ------------------- AI Health Suggestions -------------------
            st.subheader("🤖 AI Health Suggestions")

            ai_summary = generate_health_summary(summary)

            st.info(ai_summary)

        else:
            st.warning("No matching food items found in the nutrition dataset.")

    else:
        st.warning("No food items detected. Try uploading a clearer image.")
