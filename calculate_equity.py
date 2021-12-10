###########################
#
# calculate equity
#
###########################

# given an input file, estimate the probability of winning
# with a "smart random-move algorithm"


import random
import sys
from gamestate import Gamestate
import copy
import numpy as np
import time
random.seed(123456)


if( len(sys.argv) != 3):
    print('usage: calculate_equity.py filename numattempts')
    exit()

filename = sys.argv[1]
print('the filename is ', filename)
numattempts = int(sys.argv[2])
print('numattempts = ', numattempts)

gs = Gamestate()
gs.init_filename(filename)

threshold_param = 2  # attempts to change this only trash the win rate!
numwins = 0
start_time = time.time()

for attempt in range(numattempts):
    gs = Gamestate(); gs.init_filename(filename)
    # make sure the input file is not corrupt (e.g. having nine or more kings)
    if( attempt == 0):
        gs.print_state()    
        gs.sanity_check()
        
    while(True):
        prev_eval = gs.evaluateposition()
        numtries = 100
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
            else:
                break
    # game over, work out whether we won or lost
    if(gs.iswon()):
        numwins+=1
        print('w',end='',flush=True) 
    else:
        print('-',end='',flush=True)

print('\nthis many wins: ', numwins)  

end_time = time.time()

print("time taken = %s seconds" % (time.time() - start_time))




        
