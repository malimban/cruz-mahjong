
class Player:

    def __init__(self, hand, flores):
        self.hand = hand
        self.flores = flores
        
        pairs = list()
        sets = list()

    def __str__(self):
        #format = str()

        return str(self.hand) + "\t" + str(self.flores)

    def tapon(self):
        """
        Given a 17-long (18 on a kang with regular win)
        remove a tile from hand and return it
        """
        return None
    

if __name__ == "__main__":
    '''
    from Wall import Tile
    from Wall import TileType

    print( Tile(None, TileType.FLORES ))
    
    '''
    p = Player("dot hand ref", "dot flores ref")
    print("player",p.hand, p.flores, sep="\t\t")


    #'''
