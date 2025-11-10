from google import genai
from google.genai import types
from .convert_image import convert_to_base64
from PIL import Image
from io import BytesIO

client = genai.Client()

def generate_image(prompt):
        response = client.models.generate_images(
                model='imagen-4.0-generate-001',
                prompt=prompt,
                config=types.GenerateImagesConfig(
                        number_of_images= 1,
        )
        )
        for generated_image in response.generated_images:
                generated_image.image.save("./temp_image.png")
                return convert_to_base64("./temp_image.png")
