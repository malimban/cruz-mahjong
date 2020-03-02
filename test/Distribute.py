
'''

setup
    [x] build mahjong set (144 + 4 blanks) 

    [x] mix mahjong

    [x] roll dice

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

import Wall, math
from random import randint # replace with quantum
from enum import Enum


diceCount = 2
playerCount = 4
earlySawi = False

class PlayerOrder(Enum):
    __order__ = 'SOUTH EAST NORTH WEST'

    SOUTH = 0
    EAST = 1
    NORTH = 2
    WEST = 3


def _rollDice(testOutput=False): # CHANGEME replace with quantum
    DMIN = 1
    DMAX = 6

    dice = list()
    for i in range(diceCount):
        dice.append(randint(DMIN, DMAX))

    if testOutput:
        print("\nrolld: ",end='')
        for d in dice:
            print(d, end=' ')
        print()

    return dice


def _findMano(startPlayer=PlayerOrder.SOUTH.value, testOutput=False):
        
    if(testOutput):
        print("Starting Player:", startPlayer)

    dice = _rollDice(testOutput)
    sum = 0
    for d in dice:
        sum += d

    if(testOutput):
        for d in dice:
            print("+", d, end=' ')
        print("=", sum)

    # 1, 5, 9 is same as rolled player
    mano = (startPlayer+sum)%playerCount -1
    if(mano == -1):
        mano = playerCount-1
    return mano


def _bendWalls(walls=list()):
    """Return a tuple of begining index wall positions

    Parameters
    ----------
    walls : list
        Expecting a 148-len wall

    """
    
    increm = len(walls) / playerCount
    
    #           0       1       2           3
    #         South    East    North      West
    wallStart = list()

    for p in range(playerCount):
        index = math.ceil(p*increm)
        if index % 2 == 0:
            wallStart.append(index)
        else:
            wallStart.append(index-1)

    return wallStart


def _breakWall(mano, walls, testOutput=False):
    """
    Fixes the wall's start and end points
    """
    global earlySawi

    # determine which wall to use
    bWallIndex = _bendWalls(walls)

    # CHANGEME to let mano choose... also if roll > 10, let 11 or 1 be chosen... also set early sawi
    fromWall = (                            # [0] = mano wall use, [1] == True : right to left
        #((mano+2)%playerCount), False)      # assuming directlly across, clockwise
        ((mano+1)%playerCount),True)      #assuming right, counterclock 
        #((mano+3)%playerCount), False)       # assuming left, clockwise
    adjacentRight = mano - fromWall[0]

    if testOutput:
        print("StartPos",bWallIndex)
        print("UseWall:",fromWall, "r to l" if fromWall[1]
                                    else "l to r"
        )

    # roll again
    result = sum(_rollDice(testOutput))*2
    startIndex = None

    # subsection wall, reverse, append to flores side
    if adjacentRight == -1:
        startIndex = bWallIndex[fromWall[0]] + result
        bunot = walls[startIndex:]

        # need to group by pairs, invert, then readd
        flores = walls[:startIndex]
        flores.reverse()
        walls = bunot + flores        

    else: # can choose direction
        if fromWall[1]: # counterclock, r to l--the usual
            print("\tright to left")
            startIndex = bWallIndex[fromWall[0]] + result
            
            bunot = walls[startIndex:]
            flores = walls[:startIndex]
            flores.reverse()
            walls = bunot + flores
        else:
            print("\tleft to right")
            startIndex = None
            try:
                startIndex = bWallIndex[fromWall[0]+1] - result
            except:
                startIndex = bWallIndex[0] - result
            print(startIndex)

            bunot = walls[:startIndex]
            bunot.reverse()
            flores = walls[startIndex:]
            flores.reverse()

            # pair and reverse bunot
            tempBunot = list()
            
            for i in range(len(bunot)//2,0,-1):
                tB = bunot.pop()
                tempBunot.append(bunot.pop())
                tempBunot.append(tB)  
            
            
            bunot = tempBunot
            bunot.reverse()
            
            walls = bunot + flores
            
    if testOutput:
        print("Starting")
        if fromWall[1]:
            print("before",startIndex)
        else:
            print("after", startIndex)

        for i, t in enumerate(walls):
            print(t)

    return walls


def _firstDistrb(walls, testOutput=False):
    '''
    Takes sorted walls and returns list of lists of tiles
    '''
    hands = [[] for j in range(playerCount)]

    for i in range(playerCount): # first deal
        hands[i%playerCount].extend(walls[:8])
        walls = walls[8:]

    if earlySawi:
        hands[0].append(walls.pop(0))

    for i in range(playerCount): # second deal
        hands[i%playerCount].extend(walls[:8])
        walls = walls[8:]

    if not earlySawi:
        hands[0].append(walls.pop(0))


    if testOutput:
        print("\nshow hands")
        for h in hands:
            for i, t in enumerate(h):
                print(t)
            print()

    return hands
'''


def initMahjong(startPlayer=PlayerOrder.SOUTH.value, diceCountIn=2, playerCountIn=len([p.value for p in PlayerOrder]), testOutput=False):
    global diceCount, playerCount

    diceCount = diceCountIn
    playerCount = playerCountIn

    #'''
    walls = Wall.bldWall(True)
    ''' 
    walls = list()
    for i in range(148):
        walls.append(i)
    '''#'''

    # P0 roll, determine mano
    mano = _findMano(startPlayer)#, testOutput=testOutput)
    if testOutput:
        print("Mano:", mano)

    # distribute
    walls = _breakWall(mano, walls, testOutput=testOutput)
    hands = _firstDistrb(walls, testOutput=testOutput)
    
    # flores

    # joker


# begin main
if __name__ == "__main__":
    initMahjong(testOutput=True)