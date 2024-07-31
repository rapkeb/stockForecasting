from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username, password):
        self._id = None
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.services = []

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_id(self, _id):
        self._id = _id

    def get_id(self):
        return str(self._id)
