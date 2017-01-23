# main ThunBot file

import cfg
import socket
import time
import re
from Emotes import Emotes
import Commands

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

ThunBeast = "ThunBeast"
meThunBeast = "/me ThunBeast"
#network functions
#s = socket.socket()
#s.connect((cfg.HOST, cfg.PORT))
#s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
#s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
#s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))

s = socket.socket()

entryTime = time.time()
replyTimer = 0
guessTimer = 0
pyramidTimer = 0 #try starting at 0 for both of these
meToggle = 0

#instantiate our emote class
emotes = Emotes()

#MACROS
def chat(msg):
    s.send("PRIVMSG {} :{}\r\n".format(cfg.CHAN, msg).encode('utf-8'))
    #s.send("PRIVMSG {} :{}\r\n".format(cfg.CHAN, msg).encode("utf-8"))
    
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

emotes.Init(cfg.fileName)

#main loop
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
        
        messageTok = message.rsplit() #splits off newline characters as well

        #if re.search("ThunBeast__", message) or re.search("ThunBeast__,", message) and (time.time() - timer >= 5):
        if ((cfg.BOTNAME[0] in messageTok) or (cfg.BOTNAME[1] in messageTok)) and (time.time() - replyTimer >= cfg.REPLY_COOLDOWN):
            #s.send("PRIVMSG {} :{} ThunBeast\r\n".format(cfg.CHAN, username).encode("utf-8"))
            chat(username + " " + ThunBeast)
            replyTimer = time.time()

        #elif re.search("!pyramid", message) and (time.time() - pyramidTimer >= cfg.PYRAMID_COOLDOWN):
        elif (cfg.COMMAND_PYRAMID in messageTok) and (time.time() - pyramidTimer >= cfg.PYRAMID_COOLDOWN):
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

        #elif re.search("!guess", message):
        elif cfg.COMMAND_GUESS in messageTok and (time.time() - guessTimer >= cfg.GUESS_COOLDOWN):
            guessedEmote = messageTok[1] #need to not hard code this positioning
            
            if (emotes.findEmote(guessedEmote)):
                winningEmote = Commands.ThunGuess(guessedEmote, emotes)
#                randEmote = emotes.RandEmote()
#                if randEmote == messageTok[1]:
                if winningEmote == guessedEmote:
                    winCounter = Commands.GuessWin()
                    chat(username + ' is correct! I guessed ' + guessedEmote + ' ' + username + ' is winner #' + str(winCounter))
                else:
                    chat(username + ' is wrong :( My guess was ' + winningEmote)
            else:
                chat(messageTok[1] + ' is not a recognized emote')
            guessTimer = time.time()
        
        #elif cfg.COMMAND_THINKING in messageTok:
        #    chat(" :thinking: ")

        #MAKE SURE THIS IS AT THE END OF THE SEQUENCE   
        elif (cfg.THUNBEAST in messageTok) and (time.time() - replyTimer >= cfg.REPLY_COOLDOWN):
            if meToggle:
                chat(meThunBeast)
            else:
                chat(ThunBeast)
            meToggle ^= 1
            replyTimer = time.time()

       # elif cfg.COMMAND_TEST in messageTok:
            #chat(messageTok[1])
            #chat(emotes.findEmote(messageTok[1]))
        #    chat(emotes.randomEmote(messageTok[1]))
            
    ###TODO: AT THE END OF THE LOOP I NEED SOMEWAY TO CATCH UP  THE SOCKET, PROBABLY JUST THROW AWAY ANY MESSAGES IN BETWEEN(SINCE THE COOLDOWN WILL BE IN EFFECT ANYWAY)
    ###     RIGHT NOW IF I GET BEHIND IN MESSAGES THEN IT WILL NEVER CATCH UP, IT WILL BE ETERNALLY BEHIND. I THINK.