import os
from flask import Flask
from flask_restful import Resource, Api
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from application import workers
from flask_cors import CORS, cross_origin
from flask_security import Security, SQLAlchemySessionUserDatastore
from application.models import User, Role
from flask_caching import Cache


app = None
api = None
celery = None
cache = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.secret_key = 'Secret Key'
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    api = Api(app)
    app.app_context().push()

    # Create celery   
    celery = workers.celery

    # Update with configuration
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"]
    )

    celery.Task = workers.ContextTask


    CORS(app, supports_credentials=True)
    app.config['CORS_HEADERS'] = 'application/json'

    app.app_context().push()
    cache = Cache(app)
    app.app_context().push()
    return app, api, celery, cache

app, api, celery, cache = create_app()

# Import all the controllers so they are loaded
from application.controllers import *


from application.api import *
api.add_resource(UserAPI, "/api/<email>", "/api/adduser")
api.add_resource(ToggleAPI, "/api/togglecard/<card_id>")
api.add_resource(ExportAPI, "/api/export/<user_id>/<list_id>")
api.add_resource(ListAPI, "/api/lists/<user_id>", "/api/createlist/<user_id>", "/api/deletelist/<list_id>", "/api/updatelist/<list_id>")
api.add_resource(CardAPI, "/api/cards/<list_id>", "/api/createcard/<list_id>", "/api/deletecard/<card_id>", "/api/updatecard/<card_id>")

if __name__ == '__main__':
  # Run the Flask app
  app.run()
