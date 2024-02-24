from secret import GOOGLE_API_KEY
import google.generativeai as genai
from PIL import Image
import streamlit as st

class CaloriesCalculator:
    def __init__(self, prompt):
        self.__prompt = prompt
        self.__gemini_api_key = GOOGLE_API_KEY
        genai.configure(api_key=self.__gemini_api_key)
        self.__model_name = "gemini-pro-vision"
        self.__model = genai.GenerativeModel(self.__model_name)
        
    def get_response(self, img):
        response = self.__model.generate_content([self.__prompt,img])
        return response.text

if __name__ == '__main__':

    prompt = ''' You are an expert nutritionist. Your task is to look into the given image and find out all the food items
                 there. Calculate the calories for each food item and return those in the given format -

                 1. Item 1 - no of calories
                 2. Item 2 - no of calories
                 ----
                 ----

                 Also mention the total calories for the food. 
                 Give a very short summary about the food, mention whether the food is healthy or not.
             '''
    calories_calculator = CaloriesCalculator(prompt)    

    st.header("Calories Checker")
    st.title("Get Nutrition Value for Food Image...")

    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    img = ""
    if uploaded_image:
        img = Image.open(uploaded_image)
        st.image(image=img, caption="Uploaded Image...", use_column_width=True)
    
    submit = st.button("Get Facts...")
    if submit:
        response = calories_calculator.get_response(img)
        st.subheader("The response is...")
        st.write(response)
        st.subheader("\nGet Info For Other Image...")