from flask_restx import Resource
from http import HTTPStatus
from core.utils import success, failure
from models.sample_data import SampleData
from core.utils import get_filter_fields
from flask import request
from . import api


@api.route("/get_sample_data_list", endpoint="sample-data")
@api.response(404, "Internal server error")
class SampleDataAPI(Resource):
    @api.doc(
        params={
            "sort_by_asc": "Sort by asc date or channel or country or os asc or desc e.g. date, channel, country",
            "sort_by_desc": "Sort by desc date or channel or country or os asc or desc e.g. date, channel, country",
            "group_by": "Group by date or channel or country or os e.g. date, channel, country",
            "country": "The country for which to get the data e.g. US",
            "channel": "The channel for which to get the data e.g. adcolony",
            "os": "The os for which to get the data e.g. android",
            "date_to": "Data in format 2017-05-17 yyyy-mm-dd",
            "date_from": "Data in format 2017-05-17 yyyy-mm-dd",
            "cpi": "To include CPI type YES or NO default YES",
        }
    )
    # @api.marshal_with(schemas.get_sample_data, skip_none=True)
    @api.param("cpi", type="string")
    @api.param("sort_by_desc", type="string")
    @api.param("sort_by_asc", type="string")
    @api.param("group_by", type="string")
    @api.param("os", type="string")
    @api.param("country", type="string")
    @api.param("channel", type="string")
    @api.param("date_to", type="string")
    @api.param("date_from", type="string")
    # @verify_token '''needed to implement'''
    def get(self):
        """
        List all sample data

        """
        try:

            api.logger.info("Get all sample data")
            sampleData = SampleData()
            filtration_fields = get_filter_fields(request)
            query_data, total_rows, error_message = sampleData.filter_all(
                filtration_fields
            )

            if error_message:
                response_text = {"message": error_message}
                return failure(error_message), HTTPStatus.BAD_REQUEST

            if query_data:
                return success(query_data, total_rows), HTTPStatus.OK

            return success(query_data, total_rows), HTTPStatus.OK

        except Exception as ex:
            api.logger.error(ex)
            response_text = {
                "message": "Unable to fectch data, create DB may solve thi problem."
            }
            return failure(response_text), HTTPStatus.BAD_REQUEST
