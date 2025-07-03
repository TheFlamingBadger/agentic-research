from mongo_client import get_db

db = get_db()
users = db['users']
print(users.find_one())
