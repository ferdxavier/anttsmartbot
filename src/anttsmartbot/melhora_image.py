from PIL import Image, ImageEnhance

# Abre a imagem
img = Image.open("image.jpeg")

# Aumenta o contraste
enhancer = ImageEnhance.Contrast(img)
img_contrast = enhancer.enhance(1.5)

# Salva a imagem com contraste aumentado
img_contrast.save("imagem_contrast.jpeg")