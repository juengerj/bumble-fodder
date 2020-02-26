import os
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm
# from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse

# from flask_httpauth import HTTPBasicAuth
# from flask_sqlalchemy import SQLAlchemy

# from passlib.apps import custom_app_context as pwd_context

import reddit_scraper
import consts
from model import db, User, Subreddit, UserSubreddit

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "we are great"

db.init_app(app)
login = LoginManager(app)
login.login_view = "login"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# my_reddit = reddit_scraper.Reddit('credentials.txt')
my_reddit = reddit_scraper.Reddit.get_instance()


def check_valid_num(subreddit_list):
    print(f"Len subreddits: {len(subreddit_list)}")
    if (len(subreddit_list) > consts.NUM_SUBS) or (len(subreddit_list) <= 0):
        error = "Invalid number of subreddits"
        print(error)
        return False
    return True


def check_sub_exists(sub_name):
    # my_reddit.subreddits(subreddit).search_by_name(subreddit, exact=True)   # This did not work due to attribute error
    current = my_reddit.reddit.subreddit(sub_name)

    # Test with invalid name
    # invalid = my_reddit.reddit.subreddit('dogswithjobsandcatswithknivesthiscantberealright')

    if current.display_name is sub_name:
        print("It's a match!")
        return True

    return False


@app.route('/', methods=['GET'])
@app.route('/index')
def index():
    subreddits = []
    results = []
    urlsGoHere = []
    thumbnailsGoHere = []

    # print("Valid number of subreddits")
    if request.args.get('user'):
        user = request.args.get('user')
        # print(user)
        user_subreddits = UserSubreddit.get_user_subreddits(user)
        for i in user_subreddits:
            subreddit_name = Subreddit.get_subreddit_by_id(i.subreddit_id).name
            subreddits.append(subreddit_name)

    for x in range(consts.NUM_SUBS):
        subreddits.append(request.args.get('subreddit' + str(x)))
        
        enough = check_valid_num(subreddits)  # TODO: move error checking so after subs actually added to subreddits list
        if not enough:
            error = "Invalid number of subreddits.\nPlease enter between 1 and 5 subreddits."
            return render_template('index.html', error=error)

        if subreddits[x]:
            print("checking new sub")

            if check_sub_exists(subreddits[x]):
                print("Valid subreddit name!")
                my_reddit.get_submissions(subreddits[x])
                results.append(my_reddit.get_post_details('url', 'thumbnail'))
                urlsGoHere.append(results[x][::2])
                thumbnailsGoHere.append(results[x][1::2])
            else:
                print("Oh no, invalid subreddit")  # TODO: render error message in index.html

    data = [[] for i in range(consts.NUM_SUBS)]
    # print(data)

    for x in range(consts.NUM_SUBS):
        if (subreddits[x]):
            data[x] = {'subreddit': subreddits[x], 'data':[]}
            for i in range(3):
                data[x]['data'].append({'thumbnail':thumbnailsGoHere[x][i],'url':urlsGoHere[x][i],'id':str(x)+str(i)})

    # print(data)
    return render_template('index.html', data=data)


# RIPPED
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index', user=user.username)
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    print("Before validate_on_submit")
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print("Before flashing")
        if user is not None:
            flash('Please use a different username')
            return redirect(url_for('register'))

        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/secret')
@login_required
def secret():
    if current_user.is_authenticated:
        return render_template('secret.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    if not os.path.exists('user_db.sqlite'):
        with app.app_context():
            db.create_all()
    app.debug = True
    app.run(host=consts.HOST, port=consts.PORT)
