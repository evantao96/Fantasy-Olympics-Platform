from httplib2 import Http
from bs4 import BeautifulSoup
import MySQLdb
import ast



class WeatherParser():

    def __init__(self, locations_dates):
        self.locations_dates = locations_dates

    def parse(self):
        result = dict()

        i = 0
        n = len(self.locations_dates)

        for location, date in self.locations_dates:
            if i % (n/100) == 0:
                print "{} done".format(float(i)/n*100)
            # print "{} {}".format(location, date)
            result[(location, date)] = self.__get_data(location, date)
            i += 1

        return result

    def __get_html(self, location, date):
        city, state = location
        month, day, year = date

        h = Http(".cache")

        _, html_doc = h.request("http://www.wunderground.com/cgi-bin/findweather/getForecast?airportorwmo=query&historytype=DailyHistory&backurl=%2Fhistory%2Findex.html&code={}%2C+{}&month={}&day={}&year={}".format(city, state, month, day, year),
                                "GET")

        return html_doc

    def __get_data(self, location, date):
        html_doc = self.__get_html(location, date)

        soup = BeautifulSoup(html_doc, 'html.parser')

        # table = soup.find(id='historyTable').tbody

        span = soup.find("span", text="Max Temperature")

        if span is not None:
            value = span.parent.next_sibling.next_sibling.find(class_="wx-value")
            if value is not None:
                temperature = value.text

                span = soup.find("span", text="Average Humidity")

                if span is not None:
                    humidity = span.parent.next_sibling.next_sibling.text

                    data = dict()

                    if humidity.isdigit():
                        data["temperature"] = temperature
                        data["humidity"] = humidity

                        return data

        return None

db = MySQLdb.connect(
        port=3306,
        user="apoth",
        passwd="susandavidson",
        db="olympics",
        host="cis550project-mysql.cbhtjg5oqf7i.us-east-2.rds.amazonaws.com"
)

locations = [("Athens", "Greece"), ("London", "United Kingdom"), 
            ("Paris", "France"), ("St Louis", "United States"),
            ("Stockholm", "Sweden"), ("Amsterdam", "Netherlands"),
            ("Berlin", "Germany"), ("Helsinki", "Finland"),
            ("Melbourne", "Australia"), ("Rome", "Italy"),
            ("Seoul", "South Korea"), ("Barcelona", "Spain"),
            ("Beijing", "China")]

def insert(sql):
    """
    Executes SQL command, provided as input as a string
    """
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        print sql
    except:
        print "exception"
    finally:
        cursor.close()

if __name__ == "__main__":
    locations_dates = []
    for location in locations:
        for month in [1, 6]:
            for day in xrange(1, 29):
                date = (month, day, 2013)
                locations_dates.append((location, date))
    # w = WeatherParser([(("Athens", "Greece"), (1, 24, 2015))])
    w = WeatherParser(locations_dates)
    data = w.parse()
    print data

    for key, val in data.iteritems():
        if val is not None and "humidity" in val:
            location, date = key
            city, country = location
            month, day, year = date
            insert("INSERT INTO Weather (City, Country, Day, Month, Year, Temp, Humidity) VALUES ('{}', '{}', {}, {}, {}, {}, {})".format(city, country, day, month, year, val["temperature"], val["humidity"]))
