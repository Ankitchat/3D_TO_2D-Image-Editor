##        Although Named Paint It si Only used to create Hair Or Bangs.
##        Until Grayscale It will create Leaf Like Pattern Over The Image.
##        Paint File is an earliar interpretation of developed code and hence
##        is not a class based interpretaion It follow Two sets of method namely
##        1. Create editable to Create Hair includes Function called:
##            i. b1up
##            ii. b1down
##            iii. b1motion
##            iv. b2down
##        2. Identically Create Bang creates Bangs and include:
##            i. b1up2
##            ii. b1down2
##            iii. b1motion2
##            iv. b2down2
##
##        Using the Functions Left click initiallly creates a line which is used to draw hairs.
##        On right click width of hair could be extended.
##        Motion Increases Length Of HAIRS.
##        Fixes and Update would Require Colour.

from Tkinter import *
from PIL import ImageTk,Image,ImageDraw
import math

b1 = "up"
xold, yold = None, None
xlold, ylold = None, None
created=0
distance = 0
drawing_area = None
source = None
image= None
draw= None

def create_editable(src,window):
    global drawing_area,source,image,draw
    source=src
    image = Image.open(src)
    drawing_area = window
    image = image.resize((500,500),Image.ANTIALIAS)
    render_image = ImageTk.PhotoImage(image,master=drawing_area)
    draw = ImageDraw.Draw(image)
    drawing_area.delete("IMG")
    drawing_area.create_image(0, 0,image=render_image, anchor=NW,tag="IMG")
    drawing_area.image = render_image
    drawing_area.pack()
    drawing_area.bind("<Motion>", motion)
    drawing_area.bind("<ButtonPress-1>", b1down)
    drawing_area.bind("<ButtonPress-3>", b2down)
    drawing_area.bind("<ButtonRelease-1>", b1up)
    drawing_area.bind("<Configure>", resize)

def create_Bangs(src,window):
    global drawing_area,source,image,draw
    source=src
    image = Image.open(src)
    drawing_area = window
    image = image.resize((500,500),Image.ANTIALIAS)
    render_image = ImageTk.PhotoImage(image,master=drawing_area)
    draw = ImageDraw.Draw(image)
    drawing_area.delete("IMG")
    drawing_area.create_image(0, 0,image=render_image, anchor=NW,tag="IMG")
    drawing_area.image = render_image
    drawing_area.pack()
    drawing_area.bind("<Motion>", motion2)
    drawing_area.bind("<ButtonPress-1>", b1down2)
    drawing_area.bind("<ButtonPress-3>", b2down2)
    drawing_area.bind("<ButtonRelease-1>", b1up2)
    drawing_area.bind("<Configure>", resize)
    

def resize(event):
    global image,source,drawing_area,draw
    size = (event.width, event.height)
    image = Image.open(source)
    image = original.resize(size,Image.ANTIALIAS)
    render_image = ImageTk.PhotoImage(image,master=drawing_area)
    draw = ImageDraw.Draw(image)
    drawing_area.delete("IMG")
    drawing_area.create_image(0, 0,image=render_image, anchor=NW, tags="IMG")       
    

def b1down(event):
    global b1,distance,created,drawing_area,xlold,ylold,xold,yold,draw
    b1 = "down"
    if created == 0:
        line = drawing_area.create_line(event.x,event.y,event.x+10,event.y)
        draw.line(((event.x,event.y),(event.x+10,event.y)),fill=0)
        xold = event.x
        yold = event.y
        xlold = event.x+10
        ylold = event.y
        print("done")
        created = 1
        distance = 10

def b2down(event):
    global distance,draw
    if created == 1:
        drawing_area.delete("line")
        line = drawing_area.create_line(event.x,event.y,event.x+distance+1,event.y)
        draw.line(((event.x,event.y),(event.x+distance+1,event.y)),fill=0)
        xold = event.x
        yold = event.y
        xlold = event.x+distance
        ylold = event.y
        distance= distance + 10      
    
    
def b1up(event):
    global b1, xold, yold,xlold,ylold,created,drawing_area,image,draw
    b1 = "up"
    xold = None           
    yold = None
    xlold = None           
    ylold = None
    created=0
    filename = "editable.jpg"
    image.save(filename)

def motion(event):
    global distance
    if b1 == "down" and distance > 0:
        global xold, yold,created,distance,xlold,ylold,draw
        if xold is not None and yold is not None:
            try:
                m = (yold-ylold)/(xold-xlold)
            except:
                m=0
            print(distance)
            x2 = ((distance-1)/math.sqrt(abs(m)+1))+event.x
            y2 = (x2-event.x)*m + event.y
            print(xold,yold,event.x,event.y)
            print(xlold,ylold,x2,y2)
            event.widget.create_line(xold,yold,event.x,event.y)
            draw.line(((xold,yold),(event.x,event.y)))
            event.widget.create_line(xlold,ylold,x2,y2)
            draw.line(((xlold,ylold),(x2,y2)))
            xlold = x2
            ylold = y2
            distance = distance-1
        xold = event.x
        yold = event.y
        


def b1down2(event):
    global b1,distance,created,drawing_area,xlold,ylold,xold,yold,xl2old,yl2old
    b1 = "down"
    if created == 0:
        line = drawing_area.create_line(event.x,event.y,event.x+10,event.y)
        draw.line(((event.x,event.y),(event.x+10,event.y)),fill=0)
        line2 = drawing_area.create_line(event.x,event.y,event.x-10,event.y)
        draw.line(((event.x,event.y),(event.x-10,event.y)),fill=0)
        xold = event.x
        yold = event.y
        xlold = event.x+10
        ylold = event.y
        xl2old = event.x-10
        yl2old = event.y
        print("done")
        created = 1
        distance = 10
        
    
    
def b1up2(event):
    global b1, xold, yold,xlold,ylold,xl2old,yl2old,created
    b1 = "up"
    xold = None           
    yold = None
    xlold = None           
    ylold = None
    xl2old = None           
    yl2old = None
    created=0
    filename = "editable.jpg"
    image.save(filename)
    

def b2down2(event):
    global distance
    if created == 1:
        drawing_area.delete("line")
        line = drawing_area.create_line(event.x,event.y,event.x+distance+1,event.y)
        draw.line(((event.x,event.y),(event.x+distance+1,event.y)),fill=0)
        xold = event.x
        yold = event.y
        xlold = event.x+distance
        ylold = event.y
        distance= distance + 10
        

def motion2(event):
    if b1 == "down":
        global xold, yold,created,distance,xlold,ylold,xl2old,yl2old
        if xold is not None and yold is not None:
            try:
                m = (yold-ylold)/(xold-xlold)
            except:
                m=0
            x2 = ((distance-1)/math.sqrt(abs(m)+1))+event.x
            y2 = (x2-event.x)*m + event.y
            m2 = (yold-yl2old)/(xold-xl2old)
            x22 = ((-distance+1)/math.sqrt(abs(m)+1))+event.x
            y22 = (x22-event.x)*m2 + event.y
            event.widget.create_line(xold,yold,event.x,event.y)
            event.widget.create_line(xl2old,yl2old,x22,y22)
            draw.line(((xl2old,yl2old),(x22,y22)),fill=0)
            event.widget.create_line(xlold,ylold,x2,y2)
            draw.line(((xlold,ylold),(x2,y2)),fill=0)
            xlold = x2
            ylold = y2
            xl2old = x22
            yl2old = y22
            distance = distance-1
        xold = event.x
        yold = event.y





