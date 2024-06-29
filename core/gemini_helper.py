import os

from dotenv import load_dotenv
import google.generativeai as genai
import google.generativeai as genai
from IPython.display import Image

# Used to securely store your API key

from loguru import logger

load_dotenv()
 
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
logger.debug("Available Gemini Models")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

def call_gemini(query):
            #    You will be asked a question. Your reply should include a 
            #    descriptive paragraph without any heading or bold text.
   query = f"""
               You will be asked a question. Your reply should not include Answer heading.
               Answer questions only related to fitness and nutrition domain, 
               if the following Question belong to other domain except the fitness, 
               please respond with a message that you can only answer queries related to above listed domain.
               Question: {query}
           """
   response = model.generate_content(query)
   return (response.text)

def predict_image_using_gemini(file_path):
    sample_file = genai.upload_file(path=file_path, display_name="Sample drawing")

    print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

    file = genai.get_file(name=sample_file.name)
    print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")

    response = model.generate_content(
        ["""Predict only name and calories of the Fruit or Vegetable without any description and don't parse it in json in image as illustrated below.
            name: , calories:
            And if any other image is given return response as illustrated below.
            error: Sorry I cannot recognize the given image is fruit or vegetable.
         """, sample_file]
    )

    predicted_properties = response.text

        
    # Split the string by comma
    items = predicted_properties.split(',')

    if "error" in predicted_properties:
        return {
            "name":"Not a Fruit or Vegetable",
            "calories":"None"
        }
    # Initialize an empty dictionary
    food_dict = {}

    # Loop through each item in the list
    for item in items:
        # Split each item by colon and strip any leading/trailing whitespace
        key, value = item.split(':')
        key = key.strip()
        value = value.strip()

        # Add the key-value pair to the dictionary
        food_dict[key] = value

    try:
        os.remove(file_path)
        print("File Deleted Successfully at Path: ", file_path)
    except Exception as e:
        raise e

    return food_dict