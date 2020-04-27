
import modular
#import Distribute # really jus tfor joker

'''
from Distribute import joker
'''
joker = AttributeError # why does this not change, see #93 GH
if __name__ == "__main__":
    joker = modular.Tile(1, modular.TileType.BALL.value) 
#'''
discardsDict = dict()
declareds = dict()


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
        if len(sortedHand) + len(self.declared) == 17:
            self.hand = sortedHand
        elif firstSort and len(sortedHand)+len(self.declared) == 16:
            self.hand = sortedHand
        else:
            return
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
            try:
                throwIndex = int(input("Throw what?\n> "))
                if throwIndex < len(self.hand):
                    throw = self.hand[throwIndex]
                    break
            except:
                continue
        
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

            while True:
                print(self.hand)
                choice = input("Pong " + str(tile) + "?\n(y)es or (n)o\n> ")
                if choice == "y":
                    tempSet = list()
                    for i in sameValues[::-1]:
                        if i != None:
                            tempSet.append( tface.pop(i) )

                    if len(tempSet) < 3:
                        tempSet.append(tile)
                    else:
                        tface.append(tile)
                    
                    self.declared.extend(tempSet)

                    self.sortHand()
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
                try:
                    chao1 = int(input("First tile index: "))
                    chao2 = int(input("Second tile index: "))
                except:
                    continue

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

                    self.sortHand()
                    return True
                
                # reset loop
                if input("Not a straight. (q)uit chao?\n> ") == "q":
                    break

        return False
        
    def todas(self):
        import todas
        if todas.todas(self.hand, joker):
            if input("State you've won?\n(y)es/(n)o\n> ") == "y":
                return True
        return False

    
class BasicAI(Player):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.pairs = list()
        self.sets = list()
        #self.almostSets = list()
        #self.rem = list()

    def sortHand(self, firstSort=False, midFix=False, testOutput=False):
        if firstSort:
            for tile in self.hand:
                self._place(tile)
            if testOutput:
                print("\nfirst",end="")
        else:
            #ΔCHANGEME chk for seven pairs first
            self._resetPairs()

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

        #if len(self.hand) == len(sortedHand) or len(self.hand)+1 == len(sortedHand):
        if len(sortedHand) + len(self.declared) == 17: # 17CHANGEME REMOVEME
            self.hand = sortedHand
        elif (firstSort or midFix) and len(sortedHand) + len(self.declared) == 16:
            self.hand = sortedHand
        else:
            return
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

    def _resetPairs(self):
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

    def randTapon(self):
        throw = self.hand.pop(0)
        useFace = self._setFace(throw)
            
        indexOfRemove = [j if t.value == throw.value else None for j,t in enumerate(useFace)]
            
        for i in indexOfRemove:
            if i is not None:
                useFace.pop(i)
                break

        return throw

    def tapon(self, ignore=list(), mustThrow=False):
        """
        Given a 17-long (18 on a kang with regular win)
        remove a tile from hand and return it
        """
        #'''
        if not ignore:
            nonFlores = self.ball if len(self.ball) < len(self.char) and len(self.ball) > 0 else self.char
            nonFlores = self.stick if len(self.stick) < len(nonFlores) and len(self.stick) > 0 else nonFlores
        else:
            if len(ignore) == 3:
                return self.randTapon()
                
            nonFlores = self.ball
            if self.ball in ignore:
                nonFlores = self.char
            if self.char in ignore:
                nonFlores = self.stick
        

        if nonFlores: 
            throw = self._difference(nonFlores, mustThrow=mustThrow)
            if isinstance(throw, modular.Tile): # legal tile
                return throw
            else:
                ignore.append(nonFlores)
                throw = self.tapon(ignore=ignore)

        else:
            try:
                print("break set")
                # break set
                remPairs = dict()
                for t in self.pairs:
                    remPairs[t] = remPairs.get(t, 4) - 1
                    
                for p in remPairs:
                    if remPairs[p] < 2: # ΔREVIEWME
                        remPairs[p] += 4
                    
                for p in remPairs:
                    remPairs[p] -= (declareds.get(p,0) + discardsDict.get(p,0))
                
                minKey = min(remPairs, key=remPairs.get)
                self.pairs.remove(minKey)
                self._resetPairs()
                
                return minKey
            except:
                return self.randTapon()



    def _difference(self, nonFlores, mustThrow):
        """
        Takes a nonFlores and returns the least necessary item
        """

        if len(nonFlores) == 1:
            if discardsDict.get(nonFlores[0],0) + declareds.get(nonFlores[0],0) > 1:
                return nonFlores.pop()
            elif mustThrow:
                return nonFlores.pop()
            else:
                return None


        distanceFromNeighbor = list()

        i=0
        past2 = list()
        while i < len(nonFlores):
            if len(past2) < 2:
                if past2:
                    distanceFromNeighbor.append(nonFlores[i].value - past2[0].value)
                past2.append(nonFlores[i])
            else:
                '''
                1
                1   2   4   
                        ^useface
                '''
                left = past2[1].value - past2[0].value
                right = nonFlores[i].value - past2[1].value
                distanceFromNeighbor.append( left if left < right else right )

                if i == len(nonFlores) - 1:
                    distanceFromNeighbor.append(right)

            i += 1

        '''
                3
        1   2   5   8   9
                ^ throw

        
        1   1   2      1   1
        1   2   4      8   9
        ^throw
        '''

        if max(distanceFromNeighbor) > 2:
            index = distanceFromNeighbor.index(max(distanceFromNeighbor))
            return nonFlores.pop(index)
        else:
            if not mustThrow:
                return None
            else: # throw max
                usedTiles = list()
                for t in nonFlores:
                    usedTiles.append( discardsDict.get(t,0) + declareds.get(t,0) + 1)

                index = usedTiles.index(max(usedTiles))
                return nonFlores.pop(index)



    def pong(self, tile, testOutput=False):
        sameValues = [j if t.value == tile.value and t.face == tile.face else None for j,t in enumerate(self.pairs)]
        
        if len(self.pairs)/2 < 4:
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
                
                self.sortHand(midFix=True)
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

    def todas(self):
        import todas
        if todas.todas(self.hand, joker):
            return True



if __name__ == "__main__":

    import Distribute

    players = Distribute.initMahjong()
    joker = Distribute.joker

    from modular import Tile
    players[0].hand = [Tile(4, "Ball"), Tile(8, "Ball"), Tile(5, "Stick"), Tile(1, "Character"), Tile(3, "Character"), Tile(5, "Character"), Tile(8, "Character"), Tile(8, "Character"), Tile(2, "Stick"), Tile(2, "Stick"), Tile(6, "Ball"), Tile(7, "Ball"), Tile(8, "Ball"), Tile(7, "Stick"), Tile(8, "Stick"), Tile(9, "Stick")]
    players[0].bunot(Tile(4, "Character"))
    '''
    import Distribute

    players = Distribute.initMahjong()

    joker = Distribute.joker
    print(joker)

    #todas test
    print(players[0])
    print(players[0].todas())
    '''