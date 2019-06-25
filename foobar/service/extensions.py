from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restplus import Api

api = Api()
db = SQLAlchemy()
migrate = Migrate()