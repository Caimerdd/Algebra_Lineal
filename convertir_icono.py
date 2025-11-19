from PIL import Image

# Abre tu imagen
img = Image.open("logo_original.png")

# La guarda como icono .ico incluyendo varios tamaños para que se vea bien en todos lados
# (Windows usa tamaños desde 16x16 hasta 256x256)
img.save("icono.ico", format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])

print("¡Listo! Icono creado como 'icono.ico'")