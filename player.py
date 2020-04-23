
import modular
#import Distribute # really jus tfor joker

'''
from Distribute import joker
'''
#joker = modular.Tile(1, modular.TileType.BALL.value) 
joker = AttributeError # why does this not change, see #93 GH
discards = list()
declareds = list()
#'''

class Player:

    i = 0

    def __init__(self, hand, flores, money=1000):
        self.hand = hand
        self.flores = flores
        self.money = money
        
        self.ball = list()
        self.stick = list()
        self.char = list()
        self.jokers = list()

        self.declared = list()
        #self.kang = list()

        self.num = Player.i
        Player.i += 1

    def __str__(self):
        return "P" + str(self.num) + "  " + str(self.hand) + "\tlen " + str(len(self.hand)) + ", "  + str(self.declared) + "\nFlores:\t" + str(self.flores) + "\tlen " + str(len(self.flores)) + "\nJoker:\t" + str(self.jokers) + "\tlen " + str(len(self.jokers)) + "\n"

    def _setFace(self, tile):
        '''
        return list of tile's face
        '''
        if tile.face == modular.TileType.BALL.value:
            return self.ball
        elif tile.face == modular.TileType.STICK.value:
            return self.stick
        elif tile.face == modular.TileType.CHARACTER.value:
            return self.char
        return IOError(tile.face + "not allowed")

    def _place(self, tile):
        global joker

        if tile.value == modular.TileType.FLORES.value:
            self.flores.append(tile)
            return False
        elif tile.face == joker.face and tile.value is joker.value:
            self.jokers.append(tile)
        else:
            self._setFace(tile).append(tile)

        return True

    def sortHand(self, firstSort=False, testOutput=False):
        if firstSort:            
            for tile in self.hand:
                self._place(tile)
            if testOutput:
                print("Joker", joker)
                print("\nfirst",end="")

        if testOutput:
            print("P" + str(self.num) ,self.ball, self.stick, self.char, self.jokers, sep="\n\t")

        self.ball = sorted(self.ball, key=lambda tile: tile.value)
        self.stick = sorted(self.stick, key=lambda tile: tile.value)
        self.char = sorted(self.char, key=lambda tile: tile.value)
        sortedHand = self.ball + self.stick + self.char + self.jokers

        
        #if len(self.hand) == len(sortedHand) or len(self.hand)+1 == len(sortedHand):
        if len(sortedHand) + len(self.declared) == 17: # 17CHANGEME REMOVEME
            self.hand = sortedHand
        elif firstSort and len(sortedHand) == 16:
            self.hand = sortedHand
        else:
            print("Hand != sortedHand on p",self.num)
            print("len old hand",len(self.hand),self.hand)
            print("len new hand",len(sortedHand),sortedHand)
            print("from",self.ball, self.stick, self.char, self.jokers, sep="\n\t")
            raise Exception
        return True

    def bunot(self, tile, testOutput=False):
        """
        Returns True on a non-flores bunot
        """
        if testOutput:
            print("P",self.num," bunot", tile)

        # properly append if applicable
        if not self._place(tile): #it was flores
            return False


        # tile in proper face, put it in hand for display purposes

        if testOutput:
            print("\nhand b4", self.hand, len(self.hand), self.declared)

        self.hand.append(tile)

        if testOutput:
            print("\nhand now", self.hand, len(self.hand), self.declared)

        self.sortHand(testOutput=testOutput)
        return True

    def decideAction(self):
        raise NotImplementedError()

    def tapon(self):
        """
        Given a 17-long (18 on a kang with regular win)
        remove a tile from hand and return it
        """
        #'''

        for i, t in enumerate(self.hand): # display throwable
            print(i,":",t)

        throw = AttributeError
        while True:
            throwIndex = int(input("Throw what?\n> "))
            if throwIndex < len(self.hand):
                throw = self.hand[throwIndex]
                break
        
        useFace = self._setFace(throw)
        
        indexOfRemove = [j if t.value == throw.value else None for j,t in enumerate(useFace)]
            
        for i in indexOfRemove:
            if i is not None:
                useFace.pop(i)
                break

        return throw

    def pong(self, tile, testOutput=False):
        tface = self._setFace(tile)

        sameValues = [j if t.value == tile.value else None for j,t in enumerate(tface)]

        if len(sameValues) - sameValues.count(None) > 1: # at least 2 ; can pong

            if len(sameValues) - sameValues.count(None) > 2: # kang
                print("no kang yet")
                raise NotImplementedError

            while True:
                print(self.hand)
                choice = input("Pong " + str(tile) + "?\n(y)es or (n)o\n> ")
                if choice == "y":
                    for i in sameValues[::-1]:
                        self.declared.append( tface.pop(i) )
                    self.declared.append(tile)

                    return True
                elif choice == "n":
                    return False

        else: #can't pong
            return False

    def chao(self, tile, testOutput=False):
        tface = self._setFace(tile)
        print(tface)
        choice = input("Chao " + str(tile) + "?\n(y)es or (n)o\n> ")
        if choice == "y":
            while True:
                for i, t in enumerate(tface):
                    print(i,":",t)
                    
                # get two tiles from tface
                chao1 = int(input("First tile index: "))
                chao2 = int(input("Second tile index: "))

                if chao2 < chao1:
                    temp = chao1
                    chao1 = chao2
                    chao2 = temp

                # chk if valid straight
                tempChao = [tface[chao1], tface[chao2], tile]
                tempChao = sorted(tempChao, key=lambda tile: tile.value)

                if tempChao[0].value + 1 == tempChao[1].value and tempChao[1].value + 1 == tempChao[2].value:
                    # valid
                    tface.pop(chao2)
                    tface.pop(chao1)

                    self.declared.extend(tempChao)

                    return True
                
                # reset loop
                if input("Not a straight. (q)uit chao?\n> ") == "q":
                    break

        return False
        

    
