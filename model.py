import os
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


# from flask_login import UserMixin


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # subreddits = db.relationship('Subreddit', secondary='user_subreddits')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @staticmethod
    def list_users():
        # def list_users(self):
        users = User.query.all()

        user_list = []
        for user in users:
            # print('Username: %s' % user.username)
            user_list.append(user.username)

        return user_list

    @staticmethod
    def get_user(username):
        return User().query.filter_by(username=username).first()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_user(self, password):
        self.set_password(password)
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def add_user_subreddit(username, subreddit):
        user = User.get_user(username)
        subr = Subreddit.get_subreddit(subreddit)
        if UserSubreddit.query.filter_by(user_id=user.id, subreddit_id=subr.id).first() is None:
            db.session.add(UserSubreddit(user_id=user.id, subreddit_id=subr.id))
            db.session.commit()


class Subreddit(db.Model):
    __tablename__ = 'subreddit'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)

    @staticmethod
    def list_subreddits():
        subreddits = Subreddit.query.all()

        subreddit_list = []
        for subreddit in subreddits:
            subreddit_list.append(subreddit.name)

        return subreddit_list

    @staticmethod
    def get_subreddit(subreddit_name):
        return Subreddit().query.filter_by(name=subreddit_name).first()

    def add_subreddit(self):
        db.session.add(self)
        db.session.commit()


class UserSubreddit(db.Model):
    __tablename__ = 'user_subreddits'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    subreddit_id = db.Column(db.Integer(), db.ForeignKey('subreddit.id', ondelete='CASCADE'))

    @staticmethod
    def list_user_subreddit_mappings():
        user_subreddit_mappings = UserSubreddit().query.all()

        user_subreddit_list = []
        for user_subreddit in user_subreddit_mappings:
            user_subreddit_list.append(user_subreddit)

        return user_subreddit_list


if __name__ == '__main__':
    if not os.path.exists('user_db.sqlite'):
        db.create_all()
    # new_user = User(username='john')
    # new_user.add_user('doe')
    # new_user1 = User(username='jane')
    # new_user1.add_user('doe')
    # new_subreddit = Subreddit(name='dogswithjobs')
    # new_subreddit.add_subreddit()
    print(User.list_users())
    print(User.get_user('john').id)
    print(Subreddit.list_subreddits())
    print(Subreddit.get_subreddit('dogswithjobs').id)
    # User.add_user_subreddit('john', 'dogswithjobs')
    subs = UserSubreddit.list_user_subreddit_mappings()
    for i in subs:
        print('User %s has subreddit %s' % (i.user_id, i.subreddit_id))
