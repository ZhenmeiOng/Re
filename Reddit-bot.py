# to check which Python Version is being used (debugging)
import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

import praw #a wrapper for using Reddit API
import config
import time
import os
import requests

# Section 2
def bot_login():
    print("Logging in...")
    r = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "The First Bot of Ooga")
    print ("Logged in!") # for debugging
    return r

# Section 3
def run_bot(r, replied_comments):
    try:
        print("Obtaining 25 comments...")
        # replied_comments = []    // we can't initialise the array here cuz it'll become empty everytime run_bot is called from the main code
        for comment in r.subreddit('test').comments(limit=25):
            if "!joke" in comment.body and comment.id not in replied_comments and comment.author != r.user.me():
                print("String \"joke\" found! Sending a reply to comment " + comment.id )

                # Section 8
                reply = "Here is your requested Chuck Norris joke:\n\n"
                joke = requests.get('https://api.chucknorris.io/jokes/random').json()['value']
                reply += ">" + joke 
                reply += "\n\nCredit: [api.chucknorris.io](https://api.chucknorris.io/)"
                comment.reply(reply)

                # comment.reply("We found a dogs lover! [Here](https://www.earth.com/_next/image/?url=https%3A%2F%2Fcff2.earth.com%2Fuploads%2F2023%2F08%2F26042949%2FNational-Dog-Day--1400x850.jpg&w=1200&q=75) is a pic of my doggie!")
                print("Replied to comment " + comment.id)
                replied_comments.append(comment.id)

                with open("replied_comments.txt", "a") as f:   # Section 6
                    f.write(comment.id + "\n")                 # Section 6
        
        print("Sleeping for 10 seconds...")
        time.sleep(10)

    # for debugging purposes
    except praw.exceptions.APIException as e:
        print(f"APIException: {e}")
    except praw.exceptions.PRAWException as e:
        print(f"PRAWException: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Section 5
def get_saved_comments():
    if not os.path.isfile("replied_comments.txt"):
        replied_comments = []
    else:
        with open("replied_comments.txt", "r") as f:
            replied_comments = f.read()
            replied_comments = replied_comments.split("\n")
            replied_comments = list(filter(None, replied_comments)) # to filter out the last empty line of the text file from the array
    return replied_comments

r = bot_login()
# replied_comments = [] # we initialise the array here for only once
replied_comments = get_saved_comments()   # Section 7
while True: # Section 4
    run_bot(r, replied_comments)