class BasicAI(Player):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.pairs = list()
        self.sets = list()
        #self.almostSets = list()
        #self.rem = list()

    def sortHand(self, firstSort=False, testOutput=False):
        #super(self.__class__, self).sortHand(firstSort)
        if firstSort:
            for tile in self.hand:
                self._place(tile)
            if testOutput:
                print("\nfirst",end="")
        else:
            #ΔCHANGEME chk for seven pairs first
            self._resetPairs(testOutput)

        if testOutput:
            print("P" + str(self.num) ,self.ball, self.stick, self.char, self.jokers, 
            self.declared, self.pairs, self.sets, sep="\n\t")

        self.ball = sorted(self.ball, key=lambda tile: tile.value)
        self.stick = sorted(self.stick, key=lambda tile: tile.value)
        self.char = sorted(self.char, key=lambda tile: tile.value)

        if testOutput:
            print("\npairs b4 group", self.pairs)

        self._group(self.ball, testOutput)
        self._group(self.char, testOutput)
        self._group(self.stick, testOutput)

        if testOutput:
            print("\npairs after group", self.pairs)

        sortedHand = self.ball + self.stick + self.char + self.jokers + self.pairs + self.sets 

        if len(sortedHand) == 15:
            print("wy ->", sortedHand)
            raise Exception

        #if len(self.hand) == len(sortedHand) or len(self.hand)+1 == len(sortedHand):
        if len(sortedHand) + len(self.declared) == 17: # 17CHANGEME REMOVEME
            self.hand = sortedHand
        elif firstSort and len(sortedHand) == 16:
            self.hand = sortedHand
        else:
            print("\nHand != sortedHand on p",self.num)
            print("len old hand",len(self.hand),self.hand)
            print("len new hand",len(sortedHand),sortedHand)
            print("from",self.ball, self.stick, self.char, self.jokers,
            self.declared, self.pairs, self.sets, sep="\n\t")
            raise Exception


    def _group(self, nonFlores, firstSort=False, testOutput=False):
        # ΔCHANGEME action based on 7 pairs
        if nonFlores:
            self._makeStraight(nonFlores, testOutput)
            self._makePairs(nonFlores, testOutput)

    def _resetPairs(self, testOutput):
        for i in range(len(self.pairs)):
            tile = self.pairs.pop()
            self._setFace(tile).append(tile)

    def _makeStraight(self, nonFlores, testOutput=False): 

        if testOutput:
            print("\nchk 4 straight",nonFlores)

        i=0
        while i < len(nonFlores):
            tile = nonFlores[i]
            
            if testOutput:
                print("@",tile,end="\t\t")

            midIndex = next((j for j, item in enumerate(nonFlores[i+1:]) if item.value == tile.value+1), None)
            endIndex = next((j for j, item in enumerate(nonFlores[i+2:]) if item.value == tile.value+2), None) 

            # ΔCHANGEME may need this when checking lists of mixed suits
            #midIndex = next((j for j, item in enumerate(nonFlores[i+1:]) if item.value == tile.value+1 and item.face == tile.face), None)
            #endIndex = next((j for j, item in enumerate(nonFlores[i+2:]) if item.value == tile.value+2 and item.face == tile.face), None) 

            if testOutput:
                print(midIndex+i if midIndex is not None else None, endIndex, end="\n")

            if endIndex is not None and midIndex is not None:
                tempset = list()
                tempset.append( nonFlores.pop(endIndex+i+2) )
                tempset.append( nonFlores.pop(midIndex+i+1) )
                tempset.append( nonFlores.pop(i) )
                tempset.reverse()
                self.sets.extend(tempset)
                
            else:
                i += 1

        if testOutput:
            print("\n\tsets now ->",self.sets, "\n")
        

    def _makePairs(self, nonFlores, testOutput=False):
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
                self.pairs.append( nonFlores.pop(i) )
                
                for j in sameValues[::-1]:
                    if j != None:                        
                        self.pairs.append( nonFlores.pop(j+i) )
            else:
                i += 1
        
        if testOutput:
            print("\n\tPairs now ->",self.pairs, "\n")

        def tapon(self):
            """
            Given a 17-long (18 on a kang with regular win)
            remove a tile from hand and return it
            """
            #'''
            throw = self.hand.pop(0) # causes errors thrown from pair/set FIXME CHANGEME
            useFace = self._setFace(throw)
            
            indexOfRemove = [j if t.value == throw.value else None for j,t in enumerate(useFace)]
                
            for i in indexOfRemove:
                if i is not None:
                    useFace.pop(i)
                    break

            return throw

    def pong(self, tile, testOutput=False):
        sameValues = [j if t.value == tile.value and t.face == tile.face else None for j,t in enumerate(self.pairs)]
        
        if len(self.pairs)/2 < 4:
            if len(sameValues) - sameValues.count(None) > 1: # if sameTiles at least 2
                if len(sameValues) - sameValues.count(None) > 2: #kang
                    print("kang not implemented..")
                    raise NotImplementedError

                if testOutput:
                    print("pairs", self.pairs, "\nsameValues", sameValues)

                for i in sameValues[::-1]:
                    if i != None:
                        self.declared.append( self.pairs.pop(i) )
                self.declared.append(tile)
                
                # remove from hand
                face = self._setFace(tile)
                indexInFace = [j if t.value == tile.value else None for j,t in enumerate(face)]
                        
                for i in indexInFace[::-1]: 
                    if i != None:
                        face.pop(i)
                
                self.sortHand()
                return True

        return False

    def _sharedChao(self, tile):
        '''
        returns True if shared chao potential results in 2 sets
        call after chao and bunot
        '''
        useFace = super()._setFace(tile)
        oldFace = useFace.copy()
        oldSets = [t for t in self.sets if t.face == tile.face]
        otherSets = [t for t in self.sets if t.face != tile.face]
        useable = oldSets + [tile] + useFace

        # sort , create set, and test
        useable = sorted(useable, key=lambda tile: tile.value)

        # dangerous, reformats suit, sets, and adds the tile if applicable
        self._makeStraight(useable)

        if len(self.sets) / 3 == len(oldSets)+len(otherSets) / 3 + 1: # new set found
            # ΔCHANGEME how to set the declared if chao

            # mb just remove oldsets and call from chao

            return True

        else:
            self.sets = oldSets + otherSets
            useFace = oldFace
            return False

    def chao(self, tile):
        useFace = super()._setFace(tile)
        vals = [t.value for t in useFace]

        '''
        cases
        new tile finishes front:
            (1) 2 3

        middle
            4 (5) 6

        end
            7 8 (9)
        '''
        #midIndex = next((j for j, item in enumerate(useFace) if item.value == tile.value), None) 

        leftIndex = [i for i, j in enumerate(vals) if j == tile.value-1]
        lMostIndex = [i for i, j in enumerate(vals) if j == tile.value-2]
        rightIndex = [i for i, j in enumerate(vals) if j == tile.value+1]
        rMostIndex = [i for i, j in enumerate(vals) if j == tile.value+2]
        straight = list()

        # pop right to left (preserve indexes),

        if leftIndex: 
            if rightIndex: #chk middle
                six = useFace.pop(rightIndex.pop())
                four = useFace.pop(leftIndex.pop())

                straight.append( four )
                straight.append(tile)
                straight.append( six )

                self.declared.extend(straight)

                self.sortHand()
                return True

            elif lMostIndex: # chk end
                eight = useFace.pop(leftIndex.pop())
                seven = useFace.pop(lMostIndex.pop())

                straight.append( seven )
                straight.append( eight )
                straight.append(tile)

                self.declared.extend(straight)

                self.sortHand()
                return True

        elif rightIndex:
            if rMostIndex: # chk front
                three = useFace.pop(rMostIndex.pop())
                two = useFace.pop(rightIndex.pop())

                straight.append(tile)
                straight.append(two)
                straight.append(three)

                self.declared.extend(straight)

                self.sortHand()
                return True

        return False

    
    # def tapon(self):
    #     '''
    #     Prioritize making sets
    #     Make pairs

    #     From loose tiles:
    #         Throw what is already discarded/declared
    #             less likely to form pairs

    #         Throw what is furthest from your current cards
    #             e.g. given [4 5 6], throw 1 instead of 8

    #     Else, from loose, throw randomly

    #     '''

    #     return None

    def todas(self, testOutput=False):

        # assuming 5 sets, 1 pair
        hasPair = len(self.pairs)/2 == 1

        if not self.stick and not self.ball and not self.char:

            # assuming 5 sets, 1 pair
            if len(self.sets) / 3 == 5 and hasPair:  # 5 straights
                return True

        # joker test, assuming one
        remJokers = len(joker)

        # needs pair, len(nonFlores == odd)
        # needs straight len(nonFlores == even)

        for nonFlores in [self.ball, self.char, self.stick]:
            if nonFlores: # items exist
                usedJokers = self._jokersUsed(nonFlores, hasPair)
                if usedJokers < 1: # set not found
                    return False
                remJokers -= usedJokers

        if remJokers != 0: # all jokers sucessfully used
            return False
        else:
            return True
    
    def _jokersUsed(self, nonFlores, hasPair):
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
        while j < len(nonFlores):
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



if __name__ == "__main__":
    '''
    p = Player("dot hand ref", "dot flores ref")
    print("player",p.hand, p.flores, sep="\t\t")    
    '''

    import Distribute

    players = Distribute.initMahjong()
    #joker = modular.Tile(1, modular.TileType.BALL.value) # TESTING VV
    joker = Distribute.joker


    print("\n\nBefore sorting")
    print(" joker:", joker)
    for i, p in enumerate(players):
        if i == 0: # TESTING
            print("\nplayer",i,"\n",p)
    print()

    
    for p in players:
        p.sortHand(firstSort=True)
    print("\nAfter sorting")

    for i, p in enumerate(players):
        if i == 0: # TESTING
            print("\nplayer",i,"\n",p)
    print()


    print("\ntest dumb tapon on p0")
    for i in range(1, 10):
        print("throwing ",players[0].tapon(),end="\t\t")
        players[0].bunot(modular.Tile(i, modular.TileType.BALL.value))


    print("\nbaisc ai init...")
    baAI = BasicAI(players[3].hand, players[3].flores)
    
    
    print("\nai group test")
    baAI.sortHand(firstSort=True)
    print("sets",baAI.sets)
    print("pairs",baAI.pairs)
    
    #'''
