API_KEY = "upu3OsjyPDxMCvpIpYEIIKpiL"
API_KEY_SECRET = "dKIrFVxcrXJyJ1y7XuWaGpVgcSfA9HEXgWfBsv49I1dwNCC5rI"

Access_Token = "1527048299617869825-RUfyWyKrmIkFnG1QX8CZpHkZDm00c0"
Access_Token_Secret = "MCU3aw3SRsN2ncTUCrPoUklHVEQKwbodiqX38f3UDBnii"

import json
# from p# import p#
import tweepy
from tweepy.errors import NotFound, \
    Forbidden, Unauthorized, TooManyRequests, \
    BadRequest, HTTPException, TweepyException

import time
import ast
from datetime import datetime

main_man = "GeltToken"


def unix_time():
    dtime = datetime.now()
    unix_time = time.mktime(dtime.timetuple())
    return float(unix_time)


auth = tweepy.OAuth1UserHandler(
    consumer_key=API_KEY,
    consumer_secret=API_KEY_SECRET,
    access_token=Access_Token,
    access_token_secret=Access_Token_Secret
)

api = tweepy.API(auth, wait_on_rate_limit=True)

schema = {
    "GeltToken": {
        "followers": [],
        "no_follower": 0,
        "time": unix_time()
    }
}


def read_db_file():
    # Opening JSON file
    json_file = open('data.db', "r")
    db_data = json_file.read()
    json_file.close()
    if db_data.strip() == '':
        #("hello with the strip")
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
            # #(i.id_str)
            # #(i.name)
            # #(i.screen_name)
            # #("\n\n\n")
            #("i reached find")

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
        #("not found")
        return 0
    except BadRequest:
        #("ko wole")
        return 0


def check_user(user_id: str = None, screen_name: str = None):
    # for x in screen_name""
    try:
        i = api.get_user(user_id=user_id, screen_name=screen_name)
        if i:
            # #(i.id_str)
            # #(i.screen_name)
            # #(i.name)
            # #(i.followers_count)
            # #(i.profile_image_url)
            # #(i.profile_image_url_https)
            # #("https://twitter.com/" + i.screen_name)
            # #(vars(i))
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
            #("noting related to the name exist")
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


def check_main_man():
    while True:
        try:
            global check_twitter
            main_id = "salman80540408"
            check_main = check_user(screen_name=main_id)
            if check_main or not isinstance(check_main, list):
                write_db_file(str(check_main[3]))
        except:
            #("error")
            pass
        time.sleep(10)


def scrape(r, count, num: int = 50):
    ma = int(r.get("GeltToken").get("no_follower")) - int(count)
    if ma < 20:
        a = api.get_follower_ids(screen_name=main_man, count=ma)
        a = [str(i) for i in a]
        r["GeltToken"]["followers"].extend(list(a))
        r["GeltToken"]["no_follower"] = count
        #("\n\n\n\n\nreading from less than 20\n\n\n\n\n\n")
        #(f"\n\n\n\n\n{str(r)}\n\n\n\n\n\n")
        write_db_file(r)
        return a
    elif ma > 20:
        n = 0
        l = []
        for page in tweepy.Cursor(api.get_follower_ids, screen_name=main_man).items(limit=2000):
            # #(page)

            l.append(str(page))
            if n == num:
                break
            n += 1

        b = r.get("GeltToken").get("followers")
        #("\n\n\n\n\nreading from less than 20\n\n\n\n\n\n")
        #(f"\n\n\n\n\n{str(r)}\n\n\n\n\n\n")
        b.extend(l)
        c = list(set(b))
        r["GeltToken"]["no_follower"] = count
        r["GeltToken"]["followers"] = c
        write_db_file(r)
        return l


def confirm_scrape(num: int = 50, screen_name: str = None):
    """ (i.id_str, i.screen_name, i.name, i.followers_count, image)"""
    a = check_user(screen_name=screen_name)
    man = check_user(screen_name=main_man)
    if a or not isinstance(a, list):
        count = man[3]
        r = read_db_file()

        #(f"\n\n\n\n\nthis is the number of followers in db_file{r.get('GeltToken').get('no_follower')}\n\n\n\n\n\n")

        if screen_name:
            if int(r.get("GeltToken").get("no_follower")) < int(count):
                #("\n\n\n\n\nthis is under confirm_scrape where screen_name was supplied\n\n\n\n\n\n")
                scrape(r=r, count=count, num=20)
        elif not screen_name:
            if int(r.get("GeltToken").get("no_follower")) < int(count):
                #("\n\n\n\n\nthis is under confirm_scrape where screen_name was not supplied\n\n\n\n\n\n")
                scrape(r=r, count=count, num=num)

    else:
        with open("logg.t", "w") as F:
            F.write("it did't do it")
        # #("it did't do it")


if __name__ == '__main__':
    pass
