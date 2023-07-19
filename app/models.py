from app import db
from sqlalchemy.orm import relationship
from datetime import datetime

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
    
class Project(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    date_added = db.Column('date_added', db.Date, default=datetime.utcnow)
    userUID = db.Column('userUID', db.Text)
    title = db.Column('title', db.Text)
    description = db.Column('description', db.Text)
    tasks = relationship("Task", back_populates="project")

    def serialize(self):
        return {
            'id': self.id,
            'date_added': self.date_added,
            'userUID': self.userUID,
            'title': self.title,
            'description': self.description,
            'tasks': [task.serialize() for task in self.tasks]
        }
    
class Task(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    date_added = db.Column('date_added', db.Date, default=datetime.utcnow)
    title = db.Column('title', db.Text)
    description = db.Column('description', db.Text)
    project_id = db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
    project = relationship("Project", back_populates="tasks")
    status = db.Column('status', db.Text, default='pending')

    def serialize(self):
        return {
            'id': self.id,
            'date_added': self.date_added,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'project_id': self.project_id
        }
