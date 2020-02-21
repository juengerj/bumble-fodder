from flask import Flask, request, render_template, flash
# from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

# from passlib.apps import custom_app_context as pwd_context
import reddit_scraper
import consts

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# my_reddit = reddit_scraper.Reddit('credentials.txt')
my_reddit = reddit_scraper.Reddit.get_instance()


def check_valid_num(subreddit_list):
    print(f"Len subreddits: {len(subreddit_list)}")
    if (len(subreddit_list) > consts.NUM_SUBS) or (len(subreddit_list) <= 0):
        error = "Invalid number of subreddits"
        print(error)
        return False                       # TODO: render error message in index.html
    return True


def check_subreddits(subreddit_list):
    error = None
    for sub in range(len(subreddit_list)):
        # print(subreddit_list[sub])
        # exists = check_sub_exists(subreddit_list[sub])
        exists = True
        if not exists:
            print("Oh no, that subreddit does not exist")           # TODO: render error message in index.html
            return False

    return True


def check_sub_exists(subreddit):
    # Resource: https://www.reddit.com/r/redditdev/comments/68dhpm/praw_best_way_to_check_if_subreddit_exists_from/
    exists = True
    # try:
    #     my_reddit.subreddits.search_by_name(subreddit, exact=True)   # TODO: figure out error here
    # except NotFound:
    #     exists = False
    return exists


@app.route('/', methods=['GET'])
def get_urls():
    subreddits = []                                                     # Test with invalid number
    # subreddits = ["aww", "aww", "aww", "aww", "aww", "aww"]           # Test with invalid number
    results = []
    urlsGoHere = []
    thumbnailsGoHere = []

    enough = check_valid_num(subreddits)            # TODO: move error checking so after subs added to subreddits list
    if not enough:
        error = "Invalid number of subreddits.\nPlease enter between 1 and 5 subreddits."
        return render_template('index.html', error=error)

    # print("Valid number of subreddits")
    for x in range(consts.NUM_SUBS):
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

            data = [[] for i in range(consts.NUM_SUBS)]
            # print(data)

        for x in range(consts.NUM_SUBS):
            for i in range(consts.NUM_TOP):
                data[x].append({'thumbnail': thumbnailsGoHere[x][i], 'url': urlsGoHere[x][i], 'id': str(x) + str(i)})
        return render_template('index.html', data=data)


# @app.route('/top5', methods=['GET'])
# NUM_OF_SUBREDDITS = 5
# def get_top5():
#     top5subreddits[] = []
#     for i in range(NUM_OF_SUBREDDITS):
#         top5subreddits[i] = 


if __name__ == '__main__':
    # if not os.path.exists('user_db.sqlite'):
    # 	db.create_all()
    app.debug = True
    app.run(host=consts.HOST, port=consts.PORT)
