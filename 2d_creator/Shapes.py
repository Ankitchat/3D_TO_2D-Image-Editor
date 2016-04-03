##    ______________*****__________ShapeMaker________******__________________
##    Shapes file contains class Shapmaker that is used to induce various shapes according to provided
##    coordinates. It has varied amount of Parameters to intake that fulfills their respective responsiblity
##    regarding connecting dots and making shape polygons.Shapemaker is an embodiment of making a class based
##    Tkinter GUI Interface. It is solely based upon creation of various body parts and embedd them together.
##    Shapemaker also includes Custom code of Eyeball and could also be used to introduce various other custom code
##    if required.

import Tkinter as tk
from Tkinter import *
import cv2
import numpy as np
from PIL import Image, ImageTk
import math

class ShapeMaker(tk.Tk):

##    Class Shapemaker initilizes various kinds of sequence to respective datatype for creation and drawing of
##    various Figures and Objects. Shapemaker's one of most Important attribute would be circle_map which is used
##    to store and point various red dots (points) in the figure.
    
    def __init__(self,src,window,points,extra,points_connect,arc,arc_extra,arc_ex_ex
                 ,line,line_extra,line_ex_ex,eye):
        
        self.x = self.y =self.created = self.eyeball_created = 0
        self.circle_info={}
        self.line_info={}
        self.circle_map={}
        self.circle_dict={}
        self.window = window
        self.center_x=0
        self.center_y=0
        self.window.pack(side="top", fill="both", expand=True)
        self.window.bind("<ButtonPress-1>", self.on_button_press)
        self.window.bind("<B1-Motion>", self.on_move_press)
        self.window.bind("<ButtonRelease-1>", self.on_button_release)
        self.window.bind("<Triple-Button-1>", self.double_press)

        self.src=src
        self.size=(500,500)
        self.image = cv2.imread(self.src)
        self.original = Image.open(src)
        resized = self.original.resize(self.size,Image.ANTIALIAS)
        self.image = cv2.resize(self.image,self.size, interpolation = cv2.INTER_CUBIC)
        self.render_image = ImageTk.PhotoImage(resized,master= self.window)
        self.window.delete("IMG")
        self.window.create_image(0, 0, image=self.render_image, anchor=NW, tags="IMG")
        self.points = points
        self.extra_point = extra
        self.points_connect = points_connect
        self.arc = arc
        self.arc_e = arc_extra
        self.arc_ex_ex = arc_ex_ex
        self.line = line
        self.line_e = line_extra
        self.line_ex_ex = line_ex_ex
        self.eye = eye
        

        self.rect = None
        self.current_circle=0

        self.start_x = None
        self.start_y = None
        self.window.bind("<Configure>", self.resize)

    def resize(self, event):
        
##        """ Resizes the respective image with change in window size."""
        
        size = (event.width, event.height)
        self.size=size
        self.original = Image.open(self.src)
        resized = self.original.resize(size,Image.ANTIALIAS)
        self.image = cv2.resize(self.image,size, interpolation = cv2.INTER_CUBIC)
        self.render_image = ImageTk.PhotoImage(resized,master = self.window)
        self.window.delete("IMG")
        self.window.create_image(0, 0, image=self.render_image, anchor=NW, tags="IMG")        
        

    def on_button_press(self, event):
        
