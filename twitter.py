API_KEY = "upu3OsjyPDxMCvpIpYEIIKpiL"
API_KEY_SECRET = "dKIrFVxcrXJyJ1y7XuWaGpVgcSfA9HEXgWfBsv49I1dwNCC5rI"

Access_Token = "1527048299617869825-RUfyWyKrmIkFnG1QX8CZpHkZDm00c0"
Access_Token_Secret = "MCU3aw3SRsN2ncTUCrPoUklHVEQKwbodiqX38f3UDBnii"


import json
from pprint import pprint
import tweepy
from tweepy.errors import NotFound, \
    Forbidden, Unauthorized, TooManyRequests, \
    BadRequest, HTTPException, TweepyException

import time
import ast
import time
from datetime import datetime

from updater import confirm_scrape

auth = tweepy.OAuth1UserHandler(
    consumer_key=API_KEY,
    consumer_secret=API_KEY_SECRET,
    access_token=Access_Token,
    access_token_secret=Access_Token_Secret
)

api = tweepy.API(auth, wait_on_rate_limit=True)

def unix_time():
    dtime = datetime.now()
    unix_time = time.mktime(dtime.timetuple())
    return float(unix_time)




def read_db_file():
    # Opening JSON file
    json_file = open('data.db', "r")
    db_data = json_file.read()
    json_file.close()
    if db_data.strip() == '':
        #"hello with the strip")
        return "0"

    data = ast.literal_eval(db_data)
    return data

def write_db_file(d):
    d["GeltToken"]["time"] = unix_time()
    with open('data.db', "w") as json_file:
        data = json_file.write(str(d))

try:
    open("data.db", "r")
except:
    schema = {
        "GeltToken": {
            "followers": [],
            "no_follower": 0,
            "time": unix_time()
        }
    }
    write_db_file(schema)


def find_user(screen_name: str = None):
    l = []
    n = []
    try:
        a = 0
        for i in api.search_users(screen_name):
            # #i.id_str)
            # #i.name)
            # #i.screen_name)
            # #"\n\n\n")
            #"i reached find")

            l.append({
                "id": i.id_str,
                "name": i.name,
                "screen_name": i.screen_name
            })
            if a > 7:
                break
            a += 1
            # n.append(i.screen_name)
        return l

    except NotFound:
        #"not found")
        return 0
    except BadRequest:
        #"ko wole")
        return 0


def check_user(user_id: str = None, screen_name: str = None):
    # for x in screen_name""
    try:
        i = api.get_user(user_id=user_id, screen_name=screen_name)
        if i:
            #"\n\n\n\n\n\n\n\n\n\n\n")
            #i.id_str)
            #i.screen_name)
            #i.name)
            #i.followers_count)
            #i.profile_image_url)
            #i.profile_image_url_https)
            #"https://twitter.com/" + i.screen_name)
            #"\n\n\n\n\n\n\n\n\n\n\n")

            # #vars(i))
            if i.profile_image_url:
                image = i.profile_image_url
            elif i.profile_image_url_https:
                image = i.profile_image_url_https
            else:
                pass
            if i.id_str:
                return (i.id_str, i.screen_name, i.name, i.followers_count, image)
        else:
            b = find_user(screen_name)
            return b
    except Forbidden:
        return False
    except BadRequest:
        return False

    except NotFound:
        suspected_user = find_user(screen_name)
        if not suspected_user:
            #"noting related to the name exist")
            return None
        elif suspected_user:
            for i in suspected_user:
                screen = i.get("screen_name")
                namze = i.get("name")

                if screen_name == screen:
                    return check_user(screen_name=screen)
                elif screen_name == namze:
                    return check_user(screen_name=screen)
                else:
                    continue

            return suspected_user


try:
    open("data.db", "r")
except:
    check_main = check_user(screen_name="GeltToken")

    write_db_file(str(check_main[3]))

def check_follow(screen_name):
    """
    global check_twitter
    main_id = "GeltToken"
    check_main = check_user(screen_name=main_id)
    " (i.id_str, i.screen_name, i.name, i.followers_count, image)"
    r = read_db_file()
    #r)    #type(check_main[3]), type(r))
    #int(r))
    #int(check_main[3]))
    a = int(r)
    if int(check_main[3]) == a:
        return False
    elif int(check_main[3]) > a:
        write_db_file(str(check_main[3]))
        return True

    schema = {
        "GeltToken": {
            "followers": [],
            "no_follower": 0,
            "time": unix_time()
        }
    }
    """

    #f"\n\n\n\n\nthis is the screen name passed {screen_name}\n\n\n\n\n\n")
    check_main = check_user(screen_name=screen_name)
    if check_main:
        ids = check_main[0]
        r = read_db_file()
        #r)

        if str(ids) in r.get("GeltToken").get("followers"):
            #"\n\n\n\n\nFound the nigga\n\n\n\n\n\n")
            return True
        else:
            confirm_scrape(screen_name=screen_name)
            r = read_db_file()
            if str(ids) in r.get("GeltToken").get("followers"):
                #"\n\n\n\n\nWent online and Found the nigga\n\n\n\n\n\n")
                return True
            else:
                #"\n\n\n\n\nDidn't Found the nigga\n\n\n\n\n\n")
                return False
    else:

        pass
        #"\n\n\n\n\nthis is from the else part of check_follow\n\n\n\n\n\n")



