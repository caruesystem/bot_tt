from binascii import unhexlify
import sqlite3
import secrets, random
import ast

con = sqlite3.connect('cust_info.db')
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS accounts(user_id int PRIMARY KEY, twitter_username text UNIQUE, bot_user_id int, wallet text, balance int, referrals int, referred_by int, activated bool)")


##################GETTING BOT_USER_ID###################
def get_bot_(bot_user_id):
    cur.execute(f"SELECT bot_user_id FROM accounts WHERE bot_user_id = {bot_user_id}")
    return cur.fetchone()

def secrete():
    p = random.randint(100000, 10000000)
    ko = get_bot_(p)
    if ko != None:
        secrete()
    else:
        return p

########################################################

def insert_cust_ref(user_id, ref_by):
    try:
        cur.execute("INSERT into accounts values (?, ?, ?, ?, ?, ?, ?, ?)", (user_id, None, secrete(), None, 100, 0, ref_by, False))
        con.commit()
        return True
    except:
        return False

def insert_cust_twit(user_id, twit_tt):
    """REMEMBER TO VERIFY ACCOUNT DURING PRODUCTION"""
    # try:
    cur.execute("UPDATE accounts SET twitter_username = (?) WHERE user_id = (?);", (twit_tt, user_id))
    con.commit()
    #     return True
    # except:
    #     return True
        


def insert_cust_wallet(user_id, wallet):
    try:
        cur.execute(f"UPDATE accounts SET wallet = (?) WHERE user_id = (?);", (wallet, user_id))
        con.commit()
        return True
    except:
        return False

def insert_cust_referral(user_id):
    try:
        cur.execute(f"SELECT referrals from accounts WHERE user_id = {user_id}")
        qo = cur.fetchone()
        global oq
        for i in qo:
            oq = i+1
        cur.execute("UPDATE accounts SET referrals = (?) WHERE user_id = (?);", (oq, user_id))
        con.commit()
        return True
    except:
        return False

def insert_cust_balance(user_id, amt):
    # try:
    cur.execute(f"SELECT balance from accounts WHERE user_id = {user_id}")
    eka = cur.fetchone()
    global ake
    for i in eka:
        ake = i + amt
    cur.execute("UPDATE accounts SET balance = (?) WHERE user_id = (?);", (ake, user_id))
    con.commit()
    #     return True
    # except:
    #     return False

def insert_cust_active(user_id):
    try:
        cur.execute("UPDATE accounts SET activated = (?) WHERE user_id = (?);", (True, user_id))
        con.commit()
    except:
        pass

def user_exist(user_id):
    cur.execute(f"SELECT user_id from accounts WHERE user_id = {user_id}")
    pool = cur.fetchone()
    return pool


def get_active(user_id):
    cur.execute(f"SELECT activated from accounts WHERE user_id = {user_id}")
    lopo = cur.fetchone()
    # #f"\n\n\n\n\nthis is from get active {lopo[0]}\n\n\n\n\n\n")
    try:
        if lopo[0] == True:
            return True
        else:
            return False
    except:
        return False

def get_balance(user_id):
    cur.execute(f"SELECT balance from accounts WHERE user_id = {user_id}")
    bal = cur.fetchone()
    #f"\n\n\n\n\nthis is from get balance{bal}\n\n\n\n\n\n")
    if bal[0]:
        return bal[0]
    else:
        return 0


def get_referral(user_id):
    cur.execute(f"SELECT bot_user_id from accounts WHERE user_id = {user_id}")
    ref = cur.fetchone()
    #f"\n\n\n\n\nthis is from get referral string{ref}\n\n\n\n\n\n")
    if ref[0]:
        return ref[0]
    else:
        return None

def get_referred_by(user_id):
    cur.execute(f"SELECT referred_by from accounts WHERE user_id = {user_id}")
    ref = cur.fetchone()
    cur.execute(f"SELECT user_id FROM accounts WHERE bot_user_id = {ref[0]}")
    fer = cur.fetchone()
    #f"\n\n\n\n\nthis is from get referral string{ref}\n\n\n\n\n\n")
    if fer[0]:
        return int(fer[0])
    else:
        return None

def get_profile(user_id):
    cur.execute(f"SELECT twitter_username ,balance, referrals  from accounts WHERE user_id = {user_id}")
    prof = cur.fetchone()
    #f"\n\n\n\n\nthis is from get profile{prof}\n\n\n\n\n\n")

    if prof:
        return prof
    else:
        return None

def get_referral_num(text):
    cur.execute(f"SELECT user_id, referrals from accounts WHERE bot_user_id = {text}")
    refs = cur.fetchone()
    #f"\n\n\n\n\nthis is from get referral  num{refs}\n\n\n\n\n\n")
    if refs:
        return refs
    else:
        return 0



def update_referral_num(user_id, num):
    try:
        cur.execute("UPDATE accounts SET referrals = (?) WHERE user_id = (?);", (num, user_id))
        con.commit()
    except:
        pass
        #f"\n\n\n\n\ncouldn't update referral\n\n\n\n\n\n")


# get_active(1)

# insert_cust_ref(1,123456)
# insert_cust_balance(1, 100000000)
# insert_cust_wallet(2, 'qwertyio')
# insert_cust_referral(1)
# #secrete())


# ##########################################

# #wanna be database

# schema = {
#     "data": []
# }


# def read_secret() -> dict[list]:
#     # Opening JSON file
#     json_file = open('secret.db', "r")
#     db_data = json_file.read()
#     json_file.close()
#     if db_data.strip() == '':
#         #"hello with the strip")
#         return "0"

#     data = ast.literal_eval(db_data)
#     return data


# def write_secret(d):
#     with open('secret.db', "w") as json_file:
#         data = json_file.write(str(d))


# try:
#     open("secret.db", "r")
# except:

#     write_secret(schema)


# ###########################################################

# def secrete():
#     reu = secrets.token_hex(10)
#     r = read_secret()
#     #r)
#     you = r.get('data')
#     # #type(you))
#     if reu in you:
#         secrete()
#     else:
#         r["data"].append(reu)
#         write_secret(r)
#         #reu)
#         return int(reu, 16)

# def a(user_id):
#     p = int(user_id, 16)
#     cur.execute(f"SELECT bot_user_id from accounts WHERE bot_user_id = {p}")
#     vr = cur.fetchone()
#     #vr)

# a('7176526aee064964d513')
# #secrete())
###########################################################