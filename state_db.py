
import sqlite3

con = sqlite3.connect('state_info.db')
cur = con.cursor()


'''using try statement to avoid error when creating table incase table already exists'''

cur.execute("CREATE TABLE IF NOT EXISTS accounts(user_id int PRIMARY KEY, state text)")



def update_state(user_id, state_):
    """REMEMBER TO VERIFY ACCOUNT DURING PRODUCTION"""
    try:
        cur.execute("INSERT OR REPLACE into accounts values (?, ?)", (user_id, state_))
        con.commit()
        return True
    except:
        return False
    
def get_state(user_id):
    try:
        cur.execute(f"SELECT user_id, state from accounts WHERE user_id = {user_id}")
        res_t = cur.fetchone()
        return res_t
    except:
        return False