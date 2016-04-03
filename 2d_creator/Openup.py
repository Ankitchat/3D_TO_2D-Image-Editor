import numpy as np
import cv2
from matplotlib import pyplot as plt
from Tkinter import Tk
from tkFileDialog import askopenfilename
from Anime_style import Get_Outline

Tk().withdraw() 
filename = askopenfilename()
obj = Get_Outline()
obj.default_layout(filename)
