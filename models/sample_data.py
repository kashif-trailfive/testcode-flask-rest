from typing import Tuple
from core.utils import validate_date, calculate_cpi
from flask_sqlalchemy import BaseQuery
from dataclasses import dataclass
from sqlalchemy import asc, desc, inspect
from sqlalchemy.sql import text
from . import db
from sqlalchemy.orm import column_property
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import desc


@dataclass
class SampleData(db.Model):

    __tablename__ = "sample_data"

    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.String(255), nullable=False)
    channel = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    os = db.Column(db.String(255), nullable=False)
    impressions = db.Column(db.Integer, nullable=True)
    clicks = db.Column(db.Integer, nullable=True)
    installs = db.Column(db.Integer, nullable=True)
    spend = db.Column(db.Float, nullable=True)
    revenue = db.Column(db.Float, nullable=True)

    @hybrid_property
    def cpi(self):
        if self.spend is not None and self.clicks is not None:
            return self.spend / self.clicks
        else:
            return 0

    @cpi.expression
    def cpi(cls):
        if cls.spend is not None and cls.clicks is not None:
            return cls.spend / cls.clicks
        else:
            return 0

    def toDict(self):
        """
        Convert data object to dictionary
        """
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def make_responce(self, query_data: list, is_cpi: str) -> list:
        """
        Making resonce in JSON
        """

        final_data = []
        for single_row in query_data:
            dictionary = single_row.toDict()

            if is_cpi.lower().strip() == "yes":
                dictionary["CPI"] = calculate_cpi(
                    dictionary["spend"], dictionary["installs"]
                )

            final_data.append(dictionary)

        if is_cpi.lower().strip() == "yes":
            final_data = sorted(final_data, key=lambda i: (i["CPI"]), reverse=True)

        return final_data

    @staticmethod
    def emty_table():

        try:
            num_rows_deleted = db.session.query(SampleData).delete()
            db.session.commit()
            return num_rows_deleted
        except:
            db.session.rollback()
            return 0

    @staticmethod
    def populate_table():
        """
        Populate the database with sample data from dataset.csv at root.

        """
        with open("dataset.csv", "r") as f:
            record_added = 0
            next(f)
            for line in f:
                line = line.strip()
                line = line.split(",")
                record_added += 1
                print(line)
                sample_data = SampleData(
                    date=line[0],
                    channel=line[1],
                    country=line[2],
                    os=line[3],
                    impressions=line[4],
                    clicks=line[5],
                    installs=line[6],
                    spend=line[7],
                    revenue=line[8],
                )
                db.session.add(sample_data)
                db.session.commit()

            return record_added

    def validate_argument_list(self, argument_list: str) -> bool:
        return_val = []
        argumnets = argument_list.split(",")
        for argument in argumnets:
            return_val.append(argument.strip() in self.__table__.columns.keys())
        return False not in return_val

    def filter_by_date(
        self, query: BaseQuery, date_from: str, date_to: str
    ) -> BaseQuery:
        """
        Get date filtered on the basis of start date and end date

        """
        error_message = ""
        if (
            validate_date(date_from) == "DateError"
            or validate_date(date_to) == "DateError"
        ):
            error_message = "Incorrect Date Format"

        if validate_date(date_from) == "OkDate" and validate_date(date_to) == "OkDate":
            query = query.filter(
                SampleData.date >= date_from, SampleData.date <= date_to
            )

        if validate_date(date_from) == "OkDate" and validate_date(date_to) == "NoDate":
            query = query.filter(SampleData.date >= date_from)

        if validate_date(date_from) == "NoDate" and validate_date(date_to) == "OkDate":
            query = query.filter(SampleData.date <= date_to)

        return query, error_message

    def group_by(self, query: BaseQuery, group_by: str) -> BaseQuery:
        """
        Get group by data on the basis of group by argument
        """
        error_message = ""
        if self.validate_argument_list(group_by):
            query = query.group_by(text(group_by))
        else:
            error_message = "Incorrect column name(s) - Group By"

        return query, error_message

    def order_by(self, query: BaseQuery, order_by: str, attributes: str) -> BaseQuery:
        """
        Get order by data on the basis of order by argument
        """
        error_message = ""
        if self.validate_argument_list(attributes):
            if order_by == "asc":
                query = query.order_by(asc(text(attributes)))
            elif order_by == "desc":
                query = query.order_by(desc(text(attributes)))
        else:
            error_message = "Incorrect column names - Order_By " + order_by

        return query, error_message

    def filter_by_data(
        self, query: BaseQuery, sampledata: object, filter_value: str
    ) -> BaseQuery:
        """
        Get filtered data on the basis of filter argument
        """
        error_message = ""
        query = query.filter(sampledata == filter_value)

        return query, error_message

    def filter_all(self, filtration_fields: list) -> Tuple[list, int, str]:

        query = db.session.query(SampleData)

        error_message = ""

        if filtration_fields["date_from"] or filtration_fields["date_to"]:
            query, error_message = self.filter_by_date(
                query, filtration_fields["date_from"], filtration_fields["date_to"]
            )

        if filtration_fields["channel"]:
            query, error_message = self.filter_by_data(
                query, SampleData.channel, filtration_fields["channel"]
            )

        if filtration_fields["country"]:
            query, error_message = self.filter_by_data(
                query, SampleData.country, filtration_fields["country"]
            )

        if filtration_fields["os"]:
            query, error_message = self.filter_by_data(
                query, SampleData.os, filtration_fields["os"]
            )

        if filtration_fields["group_by"]:
            query, error_message = self.group_by(query, filtration_fields["group_by"])

        if filtration_fields["sort_by_asc"]:
            query, error_message = self.order_by(
                query, "asc", filtration_fields["sort_by_asc"]
            )

        if filtration_fields["sort_by_desc"]:
            query, error_message = self.order_by(
                query, "desc", filtration_fields["sort_by_desc"]
            )

        total_rows = query.count()
        filtered_data = query.all()

        filtered_data = self.make_responce(filtered_data, filtration_fields["cpi"])

        return filtered_data, total_rows, error_message
