#This class will store emotes as well has contain methods for choosing and comparing emotes

import cfg
import random
import DBInterface

class Emotes:
    '''This class stores emotes usable through twitch.tv chat interface'''
#first we need to open the file containing the emotes
#its in a .txt file and each emotes is separated by a newline

    random.seed() #default seeds from system time
    emoteList = [] #create a list that we can dynamically allocate based on the number of emotes in the file
    #file = open(cfg.fileName)

    def Init(self, fileName):
        '''Sets up the list of emotes given in the file'''
        file = open(fileName, 'r')
        for line in file:
            self.emoteList.append(line.rstrip())

    def findEmote(self, emoteString):
        '''returns the emote if it is located in the file'''
        for emote in self.emoteList:
            if emote == emoteString:
                return True
        return False

    def RandEmote(self):
        '''returns a random emote from the emoteList'''
        length = len(self.emoteList)
        index = random.randrange(length)
        return self.emoteList[index]
        
    def GetEmoteList():
        '''Reads the emote list into memory'''
        