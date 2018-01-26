import uuid

from src.common.database import Database


class About(object):
    def __init__(self, name, description, user_id, _id = uuid.uuid4().hex):
        self.name = name
        self.description = description
        self.user_id = user_id
        self._id = _id

    @classmethod
    def get_by_user_id(cls, user_id):
        data = Database.find_one('abouts', {"user_id": user_id})
        if data is not None:
            return cls(**data)

    def json(self):
        return {
            "name": self.name,
            "description": self.description,
            "user_id": self.user_id
        }

    def save_to_mongo(self):
        Database.insert("abouts", self.json())
