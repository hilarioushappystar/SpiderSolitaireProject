###########################################
#  This is the ai_module class
#  This class handles the "clever stuff" such as working out best move(s) to play
###########################################

# achieves 10% win rate in 50 games (more thorough testing may be warranted)

import numpy as np
from numpy import random 
from gamestate import Gamestate
from card import Card
import copy

def evaluate_position(gs, cfgh):        
        myeval = 100 * gs.countsuitsremoved() + gs.countsuitedbuilds() + 10*(44 - gs.counthiddencards())
        
        # do columns without face-down cards
        for foo in range(10):
            if( len( gs.columns[foo] ) == 0):
                myeval += cfgh.emptycolumnsweight
            elif( gs.columns[foo][0].isvisible):
                myeval += cfgh.emptycolumnsweight
                
        # do pollution 
        for foo in range(10):
            poll = gs.compute_pollution(foo)
            if( poll == 1):
                myeval += 2 * cfgh.pollutionweight
            if( poll == 2):
                myeval += 1 * cfgh.pollutionweight
                
        # do max run length (preparing to complete suits is very important at the 4-suit level!)
        for suit in ['c','d','h','s']:
            # no scientific basis for choosing these numbers!
            tempdict = {6:1.06, 7:2.07, 8:5.08, 9:10.09, 10:20.10, 11:30.11, 12:40.12}
            runlength = gs.compute_maxrunlength(suit)
            if( runlength in tempdict):
                myeval += tempdict[runlength] * cfgh.maxrunlengthweight  
        
        return myeval


# choose the best moveblock to play 
def choose_moveblock(gs, cfgh):
    random.seed(123456)
    threshold_param = 2
    game_result = 'STILLGOING'
    prev_eval = evaluate_position(gs,cfgh)
    
    numtries = cfgh.moveblocktries
    bestsofar_moveblock = []
    bestsofar_eval = evaluate_position(gs,cfgh)
    for mytry in range(numtries):
        
        moveblock = np.random.randint(1000,size=cfgh.moveblocklength)
        
         
        # randomly truncate 
        randsize = 1 + random.randint(cfgh.moveblocklength-1)
        moveblock = moveblock[0:randsize]
        
        # now attempt both static and look-ahead evaluation    
        gs2 = copy.deepcopy(gs)
        gs2.executemoveblock(moveblock,threshold_param,False)
        gs3 = copy.deepcopy(gs)
        gs3.executemoveblock(moveblock,threshold_param,True)
        avg_eval = 0.5 * (evaluate_position(gs2,cfgh) + evaluate_position(gs3,cfgh))
        
        if( avg_eval > bestsofar_eval):
            bestsofar_eval = avg_eval 
            bestsofar_moveblock = moveblock
        if( avg_eval == bestsofar_eval and len(moveblock) < len(bestsofar_moveblock)):
            bestsofar_eval = avg_eval 
            bestsofar_moveblock = moveblock        
    movesequence = gs.executemoveblock(bestsofar_moveblock,threshold_param,True)
        
    if( evaluate_position(gs,cfgh) <= prev_eval):
        if( len( gs.stock[0]) > 0):
            gs.dealrow()
        else:
            if gs.iswon():
                game_result = 'RESULT = WIN'
            else:
                game_result = 'RESULT = LOSE'
    return (movesequence, game_result)