##        """ Binding of Button Press Event:
##            1. If no figure is created It creates a figure with adjusted points.
##            2. If clicked area lis inside red dot of any point It changes current selected.
##            3. If clicked area do not contain any red dots it moves currently selected to that
##               area."""

        self.start_x = event.x
        self.start_y = event.y

        if self.created == 0:
            self.adjust_points(self.start_x,self.start_y)
            self.poly = self.window.create_polygon(self.points, fill="green", outline='red')
            self.polyshape(self.points)
            self.created=1

        if self.created == 1:
            curX, curY = (event.x, event.y)
            for each in self.circle_dict.keys():
                if self.in_circle(curX,curY,each):
                    print(each)
                    print(self.circle_dict)
                    self.current_circle=each
                    try:
                        self.points[2*each] = curX
                        self.points[2*each+1] = curY
                        self.circle_map[self.current_circle] = (curX,curY)
                        # expand rectangle as you drag the mouse
                        self.window.coords(self.poly,*self.points)
                        
                    except:
                        current = self.circle_map[self.current_circle]
                        if not (curX,curY)==current:
                            self.extra_point[(curX,curY)] = self.extra_point[current]
                            del self.extra_point[current]
                        self.circle_map[self.current_circle] = (curX,curY)
                        print(self.circle_map)                       
            

    def on_move_press(self, event):

##        """ Binding of Motion:
##            Does same as mouse press"""
        
        curX, curY = (event.x, event.y)
        for each in self.circle_dict.keys():
            if self.in_circle(curX,curY,each):
                self.current_circle=each
                try:
                    self.points[2*each] = curX
                    self.points[2*each+1] = curY
                    self.circle_map[self.current_circle] = (curX,curY)
                    # expand rectangle as you drag the mouse
                    self.window.coords(self.poly,*self.points)
                except:
                    current = self.circle_map[self.current_circle]
                    if not (curX,curY)==current:
                        self.extra_point[(curX,curY)] = self.extra_point[current]
                        del self.extra_point[current]
                    self.circle_map[self.current_circle] = (curX,curY)
                    print(self.circle_map)
                    
                
    def on_button_release(self, event):

##        """ Binding Of release Button:
##            1. Using various Functions it deletes whole figure and recreates
##               it and new respective point"""
        
        self.window.delete(self.poly)
        self.delete_circle()
        self.delete_line()
        curX, curY = (event.x, event.y)
        try:
            self.points[2*self.current_circle] = curX
            self.points[2*self.current_circle+1] = curY
            self.circle_map[self.current_circle] = (curX,curY)
            self.poly = self.window.create_polygon(self.points, fill="green", outline='red')
            self.polyshape(self.points)
        except:
            current = self.circle_map[self.current_circle]
            if not (curX,curY)==current:
                self.extra_point[(curX,curY)] = self.extra_point[current]
                del self.extra_point[current]
            self.circle_map[self.current_circle] = (curX,curY)
            self.poly = self.window.create_polygon(self.points, fill="green", outline='red')
            self.polyshape(self.points)
            print(self.circle_map)
            

    def double_press(self, event):

##        """Binding of Triple Click Event:
##        1. It is used to draw various lines over to image and save the image as editable.jpg output
##           in the same directory.
##        """
        self.window.delete("all")
        #self.delete_circle()
        #self.delete_line()
        pairs = []
        i=0
        while(i<len(self.points)):
            pairs.append([self.points[i],self.points[i+1]])
            i=i+2
        pairs = np.array([pairs],'int32')       
        self.image = cv2.fillPoly(self.image,np.int32(pairs),[255,255,255])
        for each in self.arc:
            if len(each)==5:
                self.draw_arc(each[0],each[1],each[2],each[3],each[4],0,0)
            else:
                self.draw_arc(each[0],each[1],each[2],each[3],each[4],each[5],each[6])
        for each in self.arc_e:
            if len(each)==5:
                self.draw_arc_extra(each[0],each[1],each[2],each[3],each[4],0,0)
            else:
                self.draw_arc_extra(each[0],each[1],each[2],each[3],each[4],each[5],each[6])
        for each in self.arc_ex_ex:
            if len(each)==5:
                self.draw_arc_ex_ex(each[0],each[1],each[2],each[3],each[4],0,0)
            else:
                self.draw_arc_ex_ex(each[0],each[1],each[2],each[3],each[4],each[5],each[6])
        for each in self.line:
            if len(each)==2:
                self.draw_line(each[0],each[1],0,0)
            else:
                self.draw_line(each[0],each[1],each[2],each[3])
        for each in self.line_e:
            if len(each)==2:
                self.draw_line_extra(each[0],each[1],0,0)
            else:
                self.draw_line_extra(each[0],each[1],each[2],each[3])
        for each in self.line_ex_ex:
            if len(each)==2:
                self.draw_line_ex_ex(each[0],each[1],0,0)
            else:
                self.draw_line_ex_ex(each[0],each[1],each[2],each[3])
        cv2.imwrite('editable.jpg',self.image)
        self.window.unbind("<ButtonPress-1>")
        self.window.unbind("<B1-Motion>")
        self.window.unbind("<ButtonRelease-1>")
        self.window.unbind("<Triple-Button-1>")
        image = ImageTk.PhotoImage(file = 'editable.jpg',width=500,height=500,master=self.window)
        self.window.create_image(0,0, image = image, anchor = NW)
        if self.eye==True:
            print("eyeball")
            self.eyeball()     
         
    
    def create_circle(self,on_x,on_y):
        
