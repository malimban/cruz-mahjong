
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


'''

from modular import TileType, FloresFace, Tile
from rng import shuffleWalls



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
