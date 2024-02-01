from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import requests
import ast

locations = [("Athens", "Greece"), ("London", "UK"), 
            ("Paris", "France"), ("Istanbul", "Turkey"),
            ("Stockholm", "Sweden"), ("Amsterdam", "Netherlands"),
            ("Berlin", "Germany"), ("Helsinki", "Finland"),
            ("Melbourne", "Australia"), ("Rome", "Italy"),
            ("Seoul", "South-Korea"), ("Barcelona", "Spain"),
            ("Beijing", "China")]
years = (2012, 2013)
months = (1, 3)

def generate_settings(locations, start_year, end_year, start_month, end_month): 
    settings = []
    for l in locations:
        for y in range(start_year, end_year):
            for m in range(start_month, end_month):
                settings.append((l, (m, y)))
    return settings

def get_html_page(city, country, year, month):
    page = requests.get("https://www.timeanddate.com/weather/{}/{}/historic?month={}&year={}".format(country, city, month, year))
    return page.content

def get_temperature_and_humidity(city, country, year, month): 
    html_doc = get_html_page(city, country, year, month)
    soup = BeautifulSoup(html_doc, "html.parser")
    block = soup.find("th", text="Average")
    if block is not None:
        value = block.parent
        if value is not None:
            temperature = value.find("td").text[:-3]
            humidity = value.find("td", {"class": "sep"}).text[:-1]
            return (temperature, humidity)
        else:
            print("Page has no HTML parent")
    else:
        print("Page has no temperature and humidity section")
    return {}

def insert(connection, sql):
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
            print("Connected to MySQL database")
            cursor = connection.cursor()
    except Error as e:
        print("Error while connecting to MySQL", e)

    locations_dates = generate_settings(locations, years[0], years[1], months[0], months[1])
    for (city, country), (year, month) in locations_dates:
        temperature, humidity = get_temperature_and_humidity(city, country, year, month)
        insert("INSERT INTO Weather (City, Country, Month, Year, Temp, Humidity) VALUES ('{}', '{}', {}, {}, {}, {})".format(city, country, month, year, val["temperature"], val["humidity"]))
    connection.close()