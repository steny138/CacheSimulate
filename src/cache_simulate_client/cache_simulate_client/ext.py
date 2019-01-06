from flask_redis import FlaskRedis
from flask_pymongo import PyMongo

mongo = PyMongo()
redis_store = FlaskRedis()
cache = {}