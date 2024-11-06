### Health Management APP
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app
st.set_page_config(page_title="Gemini Health App")
st.header("Gemini Health App")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button("Tell me the total calories")
input_prompt = """
               You are an expert nutritionist who analyzes the food items in an image and calculates the total calories. 
               Please provide a detailed breakdown of every food item in the following format:

               1. Item 1 - number of calories, protein, carbs, fats, dietary fiber, etc.
               2. Item 2 - number of calories, protein, carbs, fats, dietary fiber, etc.
               ----
               ----
               
               Also:
               - Summarize the overall meal by category (e.g., main meal, snack, dessert).
               - Suggest healthier alternatives if available.
               - Provide portion size recommendations for optimal calorie intake.
               - Indicate if each item fits specific dietary requirements (e.g., keto, vegan, gluten-free).
               """
## If submit button is clicked
if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)

