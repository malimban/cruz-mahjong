
'''

setup
    build mahjong set (144 + 4 blanks)

    mix mahjong

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

from enum import Enum
from rng import shuffleWalls

class TileType(Enum):
    '''
        each is four
        ball, bamboo, char --> 1-9

        flores: 8*4
        
        winds
            east
            south
            west
            north

        dragons
            red
            green
            white

        unique
            flower
            season

        blank tiles
    '''

    __order__ = 'BALL STICK CHARACTER FLORES'
    
    BALL = "Ball"
    STICK = "Stick"
    CHARACTER = "Character"

    FLORES = "Flores" #'winds', 'dragons', 'blanks']


class FloresFace(Enum):
    __order__ = 'EAST SOUTH WEST NORTH RED GREEN WHITE FLOWER SEASON BLANK'

    EAST = "East"
    SOUTH = "South"
    WEST = "West"
    NORTH = "North"

    RED = "Red"
    GREEN = "Green"
    WHITE = "White"

    FLOWER = "Flower"
    SEASON = "Season"

    BLANK = "Blank"

class Tile:

    def __init__(self, value, face):
        self.value = value
        self.face = face

    def __str__(self):
        return str(self.value) + "\t" + str(self.face)

    def __repr__(self):
        '''
        return str(self)
        '''
        return "\t" + str(self.value) + " " + str(self.face)
        #'''
    

def _initWalls():
    walls = list()

    for t in TileType:

        if t == TileType.FLORES:
            for f in FloresFace:
                for i in range(4):
                    walls.append( Tile(t.value, f.value))
            continue

        # generate non-flores
        for n in range(1,10):
            for i in range(4):
                walls.append( Tile(n, t.value))

    return walls


def bldWall(testOutput=False):
    """Return a randomized wall list

    Parameters
    ----------
    testOutput : boolean
        True for test output

    """
    walls = _initWalls()

    if testOutput:
        print("Initial list")

        for w in walls:
            print(w)
        for i in range(3):
            print("\n")

    walls = shuffleWalls(walls)

    if testOutput:
        print("Randomized")    
        for i, w in enumerate(walls):
            print( str(i)+" : " if i%40==0
                    else ""
                , "\t", w)

    return walls


# begin main
if __name__ == "__main__":
    wall = bldWall(True)
