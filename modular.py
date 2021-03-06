from enum import Enum

class TileType(Enum):
    '''
        each is four
        ball, bamboo, char --> 1-9

        flores: 8*4
        
        winds
            east
            south
            west
            north

        dragons
            red
            green
            white

        unique
            flower
            season

        blank tiles
    '''

    __order__ = 'BALL STICK CHARACTER FLORES'
    
    BALL = "Ball"
    STICK = "Stick"
    CHARACTER = "Character"

    FLORES = "Flores" #'winds', 'dragons', 'blanks']


class FloresFace(Enum):
    __order__ = 'EAST SOUTH WEST NORTH RED GREEN WHITE FLOWER SEASON BLANK'

    EAST = "East"
    SOUTH = "South"
    WEST = "West"
    NORTH = "North"

    RED = "Red"
    GREEN = "Green"
    WHITE = "White"

    FLOWER = "Flower"
    SEASON = "Season"

    BLANK = "Blank"

class Tile:

    def __init__(self, value, face):
        self.value = value
        self.face = face

    def __str__(self):
        return str(self.value) + " " + str(self.face)

    def __repr__(self):
        #'''
        return str(self)
        '''
        return "\t" + str(self.value) + " " + str(self.face)
        #'''

    # for custom dictionary key
    def __hash__(self):
        return hash((self.value, self.face))

    def __eq__(self, other):
        return (self.value, self.face) == (other.value, other.face)

    def __ne__(self, other):
        return not(self == other)

    