import yaml
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api

__version__ = '0.1'

api = Api(version=__version__, doc='/doc')
db = SQLAlchemy()

from estocks.es_manager import ESManager

es_manager = ESManager()

def create_app(args=None, yaml_path=None):
    yaml_path = yaml_path if yaml_path else args.yaml_path
    with open(yaml_path, 'r') as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)

    server_yaml = conf['server']

    es_manager.init_from_dict(server_yaml['es_config'])

    app = Flask(__name__)
    app.url_map.strict_slashes = server_yaml['url_map_config']['FLASK_STRICT_SLASHES']
    app.config.from_mapping(**server_yaml['server_config'])

    from estocks import namespaces
    import estocks.models

    api.init_app(app, title=server_yaml['doc_config'])
    db.init_app(app)


    return app
