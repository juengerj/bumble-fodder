from flask import Flask, request, session, render_template
#from flask_httpauth import HTTPBasicAuth
#from flask_sqlalchemy import SQLAlchemy
#from passlib.apps import custom_app_context as pwd_context
import reddit_scraper

app = Flask(__name__, static_folder='static')

my_reddit = reddit_scraper.Reddit('credentials.txt')


@app.route('/', methods=['GET'])
def get_urls():
    subreddit = request.args.get('subreddit')
    if subreddit:
        my_reddit.get_submissions(subreddit)
    else:
        my_reddit.get_submissions('dogswithjobs')
        # my_reddit.get_submissions('funny')
    results = my_reddit.get_post_details('url', 'thumbnail')
    # print(results)
    # return results
    # results = str(['fish','pony','hip','hop','hip-hop-a-bottom-us'])

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='4799')
