# The First GUI functions to be loaded.
# Anime_style contains variedity of face building operations with the help of geometric Polygons and shapes.
# Contains a single class called Getoutline with various body functions to comprehend human body.
# For testing purpose Anime_style could be used through callling Getoutline object and runningthe appropriate
# function regardingly.
# It is subtely easy to implement and as a whole most important and basic function to be called would be
# default_layout.
# For further future use , new body part must be added here and accordingly ShapeMaker object must be created
# which would have respective coordinates.
# ______________Future Methods to be Added______________________
#   - Ear
#   - hand
#   - chest
#   - feet
#   - reflection
# Any updated version of code could be added at the End of the file.


import cv2
import numpy as np
from matplotlib import pyplot as plt
from Tkinter import *
from PIL import ImageTk,Image
import Tkinter
from paint import create_editable,create_Bangs
from Shapes import ShapeMaker



class Get_Outline:

    # Class Get_Outline consists of various method to apprehand a human face case.
    # Methods of class are not arranged in alphabetical order and are rather random to
    # encounter.
    # To understand the workFlow of class just follow through starting from method default_layout.
    # Class starts Tkinter window and contains the mainloop() of the program.
    # Class was built as a wrapper to consitute Shapemaker class.
    # Code implements the use of both Tkinter using classes and solely as methods too.
    # Initilizes whole window in two parts containg : -
    #               1. Canvas to hold image.
    #               2. Buttons to perform operations.
    # Creates a file called 'editable.jpg' to store the result.
    
    def __init__(self):
        self.root = Tk()
        frame2 = Frame(self.root)
        frame2.pack()
        self.canvas = Canvas(frame2,width = 500, height = 500)
        self.current = None
           

    def outliner(self,src):
        
##        """ It is made over Opencv to get Outline of Human figure.
##            It makes Grayscale image called editable.jpg.
##            Method could be commented if colour is required.
##            To comment method remove method name from default_layout program.
##            Rename the file you want to operate as editable.jpg and place it
##            in current directory.Then access default_layout."""
        
        gray_img = cv2.imread(src,0)
        img = cv2.imread(src)
        (h,w)  = img.shape[:2]
        for i in range(0,h):
            for j in range(0,w):
                pixel_r = gray_img[i,j]
                if pixel_r>115:
                    img[i,j,0] = 255
                    img[i,j,1] = 255
                    img[i,j,2] = 255

        gimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        cv2.imwrite('editable.jpg',gimg)
        

    def switch_function(self):
        
##        """ Used as switch to calll different functions.
##            It is required because Tkinter window can only use lambda functions."""
##        
        if self.current == 0:
            create_editable('editable.jpg',self.canvas)
        if self.current == 1:
            create_Bangs('editable.jpg',self.canvas)
        if self.current == 2:
            self.nose()
        if self.current == 3:
            self.mouth()
        if self.current == 4:
            self.right_eye()
        if self.current == 5:
            self.left_eye()
        if self.current == 6:
            self.eyebrows()
        if self.current == 7:
            self.neck()

    def get_rid(self):

##        """ Get rid of previously Binded data."""
        
        self.canvas.delete("all")
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<Triple-Button-1>")
        self.canvas.unbind("<Double-Button-1>")
        
            

    def change_current(self,i):

##        """ Calls switched functions."""
        
        self.current = i
        self.get_rid()
        self.switch_function()
        

    def default_layout(self,src):
