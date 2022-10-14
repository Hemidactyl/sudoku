from tempfile import tempdir
import sudoku_generator as sg
#import numpy as np

from tkinter import *
from tkinter import ttk

#class to handle sudoku field (button) generation, updating and pop-up window to insert numbers
class sudoku:

    def __init__(self, master):
        self.master = master
        #dictionary of all the main 81 buttons, or fields as called later on
        self.fields = {}
        #the Toplevel() object to be generated when a player presses one of the editable buttons
        #self.pop_up = None
        #temp coords holder for the pop_up
        self.temp_coords = None
        #grid to be checked when it gets completely full
        self.grid = None

    #create main sudoku fields
    def create_button(self, text, x, y, style):
        button = ttk.Button(self.master, text=text, width=2, command= lambda: self.number_popup(x, y, (root.winfo_pointerx(), root.winfo_pointery())), style=style)
        button.grid(row=x, column=y, ipadx=5, ipady=5)
        self.fields[(x,y)] = button

    #function to create pop-up window with number selection to update empty fields
    def number_popup(self, x, y, pos):
        self.temp_coords = (x, y)

        self.pop_up = Toplevel(self.master)
        self.pop_up.overrideredirect(True)
        self.pop_up.grab_set()
        self.pop_up.geometry(f'+{pos[0]}+{pos[1]}')

        for i in range(9):
            k=i//3
            l=i%3
            self.create_pop_up_button(i+1, k, l, x, y)

        #adding a 'clear' button to remove a number
        clear_button=ttk.Button(self.pop_up, text="Clear", width=6, command= lambda: self.update_and_destroy('0', x, y))
        clear_button.grid(row=3, column=0, columnspan=3, sticky=(N, W, E, S))


        self.pop_up.focus_force()
        self.pop_up.bind('<Key>', self.key_down)
        self.pop_up.bind('<Delete>', self.del_down)

    #creating one of the 9 buttons in the pop_up window
    #k, l are the coordinates of the button to be created
    #x, y are the coordinates of the sudoku field to be updated with update_and_destroy
    def create_pop_up_button(self, text, k, l, x, y):
        btn = ttk.Button(self.pop_up, text=text, width=2, command = lambda: self.update_and_destroy(text, x, y))
        btn.grid(row=k, column=l)
    
    #key press event for when the pop-up is open
    def key_down(self, event):
        allowed = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9']
        if event.char in allowed:
            self.update_and_destroy(event.char, self.temp_coords[0], self.temp_coords[1])


    #player pressed delete
    def del_down(self, event):
        self.update_and_destroy('0', self.temp_coords[0], self.temp_coords[1])


    #update a field and the grid, destroy the pop_up window
    #then check for empties in the grid -> if it's full, call game checker
    def update_and_destroy(self, text, x, y):
        self.grid[(x,y)] = int(text)
        if text == '0':
            text = ''

        self.fields[(x,y)].configure(text=text)
        self.pop_up.destroy()
        print(self.grid)

        if self.count_zeros() == 0:
            self.check_sudoku()



    #initialize empty 9x9 grid for sudoku and difficulty choice buttons
    def initialize(self):
        #create all buttons
        for i in range(81):
            x=i//9
            y=i%9
            #the index floor division by 3 helps determine which square we're in
            if (x//3+y//3) % 2 == 0:
                self.create_button('', x, y, 'Dark.TButton')
                self.fields[(x,y)].configure(state=DISABLED)
            else:
                self.create_button('', x, y, 'Light.TButton')
                self.fields[(x,y)].configure(state=DISABLED)
        
        #create control buttons (start game etc.)
        self.easy_button = ttk.Button(self.master, text='Easy', command= lambda: self.start_game('Easy'))
        self.easy_button.grid(row=9, column=0, columnspan=3, sticky = (N, W, E, S))
        self.intermediate_button = ttk.Button(self.master, text='Intermediate', command= lambda: self.start_game('Intermediate'))
        self.intermediate_button.grid(row=9, column=3, columnspan=3, sticky = (N, W, E, S))
        self.hard_button = ttk.Button(self.master, text='Hard', command= lambda: self.start_game('Hard'))
        self.hard_button.grid(row=9, column=6, columnspan=3, sticky = (N, W, E, S))


    #create sudoku, put into the grid and replace difficulty buttons with a NEW GAME button
    def start_game(self, difficulty):
        #generate a valid sudoku puzzle
        self.grid = sg.make_me_a_sudoku(difficulty)
        #configure all buttons (disable buttons that have a number set, remove all the 0s)
        for i in range(81):
            x=i//9
            y=i%9

            if self.grid[x, y] == 0:
                self.fields[(x,y)].configure(text="", state=NORMAL)
            else:
                self.fields[(x,y)].configure(text=self.grid[x,y], state=DISABLED)
        
        #hide all the difficulty buttons
        self.easy_button.grid_remove()
        self.intermediate_button.grid_remove()
        self.hard_button.grid_remove()

        #create NEW GAME button
        self.new_game_button = ttk.Button(self.master, text='NEW GAME', command = self.confirm_new_game)
        self.new_game_button.grid(row=9, column=0, columnspan=9, sticky=(N, W, E, S))

    
    #new game confirmation pop up
    def confirm_new_game(self):
        self.pop_up = Toplevel(self.master)
        self.pop_up.overrideredirect(True)
        self.pop_up.grab_set()

        #getting the main window's geometry details to place pop-up along the middle
        #getting the toplevels size is overly clunky, but it is around 210
        x=root.winfo_x() + (root.winfo_width()-210)//2
        y=root.winfo_y() + root.winfo_height()//2

        self.pop_up.geometry(f'+{x}+{y}')


        frame = ttk.Frame(self.pop_up, padding="5 5 5 5")
        frame.grid(row=0, column=0, sticky=(N, W, E, S))
        
        #just a question
        warning = ttk.Label(frame, text='Are you certain?')
        warning.grid(row=0, column=0, columnspan=2)
        
        #and some buttons
        self.yes_button = ttk.Button(frame, text='YUP', command=self.new_game)
        self.yes_button.grid(row=1, column=0)

        self.no_button = ttk.Button(frame, text='NAH', command=self.pop_up.destroy)
        self.no_button.grid(row=1, column=1)


    #remove new game button and renew the difficulty buttons and clear all the sudoku fields.
    def new_game(self):
        self.pop_up.destroy()
        self.new_game_button.grid_remove()

        for i in range(81):
            x=i//9
            y=i%9
            self.fields[(x,y)].configure(text="", state=DISABLED)

        self.easy_button.grid(row=9, column=0, columnspan=3, sticky = (N, W, E, S))
        self.intermediate_button.grid(row=9, column=3, columnspan=3, sticky = (N, W, E, S))
        self.hard_button.grid(row=9, column=6, columnspan=3, sticky = (N, W, E, S))


    #count and return the number of zeros in the grid
    def count_zeros(self):
        zeros = 0
        for i in range(81):
            x=i//9
            y=i%9
            if self.grid[x,y] == 0:
                zeros += 1
        
        return(zeros)

    def check_sudoku(self):
        for i in range(81):
            x=i//9
            y=i%9

            #temporarily put a 0 in the grid for the check_index to work
            n = self.grid[x,y]
            self.grid[x,y] = 0

            if sg.check_index(self.grid, n, (x,y)) == False:
                self.grid[x,y] = n
                self.end_game_popup(False)
                return

            self.grid[x,y] = n

        self.end_game_popup(True)

    
    def end_game_popup(self, correct):
        self.pop_up = Toplevel(self.master)
        self.pop_up.overrideredirect(True)
        self.pop_up.grab_set()
        self.pop_up.geometry(f'+{root.winfo_x() + (root.winfo_width()-240)//2}+{300}')

        message = ttk.Label(self.pop_up)
        message.grid(row=0, column=0, columnspan=2)


        if correct == True:
            message.configure(text='Congratulations! You did it!')
        else:
            message.configure(text="Oh no, something ain't right...")

        other_button = ttk.Button(self.pop_up, text='Quit', command=root.destroy)
        other_button.grid(row=1, column=1)

        ng_button = ttk.Button(self.pop_up, text='New game?', command=self.new_game)
        ng_button.grid(row=1, column=0)

        
        


    
root = Tk()
root.title("Sudoku!")
root.resizable(False, False)

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


#initialize the game
game = sudoku(mainframe)

game.initialize()

root.mainloop()