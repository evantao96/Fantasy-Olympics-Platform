from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import requests
import ast

my_host = "database-1.c32yscgymlt6.us-east-1.rds.amazonaws.com"
my_database = "db1"
my_user = "evantao"
my_password = "rubyonrails"

class dbOlympicsParser():

    def __init__(self, stats):
        self.stats = stats

    def parse(self):
        result = []

        for sport_event,name  in self.stats:
            result.append(self.__get_data(sport_event,name))

        return result

    def __get_html(self, name):
        firstname,lastname = name;

        _, html_doc = h.request("http://databaseolympics.com/players/playerpage.htm?ilkid={}{}01".format(lastname[0:5],firstname[0:3]),
                                "GET")

        return html_doc

    def __get_data(self, sport_event, name):
        html_doc = self.__get_html(name)
        
        sport,event,year = sport_event

        soup = BeautifulSoup(html_doc, 'html.parser')

        resultyr = soup.find("tr", class_="statHead").findNext("a", text=year).findNext("a",text=sport).findNext("a",text=event).findNext("td",class_="cen")
        resultmd = resultyr.text.split(">")
        resultco = resultyr.findNext("a").text
        resultsc = resultyr.findNext("td",class_="rht").text.split(">")

        # medal = soup.find(
       #     "tr", class_="stathead").parent.next_sibling.next_sibling.text

        data = dict()
            data["medal"] = resultmd
            data["country"] = resultco
            data["score"] = resultsc

        return data

def insert(sql):
    """
    Executes SQL command, provided as input as a string
    """
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        print sql
    finally:
        cursor.close()

if __name__ == "__main__":
    locations_dates = []
    for location in locations:
        for year in xrange(1896, 2009, 4):
            locations_dates.append((location, date))
            w = WeatherParser(locations_dates)
            data = w.parse()
            print data

            for key, val in data.iteritems():
                if val is not None:
                    location, date = key
                    city, country = location
            insert("INSERT INTO Event (id, name) VALUES ('{}', '{}')".format(city, country, day, month, year, val["temperature"], val["humidity"]))


if __name__ == "__main__":
    w = dbOlympicsParser([(("Fencing", "Foil, Individual", "1896"), ("Henri", "Callot")), 
                          (("Track & Field", "4x100m Relay Men", "2004"), ("Maurice", "Green"))
                       ])
    data = w.parse()
    print data

