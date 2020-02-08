
'''

setup
    [x] build mahjong set (144 + 4 blanks) 

    [x] mix mahjong

    roll dice

    distribute initial

    flores & back


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

def _rollDice(): # replace with quantum
    DMIN = 1
    DMAX = 6

    d1 = randint(DMIN,DMAX)
    d2 = randint(DMIN,DMAX)

    return (d1, d2)

def _findMano():
    dice = _rollDice()

    sum = dice[1] + dice[0]

    print(dice[0], dice[1], sum)

def _bendWalls(walls=list()):
    startWallIndex = len(walls)

    return startWallIndex

def _distributeInit():

    return None
 
import Wall
from random import randint # replace with quantum

wall = Wall.bldWall()
print (_bendWalls(wall))