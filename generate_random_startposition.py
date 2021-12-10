#######################
#
#  Generate random start position
#
#######################

import sys
from card import Card
from gamestate import Gamestate


# this will generate a random position and write to myfile.txt

gs = Gamestate()
gs.init_random()
gs.print_state(sys.argv[1])
print('written to ', sys.argv[1])
print('finished!')
