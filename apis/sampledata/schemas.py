from flask_restx import fields
from . import api

sampledata = api.model(
    "SampleData",
    {
        "id": fields.Integer(),
        "date": fields.String(),
        "channel": fields.String(),
        "country": fields.String(),
        "os": fields.String(),
        "impressions": fields.Integer(),
        "clicks": fields.Integer(),
        "installs": fields.Integer(),
        "spend": fields.Float(),
        "revenue": fields.Float(),
        "cpi": fields.Float(),
    },
)


get_sample_data = api.model(
    "GetSampleData",
    {
        "status": fields.String(description="ok|nok"),
        "objects": fields.Nested(sampledata, as_list=True),
        "total_rows": fields.Integer(),
    },
)
