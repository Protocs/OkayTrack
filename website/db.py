from .app import db

task_tags_association = db.Table(
    "tasks_tags",
    db.Column("task_id", db.Integer, db.ForeignKey("task.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"))
)

task_categories_association = db.Table(
    "task_categories",
    db.Column("task_id", db.Integer, db.ForeignKey("task.id")),
    db.Column("category_id", db.Integer, db.ForeignKey("category.id"))
)


class User(db.Model):
    name = db.Column(db.String(20), primary_key=True)
    alice_id = db.Column(db.String(64), nullable=True)
    role = db.Column(db.String(5), default="user")
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<User('{self.username}')>"

    @staticmethod
    def get_by_username(username):
        return User.query().filter_by(name=username).first()


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

    author = db.relationship("User", backref="tasks")
    tags = db.relationship("Tag", secondary=task_tags_association, backref=db.backref("tasks", lazy=True))
    categories = db.relationship("Category", secondary=task_categories_association,
                                 backref=db.backref("tasks", lazy=True))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    username = db.Column(db.String(20), db.ForeignKey("user.name"))
    comment = db.Column(db.Text)


db.create_all()
