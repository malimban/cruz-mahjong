
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

#take from Distribute
walls = list()
players = list()
joker = None
discards = list()

useQuantum = False
playerCount = 4
diceCount = 2
earlySawi = False

mano = None
getPlayer = None

def _newGame(startRoller):
    global walls, players, joker, mano, getPlayer

    # set paraams method? Δ CHANGEME
    
    Distribute.initMahjong(startRoller, useQuantum, diceCount, playerCount)
    walls = Distribute.walls
    players = Distribute.players
    joker = Distribute.joker
    mano = Distribute.mano
    getPlayer = _generatePlayer(mano)


def _generatePlayer(index=0):
    while True:
        if index >= len(players):
            index=0

        if len(players[index].hand) > 16:
            yield players[index]
        else:
            print("I don't think Player",index,"is before the new mano...")
            raise IndexError

        index += 1
        

def _chkPongable(tile):
    '''
    Lets players pong if they can, starting from the first player clockwise from the mano

    If someone does pong, automatically update so that the next getPlayer will be the new mano
    '''
    global getPlayer

    # if start @ 0: 1 -> 2 -> 3 end
    for i in range(playerCount-1):
        player = next(getPlayer)
        if player.pong(tile):                
            return True
    
    # no one ponged, make next getPlayer 1
    next(getPlayer) # 3 -> 0

    return False

def main():
    global walls, players, joker, discards, mano, getPlayer
    
    # VV replace with function above?? CHANGEME Δ 
    Distribute.initMahjong(0, useQuantum, diceCount, playerCount)
    walls = Distribute.walls
    players = Distribute.players
    joker = Distribute.joker
    getPlayer = _generatePlayer()
    # where is the early sawi choice?? CHANGEME Δ

    winner = False
    
    while winner is False:

        # chk for win

        # throw one
        mano = next(getPlayer)
        tapon = mano.tapon()
        
        # move counter-clockwise
        # pong intercept, go back to throw one
        if _chkPongable(tapon):
            continue

        # chao, go back to throw one
        

        # draw+throw
        


    # reset, make new game

# begin main
if __name__ == "__main__":
    main()
