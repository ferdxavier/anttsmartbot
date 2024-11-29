import easyocr

# Carregar imagem
imagem = 'image2.jpg'

# Criar objeto EasyOCR
reader = easyocr.Reader(['pt'])  # Idioma português

# Extrair texto
texto = reader.readtext(imagem)

# Imprimir texto
for item in texto:
    print(item[1])