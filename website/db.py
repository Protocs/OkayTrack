from werkzeug.security import generate_password_hash
import datetime
from .app import db

task_tags_association = db.Table(
    "tasks_tags",
    db.Column("task_id", db.Integer, db.ForeignKey("task.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"))
)


class User(db.Model):
    name = db.Column(db.String(20), primary_key=True)
    alice_id = db.Column(db.String(64), nullable=True)
    role = db.Column(db.String(5), default="user")
    password_hash = db.Column(db.String(128), nullable=False)
    blocked = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User('{self.username}')>"

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(name=username).first()

    @staticmethod
    def get_all():
        return User.query.all()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), db.ForeignKey("user.name"), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    task = db.Column(db.Text, nullable=False)
    deadline = db.Column(db.DateTime)

    performer = db.Column(db.String(20), db.ForeignKey("user.name"), nullable=True)
    priority = db.Column(db.Integer, nullable=True)
    stage = db.Column(db.Integer, nullable=True)
    completed = db.Column(db.Boolean, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)
    category = db.relationship("Category", backref=db.backref("tasks", lazy=True))

    tags = db.relationship("Tag", secondary=task_tags_association, backref=db.backref("tasks", lazy=True))

    @staticmethod
    def get_user_tasks(username):
        return Task.query.filter_by(username=username).all()

    @staticmethod
    def get_delegated_tasks(username):
        return Task.query.filter_by(performer=username).all()

    @staticmethod
    def get_all():
        return Task.query.all()

    @staticmethod
    def get_task_by_id(id, username):
        return Task.query.filter_by(id=id, username=username).first()

    @staticmethod
    def get_late_tasks(username):
        late = []
        for task in Task.get_user_tasks(username):
            task_date = task.deadline
            if task_date < datetime.datetime.now():
                late.append(task)
        return late


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    @staticmethod
    def get_all():
        return Category.query.all()

    @staticmethod
    def get_by_id(id):
        return Category.query.filter_by(id=id).first()

    @staticmethod
    def get_by_name(name):
        return Category.query.filter_by(name=name).first()


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    username = db.Column(db.String(20), db.ForeignKey("user.name"))
    comment = db.Column(db.Text)


db.create_all()
if User.query.filter_by(role="admin").first() is None:
    admin = User(name="admin", role="admin", password_hash=generate_password_hash("password"))
    db.session.add(admin)
    db.session.commit()
