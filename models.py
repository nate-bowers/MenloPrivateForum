
from sqlalchemy import ForeignKey, Column, INTEGER, TEXT
from sqlalchemy.orm import relationship
from database import Base

#Classes
class User(Base):
    __tablename__ = "users"

    # Columns
    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)

    # Constructor
    def __init__(self, username, password):
        # id auto-increments
        self.username = username
        self.password = password
class Post(Base):
    __tablename__ = "posts"

    title = Column("title", TEXT, nullable=False)
    topic = Column("topic", TEXT, nullable=False)
    content = Column("content", TEXT, nullable=False)
    user_id = Column("user_id", TEXT, nullable=False)
    id = Column("id", INTEGER, primary_key=True, autoincrement=True)

    # Constructor
    def __init__(self, title, topic, content, user_id):
        # id auto-increments
        self.title = title
        self.topic = topic
        self.content=content
        self.user_id = user_id
        