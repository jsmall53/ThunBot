'''Containts methods for the commands compatible with ThunBot'''
from Emotes import Emotes
import cfg
import random
import math

ignoredUser = ""
#random.seed()
#first is the guess command, since this is the most popular it seems
def ThunGuess(emote, emotesRef):
    '''Takes in an emote as a string and returns an emote string'''
    random.seed()
    #diceRollReference = random.randrange(cfg.GUESS_WINRATE)
    #diceRollReference = math.floor(cfg.GUESS_WINRATE/2)
    diceRoll = random.randrange(1, cfg.GUESS_WINRATE)
    for i in range(1, cfg.GUESS_WINRATE):
        emoteRoll = emotesRef.RandEmote()
        if emoteRoll  == emote:
            return emoteRoll #then the user wins so we return the input emote
        #else: #we want to return a random emote(still has a chance to win
    return emoteRoll

def GuessWin():
    '''Returns the numbers of guess wins that have occured'''
    winFile = open(cfg.GUESSFILE, 'r+')
    for i in winFile:
        winCounter = i
    winCounter = int(winCounter)
    winCounter += 1
    winFile.seek(0)
    winFile.write(str(winCounter))
    winFile.truncate()
    winFile.close()
    return winCounter

def Ignore(user):
    '''Returns something about ignoring a user'''
    ignoredUser = user
    return ("/ignore " + ignoredUser)

def Unignore():
    '''Ungnores the previously ignored user'''
    return ("/unignore " + ignoredUser)
    