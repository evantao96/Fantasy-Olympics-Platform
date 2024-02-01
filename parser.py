import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import ast

class WeatherParser():

    def __init__(self, locations_dates):
        self.locations_dates = locations_dates

    def parse(self):
        result = dict()

        for location, date in self.locations_dates:
            result[(location, date)] = self.__get_data(location, date)

        return result

    def __get_html(self, location, date):
        city, country = location
        month, year = date
        page = requests.get("https://www.timeanddate.com/weather/{}/{}/historic?month={}&year={}".format(country, city, month, year))
        return page.content

    def __get_data(self, location, date):
        html_doc = self.__get_html(location, date)
        soup = BeautifulSoup(html_doc, 'html.parser')
        span = soup.find("th", text="Average")

        if span is not None:
            value = span.parent
        
            if value is not None:
                temperature = value.find("td").text[:-3]
                humidity = value.find("td", {"class": "sep"}).text[:-1]

                data = dict()

                data["temperature"] = temperature
                data["humidity"] = humidity

                return data

        return None

def insert(sql):
    """
    Executes SQL command, provided as input as a string
    """
    try:
        cursor.execute(sql)
        connection.commit()
        print("Successfully executed {}".format(sql))
    except:
        print("Error executing {}".format(sql))

if __name__ == "__main__":

    try: 
        connection = mysql.connector.connect(host='database-1.c32yscgymlt6.us-east-1.rds.amazonaws.com',
            database='db1',user='evantao',password='rubyonrails')
            
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version", db_Info)
            cursor = connection.cursor()
    except Error as e:
        print("Error while connecting to MySQL", e)

    locations = [("Athens", "Greece"), ("London", "UK"), 
                ("Paris", "France"), ("Istanbul", "Turkey"),
                ("Stockholm", "Sweden"), ("Amsterdam", "Netherlands"),
                ("Berlin", "Germany"), ("Helsinki", "Finalnd"),
                ("Melbourne", "Australia"), ("Rome", "Italy"),
                ("Seoul", "South-Korea"), ("Barcelona", "Spain"),
                ("Beijing", "China")]

    locations_dates = []
    for location in locations:
        for year in range(2014, 2016):
            for month in [1, 6]:
                date = (month, year)
                locations_dates.append((location, date))

    w = WeatherParser(locations_dates)
    data = w.parse()

    for key, val in data.items():
        if val is not None and "humidity" in val:
            location, date = key
            city, country = location
            month, year = date
            insert("INSERT INTO Weather (City, Country, Month, Year, Temp, Humidity) VALUES ('{}', '{}', {}, {}, {}, {})".format(city, country, month, year, val["temperature"], val["humidity"]))
    connection.close()