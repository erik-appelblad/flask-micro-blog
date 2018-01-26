from src.common.database import Database
from src.models.user import User

Database.initialize()

user = User("eappelblad@gmail.com", "badpass")

user.new_blog("My cool blog", "A blog about me")

user.new_post("b54ec636a66b465ebdec8dbaed1a112c", "A day at the shops", "It was shit")
