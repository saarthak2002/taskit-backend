from app import db
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy_utils.types.ts_vector import TSVectorType

class UserInfo(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    userUID = db.Column('userUID', db.Text, unique=True)
    username = db.Column('username', db.Text, unique=True)
    firstName = db.Column('firstName', db.Text)
    lastname = db.Column('lastName', db.Text)

    username_tsv = db.Column(
        TSVectorType("username", regconfig="english"),
        db.Computed("to_tsvector('english', \"username\")", persisted=True)
    )

    __table_args__ = (
        db.Index("idx_userinfo_username_tsv", username_tsv, postgresql_using="gin"),
    )

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
    task_categories = relationship("TaskCategory", back_populates="project")

    def serialize(self):
        return {
            'id': self.id,
            'date_added': self.date_added,
            'userUID': self.userUID,
            'title': self.title,
            'description': self.description,
            'tasks': [task.serialize() for task in self.tasks],
            'task_categories': [task_category.serialize() for task_category in self.task_categories]
        }
    
class Task(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    date_added = db.Column('date_added', db.Date, default=datetime.utcnow)
    title = db.Column('title', db.Text)
    description = db.Column('description', db.Text)
    project_id = db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
    project = relationship("Project", back_populates="tasks")
    status = db.Column('status', db.Text, default='pending')
    task_category_name = db.Column('task_category_name', db.Text, default='None')
    task_category_color = db.Column('task_category_color', db.Text, default='#bab5b5')
    created_by = db.Column('created_by', db.Text, default=None)
    completed_at_time = db.Column('completed_at_time', db.Text, default=None)
    completed_by = db.Column('completed_by', db.Text, default=None)

    def serialize(self):
        return {
            'id': self.id,
            'date_added': self.date_added,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'project_id': self.project_id,
            'task_category_name': self.task_category_name,
            'task_category_color': self.task_category_color,
            'completed_at_time': self.completed_at_time,
            'completed_by': self.completed_by,
            'created_by': self.created_by
        }
    
class TaskCategory(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Text, nullable=False)
    color = db.Column('color', db.Text, nullable=False)
    project = relationship("Project", back_populates="task_categories")
    project_id = db.Column('project_id', db.Integer, db.ForeignKey('project.id'))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'project_id': self.project_id
        }
  
class Collaborator(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    project_id = db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
    project = relationship("Project")
    userUID = db.Column('userUID', db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'userUID': self.userUID
        }