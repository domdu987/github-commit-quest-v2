#!/bin/bash
cd $(dirname $0)
./regrade.sh s34 34 982 1016 982 1015 "FOLLOW the barrel in, PUNCH 15 % on the clunk (g 1005)"
./regrade.sh s14 14 353 396 353 395 "FOLLOW the model tank (3/4 top-down), then PULL / swoop to the engineer's face"
./regrade.sh s62 62 1813 1843 1813 1842 "lateral slide from the water tank to the Mark I"
./regrade.sh s01 1+2 0 44 0 43 "PUSH in through the doors (wide to close), eased"
echo ALLDONE
