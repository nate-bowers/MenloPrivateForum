from sqlalchemy import ForeignKey, Column, INTEGER, TEXT
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

#Classes
class User(Base):
    __tablename__ = "users"

    # Columns
    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)
    #a user has a list of the posts they have upvoted
    upvotes = relationship("Upvote", back_populates="user")

    # Constructor
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Post(Base):
    __tablename__ = "posts"

    title = Column("title", TEXT, nullable=False)
    topic = Column("topic", TEXT, nullable=False)
    content = Column("content", TEXT, nullable=False)
    user_id = Column("user_id", TEXT, nullable=False)
    id = Column("id", INTEGER, primary_key=True, autoincrement=True)
    time = Column("time", TEXT, nullable=False)
    #a post has a list of its upvoted and the users that have upvoted it
    upvotes = relationship("Upvote", back_populates="post")
    upvoters = relationship("User", secondary="upvotes", primaryjoin="Post.id == Upvote.post_id", secondaryjoin="User.username == Upvote.upvoter_username", backref="upvoted_posts")

    # Constructor
    def __init__(self, title, topic, content, user_id):
        self.title = title
        self.topic = topic
        self.content=content
        self.user_id = user_id
        self.time = datetime.now()

class Upvote(Base):
    __tablename__ = 'upvotes'

    post_id = Column(INTEGER, ForeignKey('posts.id'))
    upvoter_username = Column(TEXT, ForeignKey('users.username'))
    id = Column(INTEGER, primary_key=True)

    #An upvote has access to the users who upvoted it and the post that is upvoted
    post = relationship('Post', back_populates='upvotes')
    user = relationship('User', back_populates='upvotes')

    def __init__(self, post=None, user=None):
        self.post_id = post
        self.upvoter_username = user