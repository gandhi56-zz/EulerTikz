from tkinter import * #global tkinter import
from tkinter.dnd import Tester as Dragwindow, Icon as Dragable #import screen and object dragable classes
root=Tk() #make our root window
root.withdraw() #hide it since we don't need it
main=Dragwindow(root) #make our actual main window, it can have dragable objects on
def make_btn(): #make a new 'B' button
    Dragable('B').attach(main.canvas) #make it and attach it to our window's functioning part, the canvas
Button(main.top, text='A', command=make_btn).pack() #make a button 'A' for our window
mainloop() #start the mainloop