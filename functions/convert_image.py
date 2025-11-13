import base64

def convert_to_base64(image_path):
    try:
        with open(image_path, 'rb') as image_file:
                base64_string = base64.b64encode(image_file.read()).decode()
                return base64_string
    except Exception as err:
        print(f"Falha em converter a imagem {image_path}: {err}")
        return None
