
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

import Wall, math, rng
from player import Player
from rng import rollDice
from enum import Enum
from modular import TileType

#send these over
walls = list()
players = list()
joker = None
mano = None

playerCount = 4
diceCount = 2
earlySawi = False

class PlayerOrder(Enum):
    __order__ = 'SOUTH EAST NORTH WEST'

    SOUTH = 0
    EAST = 1
    NORTH = 2
    WEST = 3


def _findMano(startRoller=PlayerOrder.SOUTH.value, testOutput=False):
        
    if(testOutput):
        print("Starting Player:", startRoller)

    dice = rollDice(diceCount, testOutput)
    sum = 0
    for d in dice:
        sum += d

    if(testOutput):
        for d in dice:
            print("+", d, end=' ')
        print("=", sum)

    # 1, 5, 9 is same as rolled player
    mano = (startRoller+sum)%playerCount -1
    if(mano == -1):
        mano = playerCount-1
    return mano


def _bendWalls():
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


def _breakWall(mano, testOutput=False) -> None:
    """
    Fixes the wall's start and end points
    """
    global walls, earlySawi

    # determine which wall to use
    bWallIndex = _bendWalls()

    # Δ CHANGEME to let mano choose... also if roll > 10, let 11 or 1 be chosen... also set early sawi
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
    result = sum(rollDice(diceCount, testOutput))*2
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
                i = i
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

    pass


def _firstDistrb(testOutput=False):
    '''
    Takes sorted walls and returns list of lists of tiles

    hands[player]   : 0 is Mano
    hands[p][0]     : hand tiles
    hands[p][1]     : flores
    '''
    global walls

    hands = [(list(), list()) for j in range(playerCount)]

    for i in range(playerCount): # first deal
        hands[i][0].extend(walls[:8])
        walls = walls[8:]

    if earlySawi:
        hands[0][0].append(walls.pop(0))

    for i in range(playerCount): # second deal
        hands[i][0].extend(walls[:8])
        walls = walls[8:]

    if not earlySawi:
        hands[0][0].append(walls.pop(0))


    if testOutput:
        print("\nshow hands")
        for h in hands:
            for i, t in enumerate(h[0]):
                print(t)
            print()

    return hands


def _refillFlores(hand):
    '''
    Expecting hand list of tiles, returns hand + flores many new tiles
    '''
    global walls
    newHand = list()
    foundFlores = list()

    for i, tile in enumerate(hand):
        if tile.value is TileType.FLORES.value:
            newHand.append(walls.pop()) # add new tile
            foundFlores.extend(hand[i:i+1])
        else:
            newHand.extend(hand[i:i+1])
    
    return (newHand, foundFlores)


def _genPlayers(hands, testOutput=False):
    global players

    for h in hands:
        players.append(Player(h[0], list()))
            
    if testOutput:
        print("show Player class")
        for i, p in enumerate(players):
            print("Player",i,"\t",p)


def _distrbAllFlores(testOutput=False):
    doneDistrb = [False]*playerCount
    pIndex = 0
    while False in doneDistrb:
        if not doneDistrb[pIndex]:
            sortedTiles = _refillFlores(players[pIndex].hand)
            newHand = sortedTiles[0]
            addFlores = sortedTiles[1]

            players[pIndex].hand = newHand
            
            if not addFlores: #empty
                doneDistrb[pIndex] = True
            else:
                players[pIndex].flores.extend(addFlores)
        
        pIndex += 1
        if pIndex == playerCount:
            pIndex = 0

    if testOutput:
        print("\n\n\nshowing that there are no flores in hand")
        for i, p in enumerate(players):
            print("\n\nPlayer",i,"\t")

            print("tiles, count",len(p.hand))
            for tile in p.hand:
                print(tile, end="\t\t")

            print("\nbegin flores, count",len(p.flores))
            for flores in p.flores:
                print(flores, end="\t\t")


def _findJoker(testOutput=False):
    global walls
    nonJokers = list()

    # mano roll
    result = sum(rollDice(diceCount, testOutput))

    # check if flores starts on bottom or top
    result = result * 2 - 1
    joker = walls.pop(result)

    if joker.value is TileType.FLORES.value:
        nonJokers.append(joker)
        joker = walls.pop(result)

        # joker can't be flores
        if joker.value is TileType.FLORES.value:
            nonJokers.append(joker)
            allDone = _findJoker() # check again to get the right values
            joker = allDone[0]
            nonJokers.extend( allDone[1] )

    if testOutput:
        print("\n\nJoker is", joker)
        print("flores is")
        for t in nonJokers:
            print(t)
    
    return (joker, nonJokers)


def initMahjong(startRoller=PlayerOrder.SOUTH.value, isQuantum=False, diceCountIn=2, playerCountIn=len([p.value for p in PlayerOrder]), testOutput=False):
    global diceCount, playerCount, walls, joker, mano, players

    rng.quantum = isQuantum

    # error chk
    if startRoller > playerCount:
        print("startRoller must be less than playerCount")
        return EnvironmentError


    diceCount = diceCountIn
    playerCount = playerCountIn

    #''' invertable comments
    walls = Wall.bldWall(testOutput)
    ''' 
    walls = list()  # [i for i in range(148)]
    for i in range(148):
        walls.append(i)
    '''#'''

    # P0 roll, determine mano
    mano = _findMano(startRoller, testOutput=testOutput)
    if testOutput:
        print("Mano:", mano)

    # distribute
    _breakWall(mano, testOutput)
    hands = _firstDistrb(testOutput)
    _genPlayers(hands, testOutput)

    # flores
    _distrbAllFlores(testOutput)

    # joker
    jokening = _findJoker(testOutput)
    joker = jokening[0]
    players[mano].flores.extend(jokening[1])


    # verify everything
    if testOutput:
        print("\n\nbegin verify")
        for i, p in enumerate(players):
            print("\nPlayer",i,"\t")

            print("tiles, count",len(p.hand))
            for tile in p.hand:
                print(tile, end="\t\t")

            print("\nbegin flores, count",len(p.flores))
            for flores in p.flores:
                print(flores, end="\t\t")
            print()

    return players



# begin main
if __name__ == "__main__":
    initMahjong(testOutput=True)
