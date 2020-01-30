from flask import Flask, request, session
#from flask_httpauth import HTTPBasicAuth
#from flask_sqlalchemy import SQLAlchemy
#from passlib.apps import custom_app_context as pwd_context
import reddit_scraper

app = Flask(__name__, static_folder='static')

my_reddit = reddit_scraper.Reddit('credentials.txt')
my_reddit.get_submissions('askreddit')


@app.route('/', methods=['GET'])
def get_urls():
    return str(my_reddit.get_post_details('url'))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
