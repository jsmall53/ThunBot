'''Containts methods for the commands compatible with ThunBot'''
from Emotes import Emotes
import cfg
import random
import DBInterface
import EmoteManager

random.seed()

#  first is the guess command, since this is the most popular it seems


def ThunGuess(username, emote, emotesRef):
    '''Takes in an emote as a string and returns an emote string'''
    for i in range(1, cfg.GUESS_WINRATE):
        emoteRoll = emotesRef.RandEmote()
        if emoteRoll  == emote:  # if we have grabbed the winning emote
            DBInterface.UpdateTotalWins()
            DBInterface.UpdateUserWins(username)
            return emoteRoll  # then the user wins so we return the input emote
    return emoteRoll

def GuessWin():
    '''Returns the numbers of guess wins that have occurred'''
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


def RegisterUniversalEmote(emote):
    DBInterface.RegisterUniversalEmote(emote)


def UnregisterUniversalEmote(emote):
    DBInterface.UnregisterUniversalEmote(emote)


def RegisterChannelEmote(channel, emote):
    DBInterface.RegisterChannelEmote(channel, emote)


def UnregisterChannelEmote(channel, emote):
    DBInterface.UnregisterChannelEmote(channel, emote)

def UpdateGlobalEmotes(managerRef):
    managerRef.ManageGlobalEmotes()

def UpdateBTTVEmotes(managerRef):
    managerRef.ManageBTTVEmotes()

def UpdateChannelEmotes(managerRef, channel):
    managerRef.ManageChannelEmotes(channel)

def UpdateAllEmotes(managerRef, channel):
    '''Updates the Database with emotes from the available API's'''
    UpdateGlobalEmotes(managerRef)
    UpdateBTTVEmotes(managerRef)
    UpdateChannelEmotes(managerRef, channel)
