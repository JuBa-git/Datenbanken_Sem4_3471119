"""kaggleToInflux
    Download csv data from Kaggle and import it into InfluxDB
    * Datasource: https://www.kaggle.com/gpreda/covid-world-vaccination-progress
    * File: country_vaccinations.csv

    Attributes:
        * name: Julian Banzhaf
        * date: 13.05.2021
        * version:  1.0 - free

    TODO:
        rename config_template.py to config.py and set variables to run the code/tests !!!
"""
from config import *
from datetime import datetime
from influxdb import InfluxDBClient
import csv
import os
import sys
import zipfile
# set environ variables before import KaggleApi
# this is only needed if the is no kaggle.json
os.environ["KAGGLE_USERNAME"] = KAGGLE_USERNAME
os.environ["KAGGLE_KEY"] = KAGGLE_KEY
from kaggle.api.kaggle_api_extended import KaggleApi


def getKaggleData(dataset, filename):
    """Download csv data from Kaggle

    :param dataset: name of a dataset in format <owner>/<name>
    :type dataset: str
    :param filename: name of a csv file in the dataset
    :type filename: str

    :return: True if file was downloaded
    :rtype: bool

    >>> getKaggleData("gpreda/covid-world-vaccination-progress", "country_vaccinations.csv" )
    True
    >>> getKaggleData("wrong/dataset", "wrong_file.csv" ) #doctest: +ELLIPSIS
    Error: ...
    False
    """
    try:
        my_api = KaggleApi()
        my_api.authenticate()

        if my_api.dataset_download_file(dataset, filename, path=None, force=True, quiet=True):
            with zipfile.ZipFile(filename + ".zip", "r") as my_zip:
                my_zip.extract(filename)
            os.remove(filename + ".zip")
            return True
    except Exception as e:
        print("Error: ", e)
    return False


def connectInfluxDB(db_name, host, user, passwd):
    """Connect to InfluxDB

    :param db_name: name of the influx database
    :type db_name: str
    :param host: hostname of the influx server
    :type host: str
    :param user: influx username
    :type user: str
    :param passwd: influx user password
    :type passwd: str

    :return: database object if connection was successful
    :rtype: InfluxDBClient or NoneType

    >>> connectInfluxDB(INFLUX_DATABASE, INFLUX_HOST, INFLUX_USER, INFLUX_USER_PASSWORD) #doctest: +ELLIPSIS
    <influxdb.client.InfluxDBClient object at 0x...>
    >>> connectInfluxDB("invalid", "invalid", "invalid", "invalid") is None #doctest: +ELLIPSIS
    Error: ...
    True
    """
    try:
        db = InfluxDBClient(database=db_name, host=host, username=user, password=passwd, port=8086)
        db.ping()
    except Exception as e:
        print("Error: ", e)
        return None
    return db


def insertData(db, filename):
    """Load data from csv into InfluxDB

    :param db: connected influx database
    :param filename: csv file

    :return: True if data was inserted
    :rtype: bool

    >>> insertData(None, None) #doctest: +ELLIPSIS
    Error: ...
    False
    """
    data = []
    try:
        with open(filename) as f:
            c = csv.reader(f, delimiter=',')
            for row in c:
                try:
                    ts = int(datetime.strptime(row[2], "%Y-%m-%d").timestamp())
                    if row[7] != "":
                        row[0] = row[0].replace(" ", "\\ ")
                        line = f'impfungen,country={row[0]} vaccinations={row[7]} {ts}'
                        data.append(line)
                except:
                    pass
        db.drop_measurement("impfungen")
        db.write_points(data, protocol='line', time_precision='s')
        return True
    except Exception as e:
        print("Error: ", e)
    return False


def main():
    """Main program

        :return: 0 if program runs successfully
        :rtype: int
    """
    dataset = "gpreda/covid-world-vaccination-progress"
    filename = "country_vaccinations.csv"
    try:
        db = connectInfluxDB(INFLUX_DATABASE, INFLUX_HOST, INFLUX_USER, INFLUX_USER_PASSWORD)
        getKaggleData(dataset, filename)
        insertData(db, filename)
        return 0
    except Exception as e:
        print("Error: ", e)
    return 1


if __name__ == '__main__':
    sys.exit(main())
