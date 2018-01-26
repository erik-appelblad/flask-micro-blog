import uuid

import datetime

from src.common.database import Database


class Post(object):
    def __init__(self, blog_id, title, content, category, author, date=datetime.datetime.utcnow(), _id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.category = category
        self.author = author
        self._id = uuid.uuid4().hex if _id is None else _id
        self.date = date

    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='posts', query={'_id': id})
        return cls(**post_data)

    @staticmethod
    def from_blog_id(id):
        return [post for post in Database.find('posts', query={'blog_id': id})]

    def save_to_mongo(self):
        Database.insert(collection='posts',
                        data=self.json())

    def json(self):
        return {
            '_id': self._id,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'category': self.category,
            'title': self.title,
            'date': self.date
        }

    def __str__(self):
        return "Title: {}\nContent: {}\nAuthor: {}".format(self.title, self.content, self.author)
