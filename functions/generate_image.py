from google import genai
from google.genai import types
from .convert_image import convert_to_base64
import os

client = genai.Client()
image_path = "./temp_image.png"

def generate_image(prompt):
    try:
        response = client.models.generate_images(
                model='imagen-4.0-generate-001',
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images= 1,
                )
        )
        for generated_image in response.generated_images:
            generated_image.image.save(image_path)
            image_base64 = convert_to_base64(image_path)
            if os.path.exists(image_path):
                    os.remove(image_path)
        return image_base64
    except Exception as err:
        print(f"Erro em gerar a imagem: {err}")
        return None
