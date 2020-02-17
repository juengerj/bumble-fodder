from flask import Flask, request, session, render_template
#from flask_httpauth import HTTPBasicAuth
#from flask_sqlalchemy import SQLAlchemy
#from passlib.apps import custom_app_context as pwd_context
import reddit_scraper

app = Flask(__name__, static_folder='static')

# my_reddit = reddit_scraper.Reddit('credentials.txt')
my_reddit = reddit_scraper.Reddit.get_instance()


@app.route('/', methods=['GET'])
def get_urls():
    subreddit = request.args.get('subreddit')
    # print("Getting subreddit", file=sys.stdout)
    if subreddit:
        my_reddit.get_submissions(subreddit)
    else:
        my_reddit.get_submissions('dogswithjobs')
    
    # print("storing subreddit", file=sys.stdout)
    
    results = my_reddit.get_post_details('url', 'thumbnail')
    urlsGoHere=results[::2]
    thumbnailsGoHere=results[1::2]
    # data={'urls':urlsGoHere, 'thumbnails':thumbnailsGoHere,'ids':idsGoHere}
    data = []
    for i in range(0,5):
        data.append({'thumbnail':thumbnailsGoHere[i],'url':urlsGoHere[i],'id':i})
    # return results
    # results = str(['fish','pony','hip','hop','hip-hop-a-bottom-us'])

    return render_template('index.html', data=data)

# @app.route('/top5', methods=['GET'])
# NUM_OF_SUBREDDITS = 5
# def get_top5():
#     top5subreddits[] = []
#     for i in range(NUM_OF_SUBREDDITS):
#         top5subreddits[i] = 




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='4799')
