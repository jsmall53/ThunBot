# cfg.py
### CONFIG CLASS FOR THUNBOT ###

##TODO: Extract some configs out to a file that it loaded in at runtime. mainly for the channel so that I dont have to recompile everytime I want to enter a different channel

channel = "etup"        #must keep this string separate from CHAN since this is also used for SQL
HOST = "irc.twitch.tv"  #twitch IRC server
PORT = 6667
NICK = "thunbot_" #name of the bot
PASS = "oauth:zq951d4x3w1vdu9mzf8hc3a730ily1"#"oauth:xxi5yk7t1ul1q3wptdklgvrrdf4qls" #password to bot account
CHAN = "#"+channel #the channel you want to join

THUNBEAST = "ThunBeast"
BOTNAME = ["ThunBot_", "ThunBot_,", "@ThunBot_,", "@ThunBot_"] #make sure both version of this exist since twitch autocomplete puts a comma at the end of the name

#EMOTESLIST FILEPATH
#FILEPATH = "D:\\git\\ThunBot\\ThunBot\\ThunBot\\"
#EMOTE_LIST = r"EmoteList.txt"
#fileName = FILEPATH+EMOTE_LIST

#GUESS WINS FILEPATH
GUESSFILE = "D:\git\ThunBot\ThunBot\ThunBot\GuessWins.txt"

#COOLDOWNS
REPLY_COOLDOWN = 5      # IN SECONDS
PYRAMID_COOLDOWN = 60   # IN SECONDS
GUESS_COOLDOWN = 15
IGNORE_COOLDOWN = 30 # SECONDS
MYWINS_COOLDOWN = 5
TOTALWINS_COOLDOWN = 5


#command strings
COMMAND_PYRAMID = "!pyramid"
COMMAND_GUESS   = "!guess"
COMMAND_TEST    = "!test"
COMMAND_THINKING = "!hmmm"  # requested by fake bade
COMMAND_GUESSWINS = "!totalwins"
COMMAND_MYWINS = '!wins'
COMMAND_REGISTER = "!reg"
COMMAND_UNREGISTER = "!unreg"
COMMAND_REGISTERUNIQUE = "!channelreg"
COMMAND_UNREGISTERUNIQUE = "!channelunreg"
COMMAND_REFRESH = "!refresh"

#MISC CONSTANTS
GUESS_WINRATE = 3 #represents the max number of possible "retries" for the guess command

GLOBAL_EMOTE_URL = "https://twitchemotes.com/api_cache/v2/global.json"
BTTV_EMOTE_URL = "https://api.betterttv.net/2/emotes"
CHAN_EMOTE_URL = "https://api.betterttv.net/2/channels/"  # to use this, make sure you append the channel name to the end of the string