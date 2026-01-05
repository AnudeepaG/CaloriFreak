'''from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure the Google Gemini API with API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get a response
def get_nutrition_analysis(image_data, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt, image_data[0]])
    return response.text

# Function to prepare uploaded image data
def prepare_image_data(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    else:
        raise FileNotFoundError("Please upload an image.")

# Initialize Streamlit app configuration
st.set_page_config(
    page_title="NutriVision Health Tracker",
    page_icon="🍏",
    layout="centered"
)

# App Header and Subheader
st.title("NutriVision Health Tracker")
st.subheader("Analyze your meal's nutritional information instantly!")

# Input prompt for the user and image upload functionality
user_prompt = st.text_input("Describe your meal:", key="user_prompt")
uploaded_file = st.file_uploader("Upload a meal image (jpg, jpeg, png):", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)


# Submit button and response section
if st.button("Analyze Meal"):
    try:
        image_data = prepare_image_data(uploaded_file)
        
        # Improved prompt
        prompt = """
        You are an expert nutritionist and food analyst. Your task is to analyze the image of a meal provided and generate a detailed nutritional breakdown along with other insightful recommendations. Follow this structured format to present the analysis:

        1. **Nutritional Breakdown**:
           - **For each identifiable item in the meal**:
             - Name of the item
             - Calories: xx kcal
             - Macronutrients: Protein (xxg), Carbs (xxg), Fats (xxg), Fiber (xxg)
             - Micronutrients: Mention any significant vitamins or minerals (e.g., Vitamin A, Iron, Calcium).

        2. **Meal Analysis**:
           - Classify the meal type (e.g., breakfast, main course, snack, dessert).
           - Identify whether the meal is balanced (covers essential food groups).
           - Highlight any prominent ingredients or cooking styles (e.g., fried, baked, steamed).
           - Comment on the meal's suitability for dietary restrictions (e.g., vegan, keto, gluten-free, low-carb).

        3. **Health Recommendations**:
           - Suggest healthier alternatives for high-calorie or nutrient-deficient items.
           - Recommend appropriate portion sizes to align with a 2,000 kcal daily diet or a custom dietary goal.

        4. **Allergy and Intolerance Warnings**:
           - Flag potential allergens (e.g., nuts, dairy, gluten) based on the identified items.

        5. **Meal Optimization**:
           - Suggest how the meal could be modified for specific goals (e.g., weight loss, muscle gain, improved digestion).
           - Recommend side dishes or beverages to complement the meal.

        6. **Cultural or Regional Insights (Optional)**:
           - Provide a brief note if the meal corresponds to any specific cultural, seasonal, or regional food habits.

        **Additional Notes**:
        - Ensure the response is concise, well-structured, and easy to understand.
        - If any part of the meal cannot be analyzed confidently, mention it clearly.
        - Use friendly and engaging language while maintaining professionalism.
        """

        response = get_nutrition_analysis(image_data, prompt)
        st.subheader("Nutrition Analysis:")
        st.write(response)
    except FileNotFoundError as e:
        st.error(str(e))
    except Exception as e:
        st.error("An error occurred while analyzing the image. Please try again.")

# Apply custom CSS for a smoother and more stylish UI
st.markdown("""
    <style>
        .stButton>button {
            background-color: #2ecc71;
            color: white;
            font-size: 18px;
            border-radius: 8px;
            padding: 10px 20px;
        }
        .stTextInput>div>input {
            font-size: 16px;
            border-radius: 8px;
            border: 1px solid #ddd;
            padding: 8px;
            width: 100%;
        }
        .stFileUploader {
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        .stApp {
            background-color: black;
        }
    </style>
""", unsafe_allow_html=True)'''




from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# ---- Env & API config ----
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.set_page_config(page_title="NutriVision Health Tracker", page_icon="🍏", layout="centered")
    st.error("Missing GOOGLE_API_KEY in environment. Please add it to your .env file.")
    st.stop()
genai.configure(api_key=api_key)

# ---- Gemini Vision call ----
def get_nutrition_analysis(image_data, prompt: str) -> str:
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content([prompt, image_data[0]])
    return getattr(response, "text", "") or ""

# ---- Prepare uploaded image ----
def prepare_image_data(uploaded_file):
    if uploaded_file is None:
        raise FileNotFoundError("Please upload an image.")
    bytes_data = uploaded_file.getvalue()
    mime = uploaded_file.type or "image/jpeg"
    return [{"mime_type": mime, "data": bytes_data}]

# ---- Streamlit UI ----
st.set_page_config(page_title="NutriVision Health Tracker", page_icon="🍏", layout="centered")
st.title("NutriVision Health Tracker")
st.subheader("Analyze your meal's nutritional information instantly!")

user_prompt = st.text_input("Describe your meal (optional):", key="user_prompt", help="Add context like ingredients, cuisine, or portion size.")
uploaded_file = st.file_uploader("Upload a meal image (jpg, jpeg, png):", type=["jpg", "jpeg", "png"])

# Preview
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Analyze
if st.button("Analyze Meal", disabled=uploaded_file is None):
    try:
        image_data = prepare_image_data(uploaded_file)

        base_prompt = """
        You are an expert nutritionist and food analyst. Analyze the uploaded meal image and produce a structured report:

        1) Nutritional Breakdown
           - For each identifiable item:
             - Name
             - Calories (kcal)
             - Macronutrients: Protein (g), Carbs (g), Fats (g), Fiber (g)
             - Key micronutrients (e.g., Vitamin A, Iron, Calcium)

        2) Meal Analysis
           - Meal type (breakfast/lunch/snack/dessert)
           - Whether the meal is balanced (food groups covered)
           - Notable ingredients & cooking style (fried/baked/steamed)
           - Suitability for common diets (vegan/keto/gluten-free/low-carb)

        3) Health Recommendations
           - Healthier alternatives for high-calorie or nutrient-poor items
           - Portion guidance (assume 2,000 kcal/day unless otherwise stated)

        4) Allergy & Intolerance Warnings
           - Potential allergens (nuts, dairy, gluten, etc.)

        5) Meal Optimization
           - Modifications for weight loss/muscle gain/digestion
           - Complementary sides or beverages

        6) Cultural/Regional Insights (optional)
           - Note any relevant cuisine or seasonal context

        - Be concise and clear; flag uncertainties explicitly.
        - Use friendly, professional language.
        """

        effective_prompt = f"{user_prompt}\n\n{base_prompt}" if user_prompt.strip() else base_prompt
        response_text = get_nutrition_analysis(image_data, effective_prompt)

        st.subheader("Nutrition Analysis:")
        if response_text:
            st.write(response_text)
        else:
            st.warning("No analysis returned. Try adding a short description of the meal or upload a clearer image.")

    except FileNotFoundError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"An error occurred while analyzing the image: {e}")

# ---- CSS ----
st.markdown("""
    <style>
        .stButton>button {
            background-color: #2ecc71;
            color: white;
            font-size: 18px;
            border-radius: 8px;
            padding: 10px 20px;
        }
        .stTextInput>div>input {
            font-size: 16px;
            border-radius: 8px;
            border: 1px solid #ddd;
            padding: 8px;
            width: 100%;
        }
        .stFileUploader {
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        .stApp {
            background-color: black;
        }
    </style>
""", unsafe_allow_html=True)