##
##        """
##        Required method do not remove or edit this until more button are needed to be added.
##        Make your Own function using ShapeMaker class and add respective Button to this.
##        This creates the base window on which Image and buttons are loaded.
##        Each Button name could have been renamed.
##        """
        
        self.outliner(src)
        frame1 = Frame(self.root)
        frame1.pack()
        B = Tkinter.Button(frame1, text ="Hair", command = lambda: self.change_current(0))
        Bu = Tkinter.Button(frame1, text ="Hair Bangs", command = lambda: self.change_current(1))
        But = Tkinter.Button(frame1, text ="Nose", command = lambda: self.change_current(2))
        Butt = Tkinter.Button(frame1, text ="Mouth", command = lambda: self.change_current(3))
        Butto = Tkinter.Button(frame1, text ="Right Eye", command = lambda: self.change_current(4))
        Button = Tkinter.Button(frame1, text ="Left Eye", command = lambda: self.change_current(5))
        Buttons = Tkinter.Button(frame1, text ="Eyebrows", command = lambda: self.change_current(6))
        Buttonss = Tkinter.Button(frame1, text ="Neck", command = lambda: self.change_current(7))
        B.grid(row=1,column=2)
        Bu.grid(row=1,column=3)
        But.grid(row=1,column=1)
        Butt.grid(row=1,column=4)
        Butto.grid(row=2,column=1)
        Button.grid(row=2,column=2)
        Buttons.grid(row=2,column=3)
        Buttonss.grid(row=2,column=4)
        image = Image.open('editable.jpg')
        resized = image.resize((500,500),Image.ANTIALIAS)
        render_image = ImageTk.PhotoImage(resized,master=self.canvas)
        self.canvas.create_image(0,0, image = render_image, anchor = NW,tags="IMG")
        self.canvas.grid(row=0,column=1)
        self.root.mainloop()
        print("Complete.")
        

    # Not required right Now was developing for future use
##    """def editable(self,src):
##        #self.default_layout()
##        create_editable('editable.jpg',self.canvas)"""
##        
        

    def nose(self):
        
##     """Nose method is used to create nose of the Face.
##        Nose would be made in downward direction after clicking the button.
##        Nose created would be joined from top circle to bottom circle as single line.
##        Also two more circle would be provided for respected joints."""
          
        self.current = None
        points = [0,0,-40,80,0,100,40,80]                                           # points represents sequence to create polygon. First point is 0 next is 1 then so on...
        extra = {(0,70,0):[0,2],(-30,80,1):[],(30,80,2):[]}                         # extra points on coordinate system would be added as red dots.First point is 0 and so on...
                                                                                    # set represent(x,y,point_no.):[list of polygon point no.s to be connected with]
        point_connect=[]                                                            # list show extra points that are connected.
                                                                                    # ___________Rest will be drawn _____________
        arc = []                                                                    # list show set of polygon points to be connected in arc.
        arc_extra = [(0,0,90,0,90,-1,0)]                                            # list show set (point_no._in_polygon,extra_point_no.) to made arc between.
                                                                                    # arc contains (pointa,pointb,angle_of_rotation,start_angle,end_angle,center_dependency,point_dependency_if_any)
        arc_ex_ex = []                                                              # set conneting arc way from extra point to extra point
        line = []                                                                   # set of polygons point to be connected in straight line.
        line_extra = [(2,0)]                                                        # set of polygon point and extra point no. to be connected.
        line_ex_ex = [(0,1,-8,0),(0,2,8,0)]                                         # extrapoint and extrapoint to be coonected
        obj = ShapeMaker('editable.jpg',self.canvas,points,extra,point_connect,arc
                         ,arc_extra,arc_ex_ex,line,line_extra,line_ex_ex,False)
        


    def mouth(self):

##     """Mouth method is used to create mouth of the Face.
##        Mouth would be made in Right side direction after clicking the button.
##        Mouth created would be joined from inside circle left to inside circle right as single line.
##        It resembles lips in Various ways. Lower Part would join to create proper figure."""

          
        self.current = None
        points = [0,0,40,-40,70,-40,100,0,70,40,40,40]
        extra = {(40,-20,0):[0],(40,20,1):[0],(70,-20,2):[3],(70,20,3):[3]}
        point_connect=[(0,2),(1,3)]
        arc = []
        arc_extra = []
        arc_ex_ex = []
        line = [(4,5)]
        line_extra = [(0,0,5,0),(0,1,5,0),(3,2,-5,0),(3,3,-5,0)]
        line_ex_ex = [(0,2),(3,1)]
        obj = ShapeMaker('editable.jpg',self.canvas,points,extra,point_connect,arc
                         ,arc_extra,arc_ex_ex,line,line_extra,line_ex_ex,False)
        #self.editable('ankitcs.jpg')


    def right_eye(self):

