
'''

setup
    [x] build mahjong set (144 + 4 blanks) 

    [x] mix mahjong

    [ ] roll dice

    [ ] associate wall with player

    [ ] distribute initial

    [ ] flores & back


play
    throw one
    
    counter-clockwise
        pong intercept, go back to throw one

        chao, go back to throw one

        win anyhow
    
    draw+throw


winning
    calculate payment


'''

import Wall
from random import randint # replace with quantum
from enum import Enum


class PlayerOrder(Enum):
    __order__ = 'SOUTH EAST NORTH WEST'

    SOUTH = 0
    EAST = 1
    NORTH = 2
    WEST = 3


def _rollDice(diceCount=2, testOutput=False): # replace with quantum
    DMIN = 1
    DMAX = 6

    dice = list()
    for i in range(diceCount):
        dice.append(randint(DMIN, DMAX))

    if testOutput:
        print("rolld: ",end='')
        for d in dice:
            print(d, end=' ')
        print("\n")

    return dice

def _findMano(startPlayer=PlayerOrder.SOUTH.value, diceCount=2, playerCount=4,  testOutput=False):
    dice = _rollDice(diceCount)

    sum = 0
    for d in dice:
        sum += d

    if(testOutput):
        print("Starting Player:", startPlayer)

        for d in dice:
            print("+", d, end=' ')
        print("=", sum)

    # 1, 5, 9 is same as rolled player
    mano = (startPlayer+sum)%playerCount -1
    if(mano == -1):
        mano = playerCount-1
    return mano


def _bendWalls(walls=list()):
    """Return a tuple of 

    Parameters
    ----------
    walls : list
        Expecting a 148-len wall

    """
    increm = len(walls)
    
    #           0       1       2           3
    #         South    East    North      West
    wallStart = (0, 1*increm, 2*increm, 3*increm)

    return wallStart

def _distributeInit(mano, wall, earlySawi=False, diceCount=2):

    # roll again
    _rollDice(diceCount)

    # subsection wall, reverse, append to flores side

    # distribute

    return None






def initMahjong(startPlayer=PlayerOrder.SOUTH.value, diceCount=2, playerCount=len([p.value for p in PlayerOrder]), testOutput=False):
    wall = Wall.bldWall()

    # P0 roll, determine mano
    mano = _findMano(startPlayer, testOutput=testOutput)
    if testOutput:
        print("Mano:", mano)

    # distribute

    # flores

    # joker


# begin main
if __name__ == "__main__":
    initMahjong(testOutput=True)