##        """ Create Red dot circle to provided point"""
        
        key_to_add=100
        for key in self.circle_map.keys():
            if self.circle_map[key]==(on_x,on_y):
                key_to_add = key
        self.circle_dict[key_to_add]=[on_x-3, on_y-3, on_x+3, on_y+3]
        self.circle_info[key_to_add]=self.window.create_oval(on_x-3, on_y-3, on_x+3, on_y+3, outline="red", 
             fill='red', width=2)

    def polyshape(self,point_list):

##        """ Creates polygon / figure structure whole required by client.
##            It is used by Button Release Event."""

        i=0
        self.delete_circle()
        self.delete_line()
        self.circle_dict={}
        self.circle_info={}
        while(i<len(point_list)):
            self.create_circle(point_list[i],point_list[i+1])
            i=i+2
        to_add = len(self.circle_dict)
        for key in self.extra_point.keys():
            self.create_circle(key[0],key[1])
            for each_point in self.extra_point[key]:
                self.create_line_from_point(key[0],key[1],each_point)
        for each in self.points_connect:
            print(each)
            self.create_line_ex_ex(each[0],each[1])
            
    def in_circle(self,event_x,event_y,circle_no):

##        """ Check if click is inside any of red dots at present point"""
        
        if event_x in range(self.circle_dict[circle_no][0],self.circle_dict[circle_no][2]):
            if event_y in range(self.circle_dict[circle_no][1],self.circle_dict[circle_no][3]):
                return True

            else:
                return False
        else:
            return False

    def delete_circle(self):

##        """Deletes all red dots"""
        
        for each in self.circle_info:
            self.window.delete(self.circle_info[each])

    def delete_line(self):

##        """Deletes all lines"""
        
        for each in self.line_info:
            self.window.delete(self.line_info[each])

## ______________________________Self Explanatory using Anime style guide___________________________________________________

    def create_line(self,point_a,point_b):
        self.line_info[len(self.line_info)]=self.window.create_line(self.points[point_a],self.points[point_a+1]
                                                                    ,self.points[point_b],self.points[point_b+1],fill="red")

    def create_line_from_point(self,x,y,point_b):
        self.line_info[len(self.line_info)]=self.window.create_line(x,y,self.points[2*point_b],self.points[2*point_b+1],fill="red")

    def create_line_ex_ex(self,point_a,point_b):
        print(self.circle_map)
        on_element = len(self.points)/2
        print(on_element)
        print(self.circle_map[on_element+point_a])
        print(self.circle_map[on_element+point_b])
        self.line_info[len(self.line_info)]=self.window.create_line(self.circle_map[on_element+point_a][0],
                                                                    self.circle_map[on_element+point_a][1],
                                                                    self.circle_map[on_element+point_b][0],
                                                                    self.circle_map[on_element+point_b][1],fill="red")