##        """
##        Right Eye is specific for right eye of the face.
##        Right Eye extends to right hence click on extreme left of right eye.
##        The above two dots could be adjusted to make appropriate eye figure.
##        After completion of Eye (ie. after triple clicking it) Next click would make eyeball.
##        Eyeball is movable and adjustable in both length and position.
##        After triple clicking again Eyeball would be created."""

        self.current = None
        points = [0,0,10,-10,25,-10,40,0,25,10,10,10]
        extra = {(33,-30,0):[],(0,-10,1):[]}
        point_connect=[]
        arc = []
        arc_extra = [(4,0,-90,90,180)]
        arc_ex_ex = [(0,1,90,120,180)]
        line = [(4,5)]
        line_extra = []
        line_ex_ex = []
        obj = ShapeMaker('editable.jpg',self.canvas,points,extra,point_connect,arc
                         ,arc_extra,arc_ex_ex,line,line_extra,line_ex_ex,True)
        #self.editable('ankitcs.jpg')


    def left_eye(self):

##        """
##        Left Eye is specific for left eye of the face.
##        Left Eye extends to left hence click on extreme right of left eye.
##        The above two dots could be adjusted to make appropriate eye figure.
##        After completion of Eye (ie. after triple clicking it) Next click would make eyeball.
##        Eyeball is movable and adjustable in both length and position.
##        After triple clicking again Eyeball would be created."""

        
        self.current = None
        points = [0,0,-10,-10,-25,-10,-40,0,-25,10,-10,10]
        extra = {(-33,-30,0):[],(0,-10,1):[]}
        point_connect=[]
        arc = []
        arc_extra = [(4,0,90,0,90)]
        arc_ex_ex = [(0,1,-90,0,60)]
        line = [(4,5)]
        line_extra = []
        line_ex_ex = []
        obj = ShapeMaker('editable.jpg',self.canvas,points,extra,point_connect,arc
                         ,arc_extra,arc_ex_ex,line,line_extra,line_ex_ex,True)
        #self.editable('ankitcs.jpg')


    def eyebrows(self):

##        """
##        Eyebrows doesn't come in set. It has unadjustable widths and three
##        dots above connects to make eyebrow complete.
##        Shifht eyebrow to left for left eyebrows."""
        
        self.current = None
        points = [0,0,10,-10,25,-10,80,0,25,10,10,10]
        extra = {(30,-20,0):[],(15,-15,1):[],(0,-10,2):[]}
        point_connect=[]
        arc = []
        arc_extra = []
        arc_ex_ex = []
        line = []
        line_extra = []
        line_ex_ex = [(0,1),(1,2)]
        obj = ShapeMaker('editable.jpg',self.canvas,points,extra,point_connect,arc
                         ,arc_extra,arc_ex_ex,line,line_extra,line_ex_ex,False)
        #self.editable('ankitcs.jpg')



    def neck(self):

##        """
##        Neck consists of various amounts of points It is also
##        used to create the chin part of the face Figure. Its consists of Various arcs ellipses and points.
##        """
        
        self.current = None
        points = [0,0,10,5,15,10,20,10,25,5,35,0,35,20,35,40,
                  20,45,10,45,0,40,0,20]
        extra = {(25,20,0):[]}
        point_connect=[]
        arc = [(5,7,90,0,180,2,6),(0,10,90,180,360,2,11)]
        arc_extra = []
        arc_ex_ex = []
        line = [(0,1),(1,2),(2,3),(3,4),(4,5)]
        line_extra = [(8,0,0,-10)]
        line_ex_ex = []
        obj = ShapeMaker('editable.jpg',self.canvas,points,extra,point_connect,arc
                         ,arc_extra,arc_ex_ex,line,line_extra,line_ex_ex,False)
        #self.editable('ankitcs.jpg')


##  _________________________________Your Functions goes Here__________________________________



## ___________________________Open up for Testing purposes__________________________________       
## obj = Get_Outline()
## obj.default_layout('ankitcs.jpg')

    
                    
                    
                    
                
                
        

