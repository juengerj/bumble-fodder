from flask import Flask, request, render_template, flash, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

# from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

# from passlib.apps import custom_app_context as pwd_context
import reddit_scraper
import consts

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "we are great"

db = SQLAlchemy(app)
login = LoginManager(app)
login.init_app(app)
login.login_view = "login"

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# my_reddit = reddit_scraper.Reddit('credentials.txt')
my_reddit = reddit_scraper.Reddit.get_instance()


@app.route('/', methods=['GET'])
def get_urls():
    subreddits = []
    results = []
    urlsGoHere = []
    thumbnailsGoHere = []

    for x in range(consts.NUM_SUBS):
        subreddits.append(request.args.get('subreddit' + str(x)))
        if subreddits[x]:
            my_reddit.get_submissions(subreddits[x])
            results.append(my_reddit.get_post_details('url', 'thumbnail'))
            urlsGoHere.append(results[x][::2])
            thumbnailsGoHere.append(results[x][1::2])
            print(thumbnailsGoHere[x])
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
    data = [[] for i in range(consts.NUM_SUBS)]

    for x in range(consts.NUM_SUBS):
        for i in range(consts.NUM_TOP):
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
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

if __name__ == '__main__':
    # if not os.path.exists('user_db.sqlite'):
    # 	db.create_all()
    app.debug = True
    app.run(host=consts.HOST, port=consts.PORT)
