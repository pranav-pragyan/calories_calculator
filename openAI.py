from secret import openAI_API_Key
from openai import OpenAI
import streamlit as st
from PIL import Image
import base64
import requests
from io import BytesIO

class CaloriesCalculator:
    def __init__(self, prompt):
        self.__prompt = prompt
        self.__model = "gpt-4-vision-preview"
        self.__openai_key = openAI_API_Key

    def get_response(self, img, file_extention):
        buffered = BytesIO()
        img.save(buffered, format = file_extention)
        img = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        message = [
            {
                "role" : "user",
                "content" : [
                    {
                        "type" : "text",
                        "text" : self.__prompt
                    },
                    {
                        "type" : "image_url",
                        "image_url": {
                            "url" : f"data:image/{file_extention};base64,{img}"
                        }
                    }
                ]
            }
        ]
        payload = {
            "model" : self.__model,
            "messages" : message,
            "max_tokens": 300
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.__openai_key}"
                }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response = response.json()
        return response["choices"][0]['message']['content']

if __name__ == '__main__':

    prompt = ''' You are an expert nutritionist. Your task is to look into the given image and find out all the food items
                 there. Calculate the calories for each food item and return those in the given format -

                 1. Item 1 - no of calories
                 2. Item 2 - no of calories
                 ----
                 ----
                 Total calories: Mention the total calories here (estimate).

                 Give a very short summary about the food, mention whether the food is healthy or not.
                 Make the word healthy/unhealthy bold.
                 Follow the above given mention instructions only and don't include extra informations.

             '''
    calories_calculator = CaloriesCalculator(prompt)

    st.header("Calories Checker")
    st.title("Get Nutrition Value for Food Image...")

    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    file_extention = str(uploaded_image.type).split("/")[-1]
    img = ""
    if uploaded_image:
        img = Image.open(uploaded_image)
        st.image(image=img, caption="Uploaded Image...", use_column_width=True)
    
    submit = st.button("Get Facts...")
    if submit:
        response = calories_calculator.get_response(img, file_extention)
        st.subheader("The response is...")
        st.write(response)
        st.subheader("\nGet Info For Other Image...")