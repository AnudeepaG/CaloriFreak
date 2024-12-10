# CaloriFreak 🍏

**CaloriFreak** is an AI-powered web app that analyzes meals for detailed nutritional insights using advanced image recognition and natural language processing.

## Features
- **Nutritional Breakdown**: Calories, macronutrients (Protein, Carbs, Fats, Fiber), and significant micronutrients.
- **Meal Classification**: Identifies meal type and balance; checks suitability for dietary preferences (e.g., vegan, keto).
- **Health Recommendations**: Suggests portion sizes, healthier alternatives, and complementary side dishes or beverages.
- **Allergy Warnings**: Flags potential allergens (e.g., nuts, dairy, gluten).
- **Cultural Insights**: Provides optional cultural or regional significance of meals.

## How It Works
1. Upload an image of your meal (JPG, JPEG, PNG).
2. Provide a short description of your meal.
3. Click **Analyze Meal** to receive a detailed report.

## Technologies
- **Frontend**: Streamlit
- **AI**: Google Gemini Pro Vision API
- **Backend**: Python, dotenv for environment variables, PIL for image handling

## Run the app:
   streamlit run app.py
