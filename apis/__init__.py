from flask_restx import Api

from .createdb.endpoints import api as createdb_api
from .sampledata.endpoints import api as sampledata_api

api = Api(
    title="CODE TEST RESTX APIs",
    version="1.0",
    description="This is code test",
)

api.add_namespace(createdb_api, path="/api/v1")
api.add_namespace(sampledata_api, path="/api/v1")
