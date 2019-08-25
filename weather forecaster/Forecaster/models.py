from Forecaster import login_manager, forecaster, database as db
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_sqlalchemy import Model


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"User:{self.id}, {self.email}, {self.username}"

    def get_reset_token(self, expires_sec=1000):
        s = Serializer(forecaster.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id":self.id}).decode("utf-8")

    @staticmethod
    def validate_reset_token(token):
        s = Serializer(forecaster.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)