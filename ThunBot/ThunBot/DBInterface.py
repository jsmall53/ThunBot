'''Handles SQL interfacing'''
#NOTES:::   don't want to store people with 0 wins, only add to DB if they ahve at least 1 win.
#           this means that if the guess is a winner, I should increment the users NumWins by 1 if they already exist, and create a new entry if they dont exist yet.
import pyodbc

server = 'JORDAN-PC\THUNBOTSQL'
database = 'Main'
username = 'sa'
password = 'ThunBeast'
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
#username = "'bigs'"

def _formatStringForQuery(string):
    newString = "'"+string+"'"
    return newString

def GuessWinsQuery(username):
    '''Executes a query for the number of wins for the username passed. Returns an int containing the number of wins'''
    username = _formatStringForQuery(username)
    cursor.execute("""
                    select NumWins
                        from GuessWins
                    where UserName={}
                    """.format(username))
    rows = cursor.fetchone()
    try:
        numWins = rows.NumWins
    except:
        numWins = 0 #otherwise they probably arent in the database

    return int(numWins)
    
def TotalGuessWinsQuery():
    '''Executes a query for the total number of guess wins'''
    cursor.execute("""
                    select total_wins
                        from TotalGuessWins
                    """)
    rows = cursor.fetchone()
    totalWins = rows.total_wins
    
    return int(totalWins)

def UpdateTotalWins():
    '''Increments the total_wins table by 1'''
    cursor.execute("update TotalGuessWins set total_wins=total_wins+1")
    cursor.commit()

def UpdateUserWins(username):
    '''Increments the personal win counter for a specified user if the user exists, if user doesnt exist it creates an entry with 1 win'''
    username = _formatStringForQuery(username)
    #cursor.execute("update GuessWins set NumWins=NumWins+1 where UserName={}".format(username))
    cursor.execute("""if not exists(select * from GuessWins where UserName = {}) 
                    BEGIN
                        insert into GuessWins(UserName, NumWins) VALUES({}, 1)
                    END
                    ELSE
                    BEGIN  
                        UPDATE GuessWins
                        set NumWins = NumWins + 1
                        where UserName = {}
                    END                                                     """.format(username, username, username))
    cursor.commit()

def GetEmoteList(emoteList):
    '''Reads the emotes table into memory. returns a list object'''
    cursor.execute("""select * from EmoteList""")
    rows = cursor.fetchall()
    for row in rows:
        emoteList.append(row.emote)
    return emoteList

def GetChannelSpecificEmotes(emoteList, channel):
    '''Appends channel specific emotes to the active emote list'''
    channel = _formatStringForQuery(channel)
    cursor.execute("""select * from UniqueEmoteList where channel = {}""".format(channel))
    rows = cursor.fetchall()
    for row in rows:
        emoteList.append(row.emote)
    return emoteList

def RegisterUniversalEmote(emote):
    '''Adds a universal emote to the emote DB. Inputs are the emote to be added'''
    emote = _formatStringForQuery(emote)
    cursor.execute("""
                    if not exists(select * from EmoteList where emote = {})
                    BEGIN
                        insert into EmoteList(emote) values({})
                    END
                    """.format(emote, emote))
    cursor.commit()

def RegisterChannelEmote(channel, emote):
    '''Added channel specific emote to the DB. Inputs are the emote to be added and the name of the channel'''
    emote = _formatStringForQuery(emote)
    channel = _formatStringForQuery(channel)
    cursor.execute("""
                    if not exists(select * from UniqueEmoteList where emote = {} and channel = {})
                    BEGIN
                        insert into UniqueEmoteList(channel, emote) values({}, {})
                    END
                    """.format(emote, channel, channel, emote))
    cursor.commit()

def UnregisterUniversalEmote(emote):
    '''Removes a universal emote from the DB. Inputs are the emote to tbe removed'''
    emote = _formatStringForQuery(emote)
    cursor.execute("""
                    if exists(select * from EmoteList where emote = {})
                    BEGIN
                        delete from EmoteList
                            where emote = {}
                    END
                    """.format(emote, emote))
    cursor.commit()


def UnregisterChannelEmote(channel, emote):
    '''Remove channel specific emote from the DB. Inputs are the emote to be removed along with the channel name'''
    emote = _formatStringForQuery(emote)
    channel = _formatStringForQuery(channel)
    cursor.execute("""
                    if exists(select * from UniqueEmoteList where emote = {} and channel = {})
                    BEGIN
                        delete from UniqueEmoteList
                            where (channel = {} and emote = {})
                    END
                    """.format(emote, channel, channel, emote))
    cursor.commit()