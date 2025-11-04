from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
from functions.convert_image import convert_to_base64


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# user = "admin"

# prompt = (
#     ler_prompt(user)
# )

# print(prompt)

# response = client.models.generate_content(
#     model="gemini-2.5-flash-image-preview",
#     contents=[prompt],
# )

# for part in response.candidates[0].content.parts:
#     if part.text is not None:
#         print(part.text)
#     elif part.inline_data is not None:
        # image = Image.open(BytesIO(part.inline_data.data))
        # image.save("generated_image.png")
        
def generate_image(prompt):
    image = "./imagem_teste.jpeg"
    return convert_to_base64(image)
