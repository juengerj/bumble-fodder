import os
from flask import Flask, request, session, render_template
# from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
# from passlib.apps import custom_app_context as pwd_context
import reddit_scraper
from prawcore import NotFound

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

NUM_SUBREDDITS = 5
NUM_TOP_POSTS = 3
# my_reddit = reddit_scraper.Reddit('credentials.txt')
my_reddit = reddit_scraper.Reddit.get_instance()


def check_valid_num(subreddit_list):
    print(f"Len subreddits: {len(subreddit_list)}")
    if (len(subreddit_list) > NUM_SUBREDDITS) or (len(subreddit_list) <= 0):
        print("Error: invalid number of subreddits selected")
        return render_template('index.html')                        # TODO: render error message in index.html


def check_subreddits(subreddit_list):
    for sub in range(len(subreddit_list)):
        print(subreddit_list[sub])
        exists = check_sub_exists(subreddit_list[sub])
        if not exists:
            print("Oh no, that subreddit does not exist")           # TODO: render error message in index.html
            return False

    return True


def check_sub_exists(subreddit):
    # Resource: https://www.reddit.com/r/redditdev/comments/68dhpm/praw_best_way_to_check_if_subreddit_exists_from/
    exists = True
    try:
        my_reddit.subreddit.search_by_name(subreddit, exact=True)   # TODO: figure out error here
    except NotFound:
        exists = False
    return exists


@app.route('/', methods=['GET'])
def get_urls():
    subreddits = []
    results = []
    urlsGoHere = []
    thumbnailsGoHere = []

    check_valid_num(subreddits)
    # check_subreddits(subreddits)

    # print("Valid number of subreddits")
    for x in range(NUM_SUBREDDITS):
        subreddits.append(request.args.get('subreddit' + str(x)))
        if subreddits[x]:
            if check_sub_exists(subreddits[x]):
                print("Valid subreddit name!")
                my_reddit.get_submissions(subreddits[x])
                results.append(my_reddit.get_post_details('url', 'thumbnail'))
                urlsGoHere.append(results[x][::2])
                thumbnailsGoHere.append(results[x][1::2])
                print(thumbnailsGoHere[x])
            else:
                print("Oh no, invalid subreddit")                   # TODO: render error message in index.html
        else:
            my_reddit.get_submissions('dogswithjobs')
            results.append(my_reddit.get_post_details('url', 'thumbnail'))
            urlsGoHere.append(results[x][::2])
            thumbnailsGoHere.append(results[x][1::2])

        # print("Getting subreddit", file=sys.stdout)
        # if subreddit:
        # my_reddit.get_submissions(subreddit)
        # else:
        # my_reddit.get_submissions('dogswithjobs')

        # print("storing subreddit", file=sys.stdout)

        # results = my_reddit.get_post_details('url', 'thumbnail')
        # data={'urls':urlsGoHere, 'thumbnails':thumbnailsGoHere,'ids':idsGoHere}
        data = [[] for i in range(NUM_SUBREDDITS)]
        print(data)

    for x in range(NUM_SUBREDDITS):
        for i in range(NUM_TOP_POSTS):
            data[x].append({'thumbnail': thumbnailsGoHere[x][i], 'url': urlsGoHere[x][i], 'id': str(x) + str(i)})
    # return results
    # results = str(['fish','pony','hip','hop','hip-hop-a-bottom-us'])
    print(data)
    return render_template('index.html', data=data)


# @app.route('/top5', methods=['GET'])
# NUM_OF_SUBREDDITS = 5
# def get_top5():
#     top5subreddits[] = []
#     for i in range(NUM_OF_SUBREDDITS):
#         top5subreddits[i] = 


if __name__ == '__main__':
    # if not os.path.exists('user_db.sqlite'):
    #     db.create_all()
    app.debug = True
    app.run(host='0.0.0.0', port='23234')
