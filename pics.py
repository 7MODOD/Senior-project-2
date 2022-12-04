import numpy as np
from PIL import Image


for x in range(0, 100):
    TheImage = np.array(Image.open("D:/Images/1.png"))

    img = Image.fromarray(TheImage)
print("hello world")
