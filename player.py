
import Wall
import Distribute

class Player:

    def __init__(self, hand, flores, money=1000):
        self.hand = hand
        self.flores = flores
        self.money = money
        
        self.ball = list()
        self.stick = list()
        self.char = list()
        self.jokers = list()
        
        self.pairs = list()
        self.sets = list()
        self.almostSets = list()
        self.declared = list()

    def __str__(self):
        return str(self.hand) + "\nFlores:\t" + str(self.flores)

    def sortHand(self):
        for tile in self.hand:
            if tile.face == Distribute.joker:
                self.jokers.append(tile)
            elif tile.face == Wall.TileType.BALL.value:
                self.ball.append(tile)
            elif tile.face == Wall.TileType.STICK.value:
                self.stick.append(tile)
            elif tile.face == Wall.TileType.CHARACTER.value:
                self.char.append(tile)
            else:
                print("Flores found in hand @", tile.face, tile.value)
                return Exception

        self.ball = sorted(self.ball, key=lambda tile: tile.value)
        self.stick = sorted(self.stick, key=lambda tile: tile.value)
        self.char = sorted(self.char, key=lambda tile: tile.value)
        sortedHand = self.ball + self.stick + self.char + self.jokers

        if len(self.hand) == len(sortedHand):
            self.hand = sortedHand
        else:
            print("Hand != sortedHand")
            print("len old hand",len(self.hand),self.hand)
            print("len new hand",len(sortedHand),sortedHand)
            raise Exception
        return True

    def tapon(self):
        """
        Given a 17-long (18 on a kang with regular win)
        remove a tile from hand and return it
        """
        raise NotImplementedError("Please implement me")
    
class BasicAI(Player):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        print("basicAI init!")

    def tapon(self):

        return None

if __name__ == "__main__":
    '''
    p = Player("dot hand ref", "dot flores ref")
    print("player",p.hand, p.flores, sep="\t\t")    
    '''
    import Distribute
    
    players = Distribute.initMahjong()

    print("Before sorting")
    for i, p in enumerate(players):
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
    baAI.sortHand()
    print(baAI)
    print(baAI.ball)

    print("\n\npop test", baAI.ball.pop(0))
    print(baAI)
    print(baAI.ball)

    #'''
