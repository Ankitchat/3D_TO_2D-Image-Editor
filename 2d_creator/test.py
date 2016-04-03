from Tkinter import *
from PIL import ImageTk,Image,ImageDraw
import math


def method(canvas):
    image = Image.open('editable.jpg')
    drawing_area = canvas
    resized = image.resize((500,500),Image.ANTIALIAS)
    render_image = ImageTk.PhotoImage(resized,master=drawing_area)
    draw = ImageDraw.Draw(image)
    drawing_area.create_image(0, 0,image=render_image, anchor=NW)
    drawing_area.image = render_image
    drawing_area.pack()
    return drawing_area


root = Tk()
drawing = Canvas(root,width = 500, height =500)
drawing = method(drawing)
root.mainloop()

