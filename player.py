
import modular
#import Distribute # really jus tfor joker

'''
from Distribute import joker
'''
#joker = modular.Tile(1, modular.TileType.BALL.value) 
joker = AttributeError # why does this not change, see #93 GH
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
        self.kang = list()

        self.num = Player.i
        Player.i += 1

    def __str__(self):
        return "P" + str(self.num) + "  " + str(self.hand) + "\tlen " + str(len(self.hand)) + ", "  + str(self.declared)        +''' "\nFlores:\t" + str(self.flores) + "\tlen " + str(len(self.flores)) +''' "\nJoker:\t" + str(self.jokers) + "\tlen " + str(len(self.jokers))

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

        if not self._place(tile): #it was flores
            return False

        # tile in proper face, put it in hand

        if testOutput:
            print("\nhand b4", self.hand, len(self.hand), self.declared)

        self.hand.append(tile) # 17CHANGEME REMOVEME

        if testOutput:
            print("\nhand now", self.hand, len(self.hand), self.declared)

        self.sortHand(testOutput=True if self.num == 1 and testOutput else None)
        return True

    def decideAction(self):
        raise NotImplementedError()

    def tapon(self):
        """
        Given a 17-long (18 on a kang with regular win)
        remove a tile from hand and return it
        """
        #'''
        throw = self.hand.pop(0)
        useSet = self._setFace(throw)
        
        indexOfRemove = [j if t.value == throw.value else None for j,t in enumerate(useSet)]
            
        for i in indexOfRemove:
            if i is not None:
                useSet.pop(i)
                break

        return throw

    def pong(self, tile, testOutput=False):
        return False
        #raise NotImplementedError("Please implement me")
        

    def chao(self, tile, testOutput=False):
        #raise NotImplementedError("Please implement me")
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


    def _group(self, nonFlores, testOutput=False):
        
        #'''
        if nonFlores:
            self._makeStraight(nonFlores, testOutput)
            self._makePairs(nonFlores, testOutput)
        '''

        #'''

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

    def pong(self, tile, testOutput=False):
        sameValues = [j if t.value == tile.value and t.face == tile.face else None for j,t in enumerate(self.pairs)]
        
        if len(sameValues) - sameValues.count(None) > 1: # if sameTiles at least 2

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

    def chao(self, tile):
        useSet = super()._setFace(tile)
        vals = [t.value for t in useSet]

        '''
        cases
        new tile finishes front:
            (1) 2 3

        middle
            4 (5) 6

        end
            7 8 (9)
        '''
        #midIndex = next((j for j, item in enumerate(useSet) if item.value == tile.value), None) 

        leftIndex = [i for i, j in enumerate(vals) if j == tile.value-1]
        lMostIndex = [i for i, j in enumerate(vals) if j == tile.value-2]
        rightIndex = [i for i, j in enumerate(vals) if j == tile.value+1]
        rMostIndex = [i for i, j in enumerate(vals) if j == tile.value+2]
        straight = list()

        # pop right to left (preserve indexes),

        if leftIndex: 
            if rightIndex: #chk middle
                six = useSet.pop(rightIndex.pop())
                four = useSet.pop(leftIndex.pop())

                straight.append( four )
                straight.append(tile)
                straight.append( six )

                self.declared.extend(straight)

                self.sortHand()
                return True

            elif lMostIndex: # chk end
                eight = useSet.pop(leftIndex.pop())
                seven = useSet.pop(lMostIndex.pop())

                straight.append( seven )
                straight.append( eight )
                straight.append(tile)

                self.declared.extend(straight)

                self.sortHand()
                return True

        elif rightIndex:
            if rMostIndex: # chk front
                three = useSet.pop(rMostIndex.pop())
                two = useSet.pop(rightIndex.pop())

                straight.append(tile)
                straight.append(two)
                straight.append(three)

                self.declared.extend(straight)

                self.sortHand()
                return True

        return False
        

    def decideAction(self):
        return None

    '''
    def tapon(self):

        return None
    #'''


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
