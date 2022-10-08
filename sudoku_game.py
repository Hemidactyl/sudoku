import sudoku_generator as sg
#import numpy as np

from tkinter import *
from tkinter import ttk
import random

#class to handle sudoku field (button) generation, updating and pop-up window to insert numbers
class sudoku:

    def __init__(self, master):
        self.master = master
        #dictionary of all the main 81 buttons, or fields as called later on
        self.fields = {}
        #the Toplevel() object to be generated when a player presses one of the editable buttons
        self.pop_up = None

    #function to create pop-up window with number selection to update empty fields
    def number_popup(self, x, y, pos):
        self.pop_up = Toplevel(self.master)
        self.pop_up.overrideredirect(True)
        self.pop_up.grab_set()
        self.pop_up.geometry(f'+{pos[0]}+{pos[1]}')

        for i in range(9):
            k=i//3
            l=i%3
            self.create_pop_up_button(i+1, k, l, x, y)

        self.pop_up.focus_force()
        self.pop_up.bind('<Key>', self.key_down)
        

    #create main sudoku fields
    def create_button(self, text, x, y, style):
        button = ttk.Button(self.master, text=text, width=2, command= lambda: self.number_popup(x, y, (root.winfo_pointerx(), root.winfo_pointery())), style=style)
        button.grid(row=x, column=y, ipadx=5, ipady=5)
        self.fields[(x,y)] = button

    #update a field and destroy the pop_up window
    def update_and_destroy(self, text, x, y):
        self.fields[(x,y)].configure(text=text)
        self.pop_up.destroy()

    #creating one of the 9 buttons in the pop_up window
    def create_pop_up_button(self, text, k, l, x, y):
        btn = ttk.Button(self.pop_up, text=text, width=2, command = lambda: self.update_and_destroy(text, x, y))
        btn.grid(row=k, column=l)
    
    #key press event for when the pop-up is open
    def key_down(self, event):
        event.char
        allowed = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        if event.char in allowed:
            self.key_pressed=event.char

        

    


    
root = Tk()
root.title("Sudoku!")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(row=0, column=0, sticky = (N, W, E, S))


#some styles
stl = ttk.Style()

#lighter colours for first square and then alternating
stl.configure('Light.TButton', background='#f6eae8', foreground='#606060')
stl.map('Light.TButton',
foreground=[('disabled', 'black')],
background=[('disabled','#f6eae8'),
            ('active', '#e3d7d5')]
)

#darker colours for second square etc.
stl.configure('Dark.TButton', background='#f5c4bc', foreground='#606060')
stl.map('Dark.TButton',
foreground=[('disabled', 'black')],
background=[('disabled','#f5c4bc'),('active', '#dbaea7')]
)



#generate a valid sudoku puzzle
grid = sg.make_me_a_sudoku()

#initiate the game
game = sudoku(mainframe)


#create all buttons
for i in range(81):
    x=i//9
    y=i%9
    #the index floor division by 3 helps determine which square we're in
    if (x//3+y//3) % 2 == 0:
        game.create_button(grid[x,y], x, y, 'Dark.TButton')
    else:
        game.create_button(grid[x,y], x, y, 'Light.TButton')

#configure all buttons (disable buttons that have a number set, remove all the 0s)
for i in range(81):
    x=i//9
    y=i%9

    if grid[x, y] == 0:
        game.fields[(x,y)].configure(text="")
    else:
        game.fields[(x,y)].configure(state=DISABLED)

#create control buttons (start game etc.)
easy_button = ttk.Button(mainframe, text="Easy").grid(row=9, column=0, columnspan=3, sticky = (N, W, E, S))
intermediate_button = ttk.Button(mainframe, text="Intermediate").grid(row=9, column=3, columnspan=3, sticky = (N, W, E, S))
hard_button = ttk.Button(mainframe, text="Hard").grid(row=9, column=6, columnspan=3, sticky = (N, W, E, S))


root.mainloop()