# compute best moveblock

import random
import sys
from gamestate import Gamestate
import copy
import numpy as np
import time
random.seed(123456)

if( len(sys.argv) != 2):
    print('usage: calculate_equity.py filename numattempts')
    exit()


filename = sys.argv[1]
print('the filename is ', filename)

gs = Gamestate()
gs.init_filename(filename)
print("current eval = ", gs.evaluateposition())
for attempt in range(1): # only one attempt
    for undef in range(1): # maky only one move during our only attempt
        threshold_param = 2

        prev_eval = gs.evaluateposition()
        numtries = 3
        bestsofar_moveblock = []
        bestsofar_eval = gs.evaluateposition()
                
        # find the best sequence of moves
        for mytry in range(numtries):
            moveblock = np.random.randint(1000,size=30)
            gs2 = copy.deepcopy(gs)
            gs2.executemoveblock(moveblock,threshold_param,False)
            if( gs2.evaluateposition() > bestsofar_eval):
                bestsofar_eval = gs2.evaluateposition()
                bestsofar_moveblock = moveblock
        # now execute the best sequence of moves
        gs.executemoveblock(bestsofar_moveblock,threshold_param,True)
        if( gs.evaluateposition() <= prev_eval):
            if( len( gs.stock[0]) > 0):
                gs.dealrow()                

print('the resulting game state is now: ')
gs.print_state()
print("NOW current eval = ", gs.evaluateposition())
