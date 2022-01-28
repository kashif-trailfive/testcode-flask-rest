from flask_restx import Resource
from http import HTTPStatus
from . import api
from models import create_database
from models.sample_data import SampleData
from core.utils import success, failure


@api.route("/create_db", endpoint="create-database")
@api.response(404, "Database not created")
class CreateDB(Resource):
    def put(self):
        """
        Populate sample data with dataset.csv at rool folder

        """
        try:
            create_database()
            rows_deleted = SampleData.emty_table()
            rows_added = SampleData.populate_table()
            response_text = {"message": "Database created"}
            return success(response_text, rows_added), HTTPStatus.OK

        except Exception as ex:
            api.logger.error(ex)
            response_text = {"message": "Unable to create/delete database"}
            return failure(response_text), HTTPStatus.BAD_REQUEST
