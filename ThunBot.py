# main ThunBot file

import cfg
import socket
import time
import re
from Emotes import Emotes
import Commands
from EmoteManager import EmoteManager

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

ThunBeast = "ThunBeast"
meThunBeast = "/me ThunBeast"
ignoredUser = "" # just for initialization

s = socket.socket()

entryTime = time.time()
replyTimer = 0
guessTimer = 0
pyramidTimer = 0 # try starting at 0 for both of these
meToggle = 0
ignoreTimer = 0
isUserIgnored = False

# instantiate our emote class
emotes = Emotes()
emoteManager = EmoteManager()

# MACROS
def chat(msg):
    s.send("PRIVMSG {} :{}\r\n".format(cfg.CHAN, msg).encode('utf-8'))
    # s.send("PRIVMSG {} :{}\r\n".format(cfg.CHAN, msg).encode("utf-8"))
    
def ban(user):
    chat(".ban {}".format(user))

def timeout(user, secs = 1):
    chat(".timeout {}".format(user, secs))

def reconnect():
    s.connect((cfg.HOST, cfg.PORT))
    s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
    s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))


s.connect((cfg.HOST, cfg.PORT))
s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))

chat(ThunBeast + " /")

Commands.UpdateAllEmotes(emoteManager, cfg.channel)  # make sure we have the latest emotes
emotes.Init(cfg.channel)

# main loop
while True:
    try:
        response = s.recv(1024).decode("utf-8")
    except:
        response = ""
        continue

    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        try:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)
            print(username + ": " + message)
        except:
            message = ""
            print(username + ":")
            continue
        
        messageTok = message.rsplit() # splits off newline characters as well

        if cfg.COMMAND_GUESS == messageTok[0] and (time.time() - guessTimer >= cfg.GUESS_COOLDOWN):
            try:
                guessedEmote = messageTok[1]  # need to not hard code this positioning
            except:
                guessedEmote = ""
                continue

            if emotes.findEmote(guessedEmote):
                winningEmote = Commands.ThunGuess(username, guessedEmote, emotes)
                if winningEmote == guessedEmote:
                    chat(username + ' is correct! I guessed ' + guessedEmote)
                else:
                    chat(username + ' is wrong. My guess was ' + winningEmote)
                guessTimer = time.time()
            else:
                chat(messageTok[1] + ' is not a recognized emote')
            continue

        elif ((cfg.BOTNAME[0] in messageTok) or (cfg.BOTNAME[1] in messageTok) or (cfg.BOTNAME[2] in messageTok) or (cfg.BOTNAME[3] in messageTok)) and (time.time() - replyTimer >= cfg.REPLY_COOLDOWN):
            chat(username + " " + ThunBeast)
            replyTimer = time.time()

        elif cfg.COMMAND_GUESSWINS == messageTok[0]:
            totalGuessWins = Commands.TotalGuessWins()
            chat('There has been %i correct guesses!' %(totalGuessWins))

        elif cfg.COMMAND_REGISTER == messageTok[0] and username == 'bigsmcgee':
            emote = messageTok[1]
            Commands.RegisterUniversalEmote(emote)
            emotes.RefreshEmoteList(cfg.channel)
            chat('Added %s to the emote list'%(emote))

        elif cfg.COMMAND_UNREGISTER == messageTok[0] and username == 'bigsmcgee':
            emote = messageTok[1]
            Commands.UnregisterUniversalEmote(emote)
            emotes.RefreshEmoteList(cfg.channel)
            chat('Removed %s from the emote list'%(emote))

        elif cfg.COMMAND_REGISTERUNIQUE == messageTok[0] and username == 'bigsmcgee':
            emote = messageTok[1]
            Commands.RegisterChannelEmote(cfg.channel, emote)
            emotes.RefreshEmoteList(cfg.channel)
            chat('Added %s to the emote list for %ss channel'%(emote, cfg.channel))

        elif cfg.COMMAND_UNREGISTERUNIQUE== messageTok[0] and username == 'bigsmcgee':
            emote = messageTok[1]
            Commands.UnregisterChannelEmote(cfg.channel, emote)
            emotes.RefreshEmoteList(cfg.channel)
            chat('Removed %s from the emote list for %ss channel'%(emote, cfg.channel))

        elif cfg.COMMAND_MYWINS == messageTok[0]:
            mywins = Commands.GuessWins(username)
            chat("%s has guessed correctly %i times"%(username, mywins))

        elif cfg.COMMAND_PYRAMID == messageTok[0] and time.time() - pyramidTimer >= cfg.PYRAMID_COOLDOWN:
            pyramidTimer = time.time()
            chat(ThunBeast)
            time.sleep(1.25)
            chat(ThunBeast + " " + ThunBeast)
            time.sleep(1.25)
            chat(ThunBeast + " " + ThunBeast + " " + ThunBeast)
            time.sleep(1.25)
            chat(ThunBeast + " " + ThunBeast)
            time.sleep(1.25)
            chat(ThunBeast)
            pyramidTimer = time.time()

        elif cfg.COMMAND_REFRESH == messageTok[0]:
            Commands.UpdateAllEmotes(emoteManager, cfg.channel)
            emotes.RefreshEmoteList(cfg.channel)

        #MAKE SURE THIS IS AT THE END OF THE SEQUENCE   
        elif cfg.THUNBEAST in messageTok and time.time() - replyTimer >= cfg.REPLY_COOLDOWN:
            if meToggle:
                chat(meThunBeast)
            else:
                chat(ThunBeast)
            meToggle ^= 1
            replyTimer = time.time()


    ### TODO: AT THE END OF THE LOOP I NEED SOMEWAY TO CATCH UP  THE SOCKET, PROBABLY JUST THROW AWAY ANY MESSAGES IN BETWEEN(SINCE THE COOLDOWN WILL BE IN EFFECT ANYWAY)
    ###     RIGHT NOW IF I GET BEHIND IN MESSAGES THEN IT WILL NEVER CATCH UP, IT WILL BE ETERNALLY BEHIND. I THINK.