##______________________________________________________________________________________________________________________________
        
    def adjust_points(self,x,y):

##        """ Used to buid figure at starting point in first button press event"""
        
        i=0
        while(i<len(self.points)):
            self.points[i]=self.points[i]+x
            self.points[i+1]=self.points[i+1]+y
            self.circle_map[len(self.circle_map)] = (self.points[i],self.points[i+1])
            i=i+2
        loop_dict = self.extra_point
        to_add = len(self.circle_map)
        for key in loop_dict.keys():
            self.extra_point[(key[0]+x,key[1]+y)] = self.extra_point[key]
            self.circle_map[to_add + key[2]] = (key[0]+x,key[1]+y)
            del self.extra_point[key]

##_________________________________________________________Drawing Functions_______________________________________________________

    def draw_arc(self,point_a,point_b,angle,fstart,tend,depend_x,depend_y):
        print("_______arc_______")
        x1 = self.points[2*point_a]
        x2 = self.points[2*point_b]
        y1 = self.points[2*point_a+1]
        y2 = self.points[2*point_b+1]
        major_arc = self.points[point_b+1]-self.points[point_a+1]
        minor_arc = self.points[point_b]-self.points[point_a]
        if depend_x == -1:
            cv2.ellipse(self.image,(x2,y1),(major_arc,minor_arc),angle,fstart,tend,0)
        elif depend_x == 2:
            print(self.circle_map)
            print(x1,x2,y1,y2)
            centerx = (x2+x1)/2
            centery = (y2+y1)/2
            distance1 = math.sqrt(math.pow((x2-x1),2)+math.pow((y2-y1),2))
            distance2 = math.sqrt(math.pow((centerx - self.circle_map[depend_y][0]),2)
                                  + math.pow((centery - self.circle_map[depend_y][1]),2))
            major_arc = int(max(distance1,distance2)/2)
            minor_arc = int(min(distance1,distance2))
            print(centerx,centery)
            print(distance1,distance2)
            cv2.ellipse(self.image,(centerx,centery),(major_arc,minor_arc),angle,fstart,tend,0)
            print("done")
        else:
            cv2.ellipse(self.image,(x1,y2),(major_arc,minor_arc),angle,fstart,tend,0)


    def draw_arc_extra(self,point_a,point_e,angle,fstart,tend,depend_x,depend_y):
        print("_______arc________")
        on_element = len(self.points)/2
        x1 = self.points[2*point_a]
        y1 = self.points[2*point_a+1]
        x2 = self.circle_map[on_element+point_e][0]
        y2 = self.circle_map[on_element+point_e][1]
        print(self.circle_map)
        print(x1,y1,x2,y2)
        major_arc = abs(y2-y1)
        minor_arc = abs(x2-x1)
        print(major_arc,minor_arc)
        if depend_x == -1:
            cv2.ellipse(self.image,(x2,y1),(major_arc,minor_arc),angle,fstart,tend,0)
        elif depend_x == 2:
            centerx = abs(x2-x1)/2
            centery = abs(y2-y1)/2
            distance1 = math.sqrt(math.pow((x2-x1),2)+math.pow((y2-y1),2))
            distance2 = math.sqrt(math.pow((centerx - self.circle_map[depend_y][0]),2)
                                  + math.pow((centery - self.circle_map[depend_y][1]),2))
            major_arc = max(distance1,distance2)
            minor_arc = min(distance1,distance2)
            cv2.ellipse(self.image,(centerx,centery),(major_arc,minor_arc),angle,fstart,tend,0)
        else:
            cv2.ellipse(self.image,(x1,y2),(major_arc,minor_arc),angle,fstart,tend,0)
        

    def draw_arc_ex_ex(self,point_ae,point_e,angle,fstart,tend,depend_x,depend_y):
        print("_______arc________")
        on_element = len(self.points)/2
        x1 = self.circle_map[on_element+point_ae][0]
        y1 = self.circle_map[on_element+point_ae][1]
        x2 = self.circle_map[on_element+point_e][0]
        y2 = self.circle_map[on_element+point_e][1]
        print(x1,y1,x2,y2)
        major_arc = abs(y2-y1)
        minor_arc = abs(x2-x1)
        print(major_arc,minor_arc)
        if depend_x == -1:
            cv2.ellipse(self.image,(x2,y1),(major_arc,minor_arc),angle,fstart,tend,0)
        elif depend_x == 2:
            centerx = abs(x2-x1)/2
            centery = abs(y2-y1)/2
            distance1 = math.sqrt(math.pow((x2-x1),2)+math.pow((y2-y1),2))
            distance2 = math.sqrt(math.pow((centerx - self.circle_map[depend_y][0]),2)
                                  + math.pow((centery - self.circle_map[depend_y][1]),2))
            major_arc = max(distance1,distance2)
            minor_arc = min(distance1,distance2)
            cv2.ellipse(self.image,(centerx,centery),(major_arc,minor_arc),angle,fstart,tend,0)
        else:
            cv2.ellipse(self.image,(x1,y2),(major_arc,minor_arc),angle,fstart,tend,0)


    def draw_line(self,point_a,point_b,depend_x,depend_y):
        print("__________line_______")
        print(self.points[2*point_a]+depend_x,self.points[2*point_a+1]+depend_y)
        print(self.points[2*point_b],self.points[2*point_b+1])
        cv2.line(self.image,(self.points[2*point_a]+depend_x,self.points[2*point_a+1]+depend_y)
                 ,(self.points[2*point_b],self.points[2*point_b+1]),0)


    def draw_line_extra(self,point_a,point_e,depend_x,depend_y):
        on_element = len(self.points)/2
        x = self.circle_map[on_element+point_e][0]
        y = self.circle_map[on_element+point_e][1]
        cv2.line(self.image,(x,y),(self.points[2*point_a]+depend_x,
                                   self.points[2*point_a+1]+depend_y),0)
        

    def draw_line_ex_ex(self,point_ae,point_e,depend_x,depend_y):
        print("______line_______")
        print(point_e,point_ae)
        on_element = len(self.points)/2
        x1 = self.circle_map[on_element+point_e][0]
        y1 = self.circle_map[on_element+point_e][1]
        x2 = self.circle_map[on_element+point_ae][0]+depend_x
        y2 = self.circle_map[on_element+point_ae][1]+depend_y
        print(depend_x,depend_y)
        if depend_x <0 or depend_y <0:
            print("one down")
            if x2 > x1:
                cv2.line(self.image,(x1,y1),(x2,y2),0)
                return
        if depend_x >0 or depend_y >0:
            print("one up")
            print(x1,x2)
            if x2 < x1:                
                cv2.line(self.image,(x1,y1),(x2,y2),0)
                return
        print(self.circle_map)
        print(x1,y1,x2,y2)
        if depend_x==0 and depend_y == 0:
            cv2.line(self.image,(x1,y1),(x2,y2),0)
            return

