
'''

setup
    [x] build mahjong set (144 + 4 blanks) 

    [x] mix mahjong

    [x] roll dice

    [x] associate wall with player

    [x] distribute initial

    [x] flores & back


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

import Distribute
import player
from player import Player, BasicAI, discardsDict, declareds

#take from Distribute
walls = list()
players = list()

#send to Distribute
useQuantum = False
playerCount = 4
diceCount = 2
earlySawi = False

mano = AttributeError
getPlayer = AttributeError
discards = list()

def _newGame(startRoller, testJoker=False):
    global walls, players, mano, getPlayer

    if not players:
        money = [1000] * playerCount
    else:
        for i, p in enumerate(players):
            money[i] = p.money

    # set paraams method? Δ CHANGEME
    
    Distribute.initMahjong(startRoller, useQuantum, diceCount, playerCount)
    walls = Distribute.walls
    players = Distribute.players
    if testJoker:
        print("joker dist",Distribute.joker, "  player", player.joker)
    player.joker = Distribute.joker
    mano = Distribute.mano
    getPlayer = _generatePlayer(mano)

    for i, p in enumerate(players):
        p.money = money[i]

    print("First mano:", mano)

    # regenerate discards
    import modular
    discards = list()
    discardsDict = dict()

    for t in modular.TileType:
        if t is modular.TileType.FLORES:
            continue
        else:
            for n in range(1,10):
                discardsDict[modular.Tile(n, t.value)] = 0

    declareds = discardsDict.copy()


def _generatePlayer(index=0):
    '''
    yields the next player to make a choice
    '''
    while True:
        if index >= len(players):
            index=0
        
        yield players[index]

        index += 1
        

def _chkPongable(tile, testOutput=False):
    '''
    Lets players pong if they can, starting from the first player clockwise from the mano

    If someone does pong, automatically update so that the next getPlayer will be the new mano
    '''
    global getPlayer, mano

    player = mano # if 3

    #if testOutput:
    print("try pong", end=" ")

    # 3 tapon,
    # start @ 0: 1 -> 2 end 
    #
    # outdated 
    # -> 3 end
    for i in range(playerCount-1):
        #if testOutput:
        print(player.num, end=" ")

        if player.pong(tile, testOutput):
            mano = player
            return True

        player = next(getPlayer)
        # 0 -> 1
        # 1 -> 2
        # 2 -> 3


    print()
    
    # no one ponged, reset getPlayer to 0
    next(getPlayer) # 3 -> 0

    return False

def main(testOutput = False):
    global walls, players, discards, mano, getPlayer
    
    _newGame(0, testJoker=testOutput)
    # where is the early sawi choice?? CHANGEME Δ

    if testOutput:
        print("discards", discards)

    
    aiCount = 3

    Player.i = len(players) - aiCount
    for i in range(aiCount+1): # player to ai
        if i == 0:
            continue
        else:
            players[i] = BasicAI(players[i].hand, players[i].flores)

    # first sort
    for p in players:
        p.sortHand(firstSort=True)

    winner = False
    mano = next(getPlayer) 

    # end setup
    
    while winner is False:

        # chk for win
        if mano.todas():
            print("Player",mano.num,"wins")
            print(mano)
            break

        # throw one
        print("Discards", discards)
        print()

        tapon = mano.tapon()
        if tapon is None:
            tapon = mano.randTapon()

        print("P", mano.num, " tapon:",tapon)

        mano = next(getPlayer) # 2 -> 3
        
        # move counter-clockwise
        # pong intercept, go back to throw one
        if _chkPongable(tapon):
            print("\nPONG! P", mano.num)
            continue
        print("\nno pong")

        # chao, go back to throw one
        if mano.chao(tapon):
            print("\nCHAO! p", mano.num)
            continue
        print("no chow\n")


        discards.append(tapon)

        # draw + throw(reset loop)
        try:
            if not mano.bunot(walls.pop(0)): #reg bunot
                while True: #flores bunot
                    if mano.bunot(walls.pop()):
                        break
        except IndexError:
            print("No winner")
            break
            


    # reset, make new game


def testDict():
    dictionary = dict()
    import Wall

    tiel = Wall.Tile(9, "Ball")

    for t in Wall.TileType:
        if t is Wall.TileType.FLORES:
            continue
        for n in range(1,10):
            tile = Wall.Tile(n, t.value)
            dictionary[tile] = 0

            '''
            if n == tiel.value and t.value == tiel.face:
                print(tiel == tile)
            if tile.value == tiel.value and tile.face == tiel.fa1ce: 
                t1 = (tiel.value, tiel.face)
                t2 = (tile.value, tile.face)
                print(t1, t2, t1 == t2)
                print(tile.__eq__(tiel)) # WHAAAAAAAAAT
            '''

    print(dictionary, len(dictionary))


    tiel = Wall.Tile(9, Wall.TileType.BALL.value)
    dictionary[tiel] = dictionary.get(tiel, 0) + 1

    print(dictionary, len(dictionary))

    return

# begin main
if __name__ == "__main__":
    main(True)
    #testDict()
