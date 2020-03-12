
import Wall
import Distribute

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
        return str(self.hand) + "\nFlores:\t" + str(self.flores) + "\nJoker:\t" + str(self.jokers)

    def _place(self, tile):
        try:
            #'''
            if tile.face == Distribute.joker.face and tile.value is Distribute.joker.value:
                self.jokers.append(tile)
            elif tile.face == Wall.TileType.BALL.value:
                self.ball.append(tile)
            elif tile.face == Wall.TileType.STICK.value:
                self.stick.append(tile)
            elif tile.face == Wall.TileType.CHARACTER.value:
                self.char.append(tile)
            ''' #https://stackoverflow.com/questions/45459026/python-mix-in-enumerations-as-dictionary-key-how-the-type-is-converted
            if tile.face == Distribute.joker.face and tile.value == Distribute.joker.value:
                return self.jokers.append(tile)
            return {
                Wall.TileType.BALL.value:       #self.ball.append(tile)
                print("this should be",Wall.TileType.BALL.value, "\t", tile.face, tile.face is Wall.TileType.BALL.value),
                Wall.TileType.STICK.value:      self.stick.append(tile),
                Wall.TileType.CHARACTER.value:  self.char.append(tile)
            }[tile.face]
            #'''
        except:
            print("Flores found in hand @", tile.face, tile.value)
            raise Exception

    def sortHand(self):
        for tile in self.hand:
            self._place(tile)

        self.ball = sorted(self.ball, key=lambda tile: tile.value)
        self.stick = sorted(self.stick, key=lambda tile: tile.value)
        self.char = sorted(self.char, key=lambda tile: tile.value)
        sortedHand = self.ball + self.stick + self.char + self.jokers

        if len(self.hand) == len(sortedHand):
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
        if tile.face is Wall.TileType.FLORES.value:
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
        raise NotImplementedError("Please implement me")
    
class BasicAI(Player):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.pairs = list()
        self.sets = list()
        self.almostSets = list()
        self.rem = list()
        self.declared = list()

    def sortHand(self):
        super(self.__class__, self).sortHand()
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

        '''
        for i, tile in enumerate(nonFlores):
            midIndex = next((j for j, item in enumerate(nonFlores) if item.value == tile.value), None) 
            endIndex = next((j for j, item in enumerate(nonFlores) if item.value == tile.value), None) 
            if endIndex is None:
                self.pairs.append( nonFlores.pop(i) )
                self.pairs.append( nonFlores.pop(midIndex-1) )
            else: # triple or quad possible
                quadIndex = next((j for j, item in enumerate(nonFlores) if item.value == tile.value), None) 
                if quadIndex is None: # triple                     
                    self.pairs.append( nonFlores.pop(i) )
                    self.pairs.append( nonFlores.pop(midIndex-1) )
                    self.pairs.append( nonFlores.pop(endIndex-2) )
                else:
                    self.pairs.append( nonFlores.pop(i) )
                    self.pairs.append( nonFlores.pop(midIndex-1) )
                    self.pairs.append( nonFlores.pop(endIndex-2) )
                    self.pairs.append( nonFlores.pop(quadIndex-3) )
        #'''

    

    def decideAction(self):
        return None

    def tapon(self):

        return None

if __name__ == "__main__":
    '''
    p = Player("dot hand ref", "dot flores ref")
    print("player",p.hand, p.flores, sep="\t\t")    
    '''
    
    players = Distribute.initMahjong()
    Distribute.joker = Wall.Tile(1, Wall.TileType.BALL.value) # TESTING
    print("distribute joker", Distribute.joker)

    print("Before sorting")
    for i, p in enumerate(players):
        if i == 0: # TESTING
            print("\nplayer",i,"\n",p)
    print()

    
    for p in players:
        p.sortHand()
    print("After sorting\n")

    for i, p in enumerate(players):
        print("\nplayer",i,"\n",p)
    print()

    print("baisc ai init...")
    baAI = BasicAI(players[3].hand, players[3].flores)
    
    
    print("ai group test")
    baAI.sortHand()
    print("sets",baAI.sets)
    print("pairs",baAI.pairs)
    
    #'''
