from app import db

class UserInfo(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    userUID = db.Column('userUID', db.Text, unique=True)
    username = db.Column('username', db.Text, unique=True)
    firstName = db.Column('firstName', db.Text)
    lastname = db.Column('lastName', db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'userUID': self.userUID,
            'firstname': self.firstName,
            'lastname': self.lastname
        }