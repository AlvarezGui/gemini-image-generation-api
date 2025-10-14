import base64

with open('./imagem_teste.jpeg', 'rb') as image_file:
    base64_bytes = base64.b64encode(image_file.read())
    print(base64_bytes)

    base64_string = base64_bytes.decode()
    print(base64_string)
