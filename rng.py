
from random import randint 
import random

import qsharp
from Qrng import GenRandQbit 

quantum = False

def rollDice(diceCount=2, testOutput=False):
    if quantum:
        DMIN = 1
        DMAX = 6

        dice = list()
        while len(dice) < diceCount:
            qNum = genQNum(DMAX)
            if qNum >= DMIN:
                dice.append(qNum)

        if testOutput:
            print("\nrolld: ",end='')
            for d in dice:
                print(d, end=' ')
            print()

        return dice
    else:
        dice = _rollPseudo(diceCount)

    return dice

def shuffleWalls(walls = list()):
    if quantum:
        for i in range(len(walls)-1, 0, -1): 
            # Pick a random index from 0 to i  
            j = genQNum(i + 1)  
            
            # Swap arr[i] with the element at random index  
            walls[i], walls[j] = walls[j], walls[i]  

    else:
        random.shuffle(walls) 

    return walls    

def genQNum(max = 148, testOutput=False): 
    '''
    Takes maximum integer, returns random integer
    '''
    output = max + 1 # +1 to iterate

    while output > max:
        bits = [] 

        for i in range(0, max.bit_length()): 
            bits.append(GenRandQbit.simulate()) 

        if testOutput: print("bitstr",bits)

        output = int("".join(str(x) for x in bits), 2) 
    
    return output
        

def _rollPseudo(diceCount=2, testOutput=False): 
    DMIN = 1
    DMAX = 6

    dice = list()
    for i in range(diceCount):
        dice.append(randint(DMIN, DMAX))
        i = i

    if testOutput:
        print("\nrolld: ",end='')
        for d in dice:
            print(d, end=' ')
        print()

    return dice

if __name__ == "__main__":
    quantum = True
    print(rollDice())