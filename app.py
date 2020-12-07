from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from Config import Config
from extensions import db

from models.worker import Workers
from resources.tool import ToolListResource, ToolResource, ToolPublishResource

from resources.worker import WorkerListResource
from resources.inventory import InventoryListResource, InventoryResource, InventoryPublishResource


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()

    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)


def register_resources(app):
    api = Api(app)


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000, debug=True)
