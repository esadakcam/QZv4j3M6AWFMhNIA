from flask import Flask, render_template
import twint
import json
import os
class Tweet:
    def __init__(self,context,retweet ,like ,url,user,username,date,time,replies): #tweet class
        self.context = context
        self.retweet = retweet
        self.like = like
        self.url = url
        self.user = user
        self.username = username
        self.date = date
        self.time = time
        self.replies = replies

def sortR(tweet): #sort methods
    return tweet.retweet
def sortL(tweet):
    return tweet.like
def sortD(tweet):
    return tweet.date
tweets = []
flag = False
def read():  #reading data
    document_path = os.path.join('file.txt')
    with app.open_resource(document_path, 'r') as file1:
        Lines = file1.readlines()
        for  i in  range(len(Lines)):
            res = json.loads(Lines[i])
            tw = Tweet(res["tweet"],res["retweets_count"],res["likes_count"],res["link"],res["name"],res["username"],res["date"],res["time"],res["replies_count"])
            tweets.append(tw)


app = Flask(__name__)
@app.route("/")
def index():
    tweets.sort(reverse=True,key=sortD)
    return render_template("index.html", tweets = tweets)

@app.route("/like")
def like():
    tweets.sort(reverse=True,key=sortL)
    return render_template("index.html", tweets = tweets)

@app.route("/retweet")
def retweet():
    tweets.sort(reverse=True,key=sortR)
    return render_template("index.html", tweets = tweets)

@app.route("/refresh")
def refresh():
    os.remove("file.txt")
    c = twint.Config()
    c.Search = "request for startup"
    c.Limit = 1000 #number of total tweets
    c.Store_json = True
    c.Output = "file.txt"
    # Run
    twint.run.Search(c)
    tweets.clear()
    flag = True
    read()
    return render_template("index.html", tweets = tweets)


if(flag == True):
    flag = False
    refresh()


if __name__ == "__main__":
    read()
    app.run(debug=False)
