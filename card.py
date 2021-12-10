import numpy as np

class Card():

    '''

    class for Card
    Cards have a rank, suit, and an "isvisible" flag

    '''

    # constructor

    
    def __init__(self,string): # example  'Qs' -> visible Queen of Spades or '-0h' -> not visible Ten of Hearts
        foo = {'A':1, '2':2, '3':3, '4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'0':10,'J':11,'Q':12,'K':13}
        if(string == None):
            self.rank = None
            self.suit = None
        else:
            if(string[0] == '-'):
                self.isvisible = False
                self.rank = foo[string[1]]
                self.suit = string[2]
            else:
                self.rank = foo[string[0]]
                self.suit = string[1]
                self.isvisible = True
    
    
    def printcard(self):
        print(self.rank)
        print(self.suit)
        print(self.isvisible)
        
    def issamesuit(self,othercard):
        return othercard.suit == self.suit
    
    def getsuit(self):
        return self.suit
    def getrank(self):
        return self.rank
    
    def setvisible(self,flag):
        self.isvisible = flag
    
    # nextrank = 1 higher, e.g. if I am the 6 of hearts then any 7 is the next rank
    def isnextrank(self,othercard):
        return othercard.rank == self.rank + 1
    
    # prevrank = 1 lower, e.g. if I am the 6 of hearts then any 5 is the prev rank
    def isprevrank(self,othercard):
        return othercard.rank == self.rank -1
    
    def card2string(self):
        foo = {1:'A',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'0',11:'J',12:'Q',13:'K'}
        bar = '-'
        if( self.isvisible):
            bar = ''
        return bar + foo[self.rank] + self.suit
    
    # convert a card to a number between 0 and 51
    def card2id(self):
        dweet = {'c':0,'d':1,'h':2,'s':3}
        number = dweet[self.suit] * 13 + self.rank - 1
        return number
    
    # convert number between 0 and 51 to a card
    @staticmethod
    def id2card(myid):
        c = Card('Ac') # arbitrary choice of Ac
    
        dweet = {0:'c',1:'d',2:'h',3:'s'}
        c.suit = dweet[np.floor(myid/13)]
        c.rank = myid % 13 + 1
        return c
