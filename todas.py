import modular

ball = list()
char = list()
stick = list()
jokers = list()

def todas(hand, joker):
    global ball, char, stick, jokers

    ball = list()
    char = list()
    stick = list()
    jokers = list()

    for t in hand:
        if t.face is joker.face and t.value is joker.value:
            jokers.append(t)
        elif t.face is modular.TileType.BALL.value:
            ball.append(t)
        elif t.face == modular.TileType.CHARACTER.value:
            char.append(t)
        elif t.face == modular.TileType.STICK.value:
            stick.append(t)


    # done reseting hand, now make sets and check
    pairs = list()
    pairs.extend(_makePairs(ball))
    pairs.extend(_makePairs(char))
    pairs.extend(_makePairs(stick))

    ballSets = _makeStraight(ball)
    charSets = _makeStraight(char)
    stickSets = _makeStraight(stick)
    pongSets = _pair2pong(pairs)


    # 5 sets (15) + 1 pair (2)
    withoutJokerLen = len(ballSets) + len(charSets) + len(stickSets) + len(pongSets)

    if withoutJokerLen == 15 and len(pairs) == 2: # pairs accounted
        return True


    if len(pairs) > len(jokers)+1:
        return False

    # using jokers
    hasPair = True if pairs else False
    # joker test, assuming one
    remJokers = len(jokers)

    # needs pair, len(nonFlores == odd)
    # needs straight len(nonFlores == even)

    for nonFlores in [ball, char, stick]:
        if nonFlores: # items exist
            usedJokers = _jokersUsed(nonFlores, hasPair)
            if usedJokers < 1: # set not found
                return False
            remJokers -= usedJokers

    if remJokers == 0: # all jokers sucessfully used
        return True
    else:
        return False

def _jokersUsed(nonFlores, hasPair):
    '''
    Returns jokers used for valid set
    '''

    if len(nonFlores) == 1: # joker need for pair
        if hasPair: # but we already have a pair
            # assume need a set
            return 2
        else:
            return 1

    usedJokers = 0
    j = 0
    while j < len(nonFlores)-1:
        difference = [t.value - nonFlores[j].value for t in nonFlores[j+1:]]

        if difference[0] < 3: # max difference 2, can make set
            usedJokers += 1
            j += 2

        else: # diff greater than 3, set not viable
            if hasPair: # must be a set
                usedJokers += 2
                j += 2
            else: # must be a pair
                usedJokers += 1
                j += 1

    return usedJokers


def _pair2pong(nonFlores):
        
    sets = list()
    i=0

    while i < len(nonFlores):
        tile = nonFlores[i]

        midIndex = next((j for j, item in enumerate(nonFlores[i+1:]) if item.value == tile.value), None)
        endIndex = next((j for j, item in enumerate(nonFlores[i+2:]) if item.value == tile.value), None) 

        if endIndex is not None and midIndex is not None:
            tempset = list()
            tempset.append( nonFlores.pop(endIndex+i+2) )
            tempset.append( nonFlores.pop(midIndex+i+1) )
            tempset.append( nonFlores.pop(i) )
            tempset.reverse()
            sets.extend(tempset)

        else:
            i+= 1

    return sets



def _makeStraight(nonFlores, testOutput=False):

    sets = list()
    i=0
    while i < len(nonFlores):
            tile = nonFlores[i]
            
            if testOutput:
                print("@",tile,end="\t\t")

            midIndex = next((j for j, item in enumerate(nonFlores[i+1:]) if item.value == tile.value+1), None)
            endIndex = next((j for j, item in enumerate(nonFlores[i+2:]) if item.value == tile.value+2), None) 

            if testOutput:
                print(midIndex+i if midIndex is not None else None, endIndex, end="\n")

            if endIndex is not None and midIndex is not None:
                tempset = list()
                tempset.append( nonFlores.pop(endIndex+i+2) )
                tempset.append( nonFlores.pop(midIndex+i+1) )
                tempset.append( nonFlores.pop(i) )
                tempset.reverse()
                sets.extend(tempset)
                
            else:
                i += 1
    return sets

def _makePairs(nonFlores, testOutput=False):
    pairs = list()

    #'''
    if testOutput:
        print("\nPairs",nonFlores)
        
    i=0
    
    while i < len(nonFlores):
        tile = nonFlores[i]
        if testOutput:
            print("@",tile,end="\t\t")

        # index-1 of relative to current tile
        sameValues = [j if t.value == tile.value else None for j,t in enumerate(nonFlores[i+1:])]

        if any(x != None for x in sameValues):
            pairs.append( nonFlores.pop(i) )
            
            for j in sameValues[::-1]:
                if j != None:                        
                    pairs.append( nonFlores.pop(j+i) )
        else:
            i += 1
    
    if testOutput:
        print("\n\tPairs now ->",pairs, "\n")
    return pairs




def main():
    hand =  [modular.Tile(4, "Character"), modular.Tile(8, "Character"), modular.Tile(8, "Stick"), modular.Tile(6, "Ball"), modular.Tile(6, "Ball"), modular.Tile(7, "Ball"), modular.Tile(7, "Ball"), modular.Tile(7, "Ball"), modular.Tile(2, "Character"), modular.Tile(2, "Character"), modular.Tile(9, "Character"), modular.Tile(9, "Character"), modular.Tile(5, "Stick"), modular.Tile(5, "Stick"), modular.Tile(6, "Character"), modular.Tile(7, "Character"), modular.Tile(8, "Character")]
    '''
    hand = list()
    for i in range(1,10):
        hand.append(modular.Tile(i,"Ball"))

    hand.append(modular.Tile(1,"Ball"))
    hand.append(modular.Tile(1,"Ball"))

    
    hand.append(modular.Tile(2,"Stick"))
    hand.append(modular.Tile(2,"Stick"))
    hand.append(modular.Tile(3,"Stick"))
    #hand.append(modular.Tile(4,"Stick"))
    #hand.append(modular.Tile(5,"Stick"))
    #hand.append(modular.Tile(6,"Stick"))

    hand.append(modular.Tile(7,modular.TileType.CHARACTER.value))
    hand.append(modular.Tile(8,modular.TileType.CHARACTER.value))
    hand.append(modular.Tile(9,modular.TileType.CHARACTER.value))
    '''

    print(hand)
    if todas(hand, modular.Tile(8,"Stick")):
        print("todas")

if __name__ == "__main__":
    main()


    