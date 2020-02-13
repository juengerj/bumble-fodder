from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    def __repr__(self):
        return '<User {}>'.format(self.username)   

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

if __name__ == '__main__':
    u = User(username='susan', email='susan@example.com')
    u.set_password('mypassword')
    u.check_password('anotherpassword')
    print (result)
    result = u.check_password('anotherpassword')