##_________________________________________________________________________________________________________________

##________________________________________Custom Eyeball Functions__________________________________________________
##          Called only for tight and left eyes
        
    def eyeball(self):
        self.window.create_image(0, 0, image=self.render_image, anchor=NW, tags="IMG")  
        self.window.bind("<ButtonPress-1>", self.circle_press)
        self.window.bind("<B1-Motion>", self.circle_move_press)
        self.window.bind("<Triple-Button-1>", self.circle_release)


    def circle_press(self, event):
        if self.eyeball_created==0:
            self.center_x = event.x
            self.center_y = event.y
            self.eyeball = self.window.create_oval(event.x-10, event.y-10, event.x+10, event.y+10, outline="red", 
                 fill='green')
            self.eyeball_created=1
            
        if self.eyeball_created==1:
            self.window.delete(self.eyeball)
            self.center_x = event.x
            self.center_y = event.y
            self.eyeball = self.window.create_oval(event.x-10, event.y-10, event.x+10, event.y+10, outline="red", 
                 fill='green')
            self.eyeball_created=1
            

    def circle_move_press(self, event):
        print(self.center_x,self.center_y)
        radius = event.x - self.center_x
        self.radius = radius
        print(radius)
        self.window.delete(self.eyeball)
        self.eyeball = self.window.create_oval(self.center_x-radius,self.center_y-radius
                           ,self.center_x+radius,self.center_y+radius,outline="red",fill='green')
        
    def isLeft(self,ax,ay,bx,by,cx,cy):
        if ((bx - ax)*(cy - ay) - (by - ay)*(cx - ax)) > 0:
            return True
        if ((bx - ax)*(cy - ay) - (by - ay)*(cx - ax)) == 0:
            print("Vanishing")
            self.image[cy,cx,0]=0
            self.image[cy,cx,1]=0
            self.image[cy,cx,2]=0
            return False
        return False

    def in_eyeball(self,x,y):
        if (math.pow((x-self.center_x),2) +math.pow((y - self.center_y),2)) <= math.pow(self.radius,2):
            return True
        return False          
        
    def in_eyelid(self,ptx,pty):

