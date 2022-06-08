
import sqlite3

con = sqlite3.connect('verify.db')
cur = con.cursor()


'''using try statement to avoid error when creating table incase table already exists'''

cur.execute("CREATE TABLE IF NOT EXISTS accounts(user_id text, follower_id text, followed bool)")

def alpha(user_id, follower_id):
    try:
        cur.execute("INSERT into accounts values (?, ?)", (user_id, follower_id, 'False'))
        con.commit()
        return True
    except:
        return False

def beta(user_id):
    try:
        cur.execute(f"SELECT user_id, follower_id, followed from accounts WHERE user_id = {user_id}")
        res_t = cur.fetchall()
        print(res_t)
        cur.execute("INSERT OR REPLACE into accounts values (?, ?)", (user_id, ))
        return res_t
    except:
        return False

beta('1')