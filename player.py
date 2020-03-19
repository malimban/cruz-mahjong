
import modular
#import Distribute # really jus tfor joker

joker = EnvironmentError
joker = modular.Tile(1, modular.TileType.BALL.value) # TESTING VV

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

        self.num = Player.i
        Player.i += 1

    def __str__(self):
        return str(self.hand) + "\tlen " + str(len(self.hand)) + "\nFlores:\t" + str(self.flores) + "\tlen " + str(len(self.flores)) + "\nJoker:\t" + str(self.jokers) + "\tlen " + str(len(self.jokers))

    def _place(self, tile):
        global joker
        print("joker in class::", joker)

        if tile.value == modular.TileType.FLORES.value:
            self.flores.append(tile)
            return False
        # joker not determined... error
        elif tile.face == joker.face and tile.value is joker.value:
            self.jokers.append(tile)
        elif tile.face == modular.TileType.BALL.value:
            self.ball.append(tile)
        elif tile.face == modular.TileType.STICK.value:
            self.stick.append(tile)
        elif tile.face == modular.TileType.CHARACTER.value:
            self.char.append(tile)
        else:
            print("\nnot placed..?", tile)
            raise Exception
        return True

    def sortHand(self, firstSort=False):
        if firstSort:
            for tile in self.hand:
                self._place(tile)

        print("\nfirst",self.ball, self.stick, self.char, self.jokers, sep="\n\t")

        self.ball = sorted(self.ball, key=lambda tile: tile.value)
        self.stick = sorted(self.stick, key=lambda tile: tile.value)
        self.char = sorted(self.char, key=lambda tile: tile.value)
        sortedHand = self.ball + self.stick + self.char + self.jokers

        if len(self.hand) == len(sortedHand) or len(self.hand) == len(sortedHand)-1:
            self.hand = sortedHand
        else:
            print("Hand != sortedHand on p",self.num)
            print("len old hand",len(self.hand),self.hand)
            print("len new hand",len(sortedHand),sortedHand)
            print("from",self.ball, self.stick, self.char, self.jokers, sep="\n\t")
            raise Exception
        return True

    def bunot(self, tile):
        """
        Returns True on a non-flores bunot
        """
        if tile.face is modular.TileType.FLORES.value:
            self.flores.append(tile)
            return False
        
        self._place(tile)
        self.sortHand()
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

        if throw.face == modular.TileType.BALL.value:
            indexOfRemove = [j if t.value == throw.value else None for j,t in enumerate(self.ball)]
            
            for i in indexOfRemove:
                if i is not None:
                    self.ball.pop(i)
                    break

        elif throw.face == modular.TileType.STICK.value:
            indexOfRemove = [j if t.value == throw.value else None for j,t in enumerate(self.stick)]
            
            for i in indexOfRemove:
                if i is not None:
                    self.stick.pop(i)
                    break

        elif throw.face == modular.TileType.CHARACTER.value:
            indexOfRemove = [j if t.value == throw.value else None for j,t in enumerate(self.char)]
            for i in indexOfRemove:
                if i is not None:
                    self.char.pop(i)
                    break

        return throw
        '''
        balllen = len(self.ball)
        sticklen = len(self.stick)
        charlen = len(self.char)

        if balllen > 0 and balllen < sticklen and balllen < charlen:
            return self.ball.pop()
        elif sticklen > 0 and sticklen < balllen and sticklen < charlen:
            return self.stick.pop()
        else:
            return self.char.pop()
        '''

        #raise NotImplementedError("Please implement me")

    
class BasicAI(Player):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.pairs = list()
        self.sets = list()
        self.almostSets = list()
        self.rem = list()
        self.declared = list()

    def sortHand(self, firstSort=False):
        super(self.__class__, self).sortHand(firstSort)
        self._group(self.ball)
        self._group(self.char)
        self._group(self.stick)

    def _group(self, nonFlores, testOutput=False):
        
        #'''
        if nonFlores:
            self._makeStraight(nonFlores, testOutput)
            self._makePairs(nonFlores, testOutput)
        '''

        #'''

    def _makeStraight(self, nonFlores, testOutput=False):    
        if testOutput:
            print("\ncurent on straight",nonFlores)

        i=0
        while i < len(nonFlores):
            tile = nonFlores[i]
            
            if testOutput:
                print("@",tile,end="\t\t")

            midIndex = next((j for j, item in enumerate(nonFlores[i+1:]) if item.value == tile.value+1), None)
            endIndex = next((j for j, item in enumerate(nonFlores[i+2:]) if item.value == tile.value+2), None) 

            if testOutput:
                print(midIndex+i, endIndex, end="\n")

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
            print("\n\t",self.sets, "\n")
           

    def _makePairs(self, nonFlores, testOutput=False):
        #'''
        if testOutput:
            print("\nPairs",nonFlores)
        #for i, tile in enumerate(nonFlores):
        i=0
        #for tile in iter(nonFlores):
        while i < len(nonFlores):
            tile = nonFlores[i]
            if testOutput:
                print("@",tile,end="\t\t")
            sameValues = [j if t.value == tile.value else None for j,t in enumerate(nonFlores[i+1:])]

            if any(x != None for x in sameValues):
                self.pairs.append( nonFlores.pop(i) )
                
                for j in sameValues[::-1]:
                    if j != None:                        
                        self.pairs.append( nonFlores.pop(j+i) )
            else:
                i += 1
        
        if testOutput:
            print("\n\t",self.pairs, "\n")
    

    def decideAction(self):
        return None

    def tapon(self):

        return None



if __name__ == "__main__":
    '''
    p = Player("dot hand ref", "dot flores ref")
    print("player",p.hand, p.flores, sep="\t\t")    
    '''

    import Distribute

    players = Distribute.initMahjong()
    #joker = modular.Tile(1, modular.TileType.BALL.value) # TESTING VV
    Distribute.joker = joker
    print("\n\n joker:", joker)


    print("\n\nBefore sorting")
    print("\n\n joker:", joker)
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
