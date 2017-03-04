# cfg.py
### CONFIG CLASS FOR THUNBOT ###

HOST = "irc.twitch.tv"  #twitch IRC server
PORT = 6667
NICK = "thunbot_" #name of the bot
PASS = "oauth:zq951d4x3w1vdu9mzf8hc3a730ily1"#"oauth:xxi5yk7t1ul1q3wptdklgvrrdf4qls" #password to bot account
CHAN = "#etup" #the channel you want to join
#RATE =  (20/30)         #chat spam limit

THUNBEAST = "ThunBeast"
BOTNAME = ["ThunBot_", "ThunBot_,"] #make sure both version of this exist since twitch autocomplete puts a comma at the end of the name

#EMOTESLIST FILEPATH
FILEPATH = "D:\\git\\ThunBot\\ThunBot\\ThunBot\\"
EMOTE_LIST = r"EmoteList.txt"
fileName = FILEPATH+EMOTE_LIST

#GUESS WINS FILEPATH
GUESSFILE = "D:\git\ThunBot\ThunBot\ThunBot\GuessWins.txt"

#COOLDOWNS
REPLY_COOLDOWN = 5      #IN SECONDS
PYRAMID_COOLDOWN = 60   #IN SECONDS
GUESS_COOLDOWN = 15
IGNORE_COOLDOWN = 30 #SECONDS
MYWINS_COOLDOWN = 5
TOTALWINS_COOLDOWN = 5


#command strings
COMMAND_PYRAMID = "!pyramid"
COMMAND_GUESS   = "!guess"
COMMAND_TEST    = "!test"
COMMAND_THINKING = "!hmmm"  #requested by fake bade
#COMMAND_IGNORE = "!ignore"
COMMAND_GUESSWINS = "!totalwins"
#COMMAND_TESTWINS = "!testwins"
#COMMAND_TESTUSERWINS = "!testuserwins"
COMMAND_MYWINS = "!wins"

#MISC CONSTANTS
GUESS_WINRATE = 5 #represents the max number of possible "retries" for the guess command