'''Containts methods for the commands compatible with ThunBot'''
from Emotes import Emotes
import cfg
import random
import math
import DBInterface

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
        if emoteRoll  == emote: #if we have grabbed the winning emote
            #TODO: INCREMENT TOTAL WIN COUNTER
            #TODO: IF USER EXISTS IN GUESSWINS, INCREMENT COUNTER
            #       OTHERWISE ADD A NEW ENTRY
            return emoteRoll #then the user wins so we return the input emote
        #else: #we want to return a random emote
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

def GuessWins(username):
    numWins = DBInterface.GuessWinsQuery(username)
    return numWins

def TotalGuessWins():
    return DBInterface.TotalGuessWinsQuery()

def TestTotalGuessWins():
    DBInterface.UpdateTotalWins()
    return TotalGuessWins()

def TestUpdateUserGuessWins(username):
    DBInterface.UpdateUserWins(username)
    return GuessWins(username)