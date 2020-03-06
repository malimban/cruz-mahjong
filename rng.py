
from random import randint 
import random

quantum = False

def rollDice(diceCount=2, testOutput=False):
    if quantum:
        pass
    else:
        dice = _rollPseudo(diceCount)

    return dice

def shuffleWalls(walls = list()):
    if quantum:
        pass
    else:
        random.shuffle(walls) 

    return walls
    
        

def _rollPseudo(diceCount=2, testOutput=False): 
    DMIN = 1
    DMAX = 6

    dice = list()
    for i in range(diceCount):
        dice.append(randint(DMIN, DMAX))
        i = i

    if testOutput:
        print("\nrolld: ",end='')
        for d in dice:
            print(d, end=' ')
        print()

    return dice
