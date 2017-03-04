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

def _formatUsernameForQuery(username):
    newUserName = "'"+username+"'"
    return newUserName

def GuessWinsQuery(username):
    '''Executes a query for the number of wins for the username passed. Returns an int containing the number of wins'''
    username = _formatUsernameForQuery(username)
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
    
def CheckUser(username):
    '''checks if the user is in the GuessWins table'''

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
    '''Increments the personal win counter for a specified user'''
    username = _formatUsernameForQuery(username)
    cursor.execute("update GuessWins set NumWins=NumWins+1 where UserName={}".format(username))
    cursor.commit()
#cursor.execute("""
#                select UserName, NumWins
#                    from GuessWins
#                where UserName = {}
#                """.format(username))
#rows = cursor.fetchall()
#for row in rows:
#    print('%s has %i wins' %(row.UserName, row.NumWins))
#    row = cursor.fetchone()