##        """ Check if Eyeball is in Eyelid or not
##            Removes all the parts that are outside."""
        
        on_element = len(self.points)/2
        x2 = self.points[8]
        y2 = self.points[9]
        x1 = self.points[10]
        y1 = self.points[11]
        if not self.isLeft(x1,y1,x2,y2,ptx,pty):
            print("At up")
            x1 = self.points[8]
            y1 = self.points[9]
            x2 = self.circle_map[on_element+0][0]
            y2 = self.circle_map[on_element+0][1]
            if not self.isLeft(x1,y1,x2,y2,ptx,pty):
                print("At right")
                x2 = self.points[10]
                y2 = self.points[11]
                x1 = self.circle_map[on_element+1][0]
                y1 = self.circle_map[on_element+1][1]
                if self.isLeft(x2,y2,x1,y1,ptx,pty):
                    print("At Left")
                    x1 = self.circle_map[on_element+0][0]
                    y1 = self.circle_map[on_element+0][1]
                    x2 = self.circle_map[on_element+1][0]
                    y2 = self.circle_map[on_element+1][1]
                    if not self.isLeft(x1,y1,x2,y2,ptx,pty):
                        print("At down")
                        return True
        return False
                    
            
        
    def circle_release(self, event):
        print("Iy working")
        on_element = len(self.points)/2
        cv2.circle(self.image,(self.center_x,self.center_y),self.radius,0)
        cv2.circle(self.image,(self.center_x,self.center_y),self.radius/5,[0,0,0])
        cv2.circle(self.image,(self.center_x+(self.radius/4),self.center_y-2),5,0)
        cv2.imwrite('editable.jpg',self.image)
        self.image = cv2.imread(self.src)
        self.image = cv2.resize(self.image,self.size, interpolation = cv2.INTER_CUBIC)
        for x in range(self.center_x-self.radius,self.center_x+self.radius):
            print("here at "+str(x))
            print(self.circle_map[on_element+0][0]-20,self.points[9]+20)
            for y in range(self.center_y-self.radius,self.center_y+self.radius):
                print("here at y"+str(y))
                if self.in_eyeball(x,y):
                    print("inside eyeball")
                    if not self.in_eyelid(x,y):
                        print("inside")
                        print(self.image[y,x,0])
                        self.image[y,x,0]=255
                        self.image[y,x,1]=255
                        self.image[y,x,2]=255
        cv2.imwrite('editable.jpg',self.image)

##__________________________________________________________________________________________________________

##______________________________________Your Code Goes Here__________________________________________________
                        
                
            

        
        
        
        
        
                

