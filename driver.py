# try another driver

import tkinter as tk
import os.path
from gamestate import Gamestate
import copy
import numpy as np
import time 
import random
from card import Card

class UI:
    def __init__(self, parent):
        
        parent.title('Spider Solitaire AI (sans undo)')
        parent.geometry('1000x500')
        frame = tk.Frame(parent)
        frame.pack()

        self.canvas = tk.Canvas(parent, width=1000, height=500, bg = '#afeeee')
        self.name_label = tk.Label(parent, text = 'Filename', font=('calibre',10, 'bold'))
        self.canvas.create_window(100, 30, window=self.name_label)
        self.entry1 = tk.Entry(parent) 
        self.canvas.create_window(200, 30, window=self.entry1)

        self.canvas.pack()
        self.button1 = tk.Button(frame,
                   text="Init_file",
                   command=self.set_gamestate)
        self.button1.pack(side=tk.LEFT)
        self.button2 = tk.Button(frame,
                   text="Init_random",
                   command=self.set_gamestate_random)
        self.button2.pack(side=tk.LEFT)
        self.button3 = tk.Button(frame,
                   text="single moveblock",
                   command=self.execute_moveblock)
        self.button3.pack(side=tk.LEFT)
        self.button3['state'] = tk.DISABLED 
        self.button4 = tk.Button(frame,
                   text="all moveblocks",
                   command=self.execute_every_moveblock)
        self.button4.pack(side=tk.LEFT)
        self.button4['state'] = tk.DISABLED 
        

        self.button5 = tk.Button(frame, 
                   text="QUIT", 
                   fg="red",
                   command=quit)
        self.button5.pack(side=tk.LEFT)

    def set_gamestate(self):
        
        self.gs = Gamestate()
        mystr = self.entry1.get()    
        try:
            self.gs.init_filename(mystr)
            self.canvas.delete("some_tag")
            data = self.gs.printstate_canvas()
            for datum in data:
                self.canvas.create_text(datum[0],datum[1],text=datum[2],fill=datum[3],font="Courier 10",tag="some_tag")
            self.button3['state']=tk.NORMAL; self.button4['state']=tk.NORMAL
            self.canvas.create_text(400,300,text=self.gs.sanity_check(),fill='black',font="Courier 10",tag="some_tag")
        except:
            self.canvas.delete("some_tag")
            self.canvas.create_text(200,200,fill = 'red', font = "Times 12", text='ERROR: File is corrupted or does not exist',tag = "some_tag")
            self.button3['state']=tk.DISABLED; self.button4['state']=tk.DISABLED


    def set_gamestate_random(self):
        self.gs = Gamestate()
        self.gs.init_random()
        self.canvas.delete("some_tag")
        data = self.gs.printstate_canvas()
        for datum in data:
            self.canvas.create_text(datum[0],datum[1],text=datum[2],fill=datum[3],font="Courier 10",tag="some_tag")
        self.button3['state']=tk.NORMAL; self.button4['state']=tk.NORMAL
 
    def execute_moveblock(self):
        game_result = 'STILLGOING'
    
        prev_eval = self.gs.evaluateposition()
        numtries = 100
        threshold_param = 2
        bestsofar_moveblock = []
        bestsofar_eval = self.gs.evaluateposition()
                    
        # find the best sequence of moves
        for mytry in range(numtries):
            moveblock = np.random.randint(1000,size=30)
            gs2 = copy.deepcopy(self.gs)
            gs2.executemoveblock(moveblock,threshold_param,False)
            if( gs2.evaluateposition() > bestsofar_eval):
                bestsofar_eval = gs2.evaluateposition()
                bestsofar_moveblock = moveblock
        # now execute the best sequence of moves
        movesequence = self.gs.executemoveblock(bestsofar_moveblock,threshold_param,True)
        
        if( self.gs.evaluateposition() <= prev_eval):
            if( len( self.gs.stock[0]) > 0):
                self.gs.dealrow()
            else:
                if self.gs.iswon():
                    game_result = 'RESULT = WIN'
                else:
                    game_result = 'RESULT = LOSE'
            
    # now print the stuff
        self.canvas.delete("some_tag")
        data = self.gs.printstate_canvas()
        for datum in data:
            self.canvas.create_text(datum[0],datum[1],text=datum[2],fill=datum[3],font="Courier 10",tag="some_tag")
        if( game_result == 'STILLGOING'):
            self.canvas.create_text(500,300,text='Last Moveblock = ' +self.moveblock2str(movesequence),fill='black',font='Times 12',tag="some_tag")
            self.canvas.create_text(500,350,text='Evaluation = ' + str(self.gs.evaluateposition()), fill='black',font='Times 12',tag="some_tag")
        else:
            self.canvas.create_text(400,300,text=game_result,fill='black',font='Times 20',tag="some_tag")
        return game_result 
        
        
    def execute_every_moveblock(self):
        for dweet in [self.button1, self.button2, self.button3, self.button4]:
            dweet['state'] = tk.DISABLED 
        game_result = self.execute_moveblock()
        if( game_result == 'STILLGOING'):
            self.canvas.after(1000, self.execute_every_moveblock)
        else:
            for dweet in [self.button1, self.button2, self.button3, self.button4]:
                dweet['state'] = tk.NORMAL 
            self.canvas.delete("some_tag")
            data = self.gs.printstate_canvas()
            for datum in data:
                self.canvas.create_text(datum[0],datum[1],text=datum[2],fill=datum[3],font="Courier 10",tag="some_tag")
            self.canvas.create_text(400,300,text=game_result,fill='black',font='Times 20',tag="some_tag")
            
    # convert a moveblock to string for ease of reading 
    def moveblock2str(self, moveblock):
        if( len(moveblock) < 10):
            return str(moveblock)
        else:
            return str(moveblock[0:10]) + '\n' + self.moveblock2str(moveblock[10:len(moveblock)])


if __name__ == "__main__":
    root = tk.Tk()
    ui = UI(root)
    root.mainloop()