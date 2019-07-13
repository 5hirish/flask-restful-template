from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restplus import Api

api = Api(version='1.0')
sql_db = SQLAlchemy()
migrate = Migrate()