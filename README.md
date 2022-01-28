
# Sample Test-API
This is a sample APIs , written in Flask and Flask-RESTX
[For more information regarding RESTX. Click here.](https://flask-restx.readthedocs.io/en/latest/index.html)

Introduction
------------
This is a test code written in Flask and RESTX as per the following requirements

Expose the sample dataset through a single generic HTTP API endpoint, which is capable of filtering, grouping and sorting.
Dataset represents performance metrics (impressions, clicks, installs, spend, revenue) for a given date, advertising channel, country and operating system.
Dataset is expected to be stored and processed in a relational database.
Client of this API should be able to:

- Filter by time range (date_from+date_to is enough), channels, countries, operating systems
- Group by one or more columns: date, channel, country, operating system
- Sort by any column in ascending or descending order
- See derived metric CPI (cost per install) which is calculated as cpi = spend / installs


Installing Project Dependencies
----- 
[This project uses Flask and Python 3.8 for virtual environment management. Its assumed that vistural enviourment is up and running by python3 -m venv testcodeenv ]

Requirment could be installed as

`pip -r install requirements.txt`

Running the application
-----

From the root of this project enter the following terminal command:

`python app.py`


Swagger
-----
This project will run in swagger ui.  

[For more information regarding swagger. Click here.](https://swagger.io/)

You can run the swagger to excute the end-point. like

`http://192.168.18.64:5000`


Rest Api 
-----
All API end points will be exposed through swagger.