import base64

def convert_to_base64(image):
    with open(image, 'rb') as image_file:
        base64_bytes = base64.b64encode(image_file.read())
        base64_string = base64_bytes.decode()
        return base64_string
