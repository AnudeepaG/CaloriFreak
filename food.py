from dotenv import load_dotenv
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
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Submit button and response section
if st.button("Analyze Meal"):
    try:
        image_data = prepare_image_data(uploaded_file)
        prompt = """
            You are an expert nutritionist who analyzes food items in an image and provides a comprehensive nutritional breakdown.
            Please use the following format:

            1. Item - Calories: xx, Protein: xxg, Carbs: xxg, Fats: xxg, Fiber: xxg
            2. Item - Calories: xx, Protein: xxg, Carbs: xxg, Fats: xxg, Fiber: xxg
            ----
            ----
            
            Additionally:
            - Summarize the meal type (e.g., main course, snack, dessert).
            - Suggest healthier alternatives if possible.
            - Offer portion size recommendations for optimal calorie intake.
            - Indicate if the item fits specific dietary requirements (e.g., keto, vegan, gluten-free).
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
""", unsafe_allow_html=True)
