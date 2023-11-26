from pathlib import Path
import matplotlib.pyplot as plt

def on_click(event):
    x = event.xdata
    y = event.ydata

    print(f'Coordenadas do clique: x={x}, y={y}')

from PIL import Image


image_path = Path('images\img2.png')

img = Image.open(image_path)
img.save(image_path)

img = plt.imread(image_path)

fig, ax = plt.subplots()
ax.imshow(img)

fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()
