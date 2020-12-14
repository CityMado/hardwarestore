from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from Config import Config
from extensions import db, jwt

from resources.worker import WorkerListResource, WorkerResource, MeResource
from resources.token import TokenResource
from resources.tool import ToolListResource, ToolResource, ToolPublishResource
from resources.sale import SaleListResource, SaleResource, SalePublishResource


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
    jwt.init_app(app)


def register_resources(app):
    api = Api(app)

    api.add_resource(WorkerListResource, '/workers')
    api.add_resource(WorkerResource, '/workers/<string:username>')
    api.add_resource(MeResource, '/me')

    api.add_resource(TokenResource, '/token')

    api.add_resource(ToolListResource, '/tools')
    api.add_resource(ToolResource, '/tools/<int:tool_id>')
    api.add_resource(ToolPublishResource, '/tools/<int:tool_id>/publish')

    api.add_resource(SaleListResource, '/sales')
    api.add_resource(SaleResource, '/sales/<int:sale_id>')
    api.add_resource(SalePublishResource, '/tools/<int:sale_id>/publish')

if __name__ == '__main__':
    app = create_app()
    app.run(port=5000, debug=True)
