from flask import Flask, request, session, render_template
#from flask_httpauth import HTTPBasicAuth
#from flask_sqlalchemy import SQLAlchemy
#from passlib.apps import custom_app_context as pwd_context

import numpy
import pandas as pds
import pprint
import reddit_scraper


app = Flask(__name__, static_folder='static')

# my_reddit = reddit_scraper.Reddit('credentials.txt')
my_reddit = reddit_scraper.Reddit.get_instance()

################################################################
###############DEBUG###ZONE####################################


# subreddit = input("Enter Subreddit ")
# data = []
# # subreddit = request.args.get('subreddit')
# if subreddit:
#     my_reddit.get_submissions(subreddit)
# else:
#     my_reddit.get_submissions('dogswithjobs')
# submissions = list(my_reddit.submission)
# # for entry in submissions:
# #     pprint.pprint(vars(entry))

# #TITLES OF POSTS IN SUBREDDIT
# print('////////////////////////TITLES/////////////////////////////////////////')
# for entry in submissions:
#     print(entry.title)


# #NUMBER OF COMMETNS
# print('////////////////////////NUMBER OF COMMENTS/////////////////////////////')
# for entry in submissions:
#     print(len(entry.comments))

# #COMMENTS
# # for entry in submissions:
# #     print('////////////////////////COMMENTS///////////////////////////////////////')
# #     for comment in entry.comments:
# #         print(comment.body)

# print(len(submissions))
# # pprint.pprint(vars(my_reddit.submission))








##################################################################


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

@app.route('/comments', methods=['GET'])
def get_comments():
    data = []
    subreddit = request.args.get('subreddit')
    if subreddit:
        my_reddit.get_submissions(subreddit)
    else:
        my_reddit.get_submissions('dogswithjobs')
    submissions = list(my_reddit.submission)
    titles = []
    NumOfPostComments =[]
    labels =[]
    for entry in submissions:
        titles.append(entry.title)
        labels.append(entry.title[0:5])
        # NumOfPostComments.append(len(entry.comments))
        NumOfPostComments.append(entry.num_comments)
    for index in range(len(submissions)):
        data.append({'title':titles[index],'total_comments':NumOfPostComments[index],'index':index})
    legend = subreddit + ' Comments'

    return render_template('comments.html', data = data, subreddit = subreddit, legend = legend, labels = labels, values = NumOfPostComments)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='4799')
