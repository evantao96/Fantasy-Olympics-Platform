from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import requests
import ast

my_host = "database-1.c32yscgymlt6.us-east-1.rds.amazonaws.com"
my_database = "db1"
my_user = "evantao"
my_password = "rubyonrails"
locations = [("Athens", "Greece"), ("London", "UK"), 
            ("Paris", "France"), ("Istanbul", "Turkey"),
            ("Stockholm", "Sweden"), ("Amsterdam", "Netherlands"),
            ("Berlin", "Germany"), ("Helsinki", "Finland"),
            ("Melbourne", "Australia"), ("Rome", "Italy"),
            ("Seoul", "South-Korea"), ("Barcelona", "Spain"),
            ("Beijing", "China")]
years = (2012, 2013)
months = (1, 13)

# Returns all combinations of locations, years and months as a list of tuples
def generate_settings(locations, start_year, end_year, start_month, end_month): 
    settings = []
    for l in locations:
        for y in range(start_year, end_year):
            for m in range(start_month, end_month):
                settings.append((l, (y, m)))
    return settings

# Returns the timeanddate.com page of the city, country, year and month
def get_html_page(city, country, year, month):
    url = "http://timeanddate.com/weather/{}/{}/historic?month={}&year={}".format(country.lower(), city.lower(), month, year)
    page = requests.get(url)
    return page.content

# Gets the temperature and humidity of the city, country during the year, month
def get_temperature_and_humidity(city, country, year, month): 
    html_doc = get_html_page(city, country, year, month)
    soup = BeautifulSoup(html_doc, "html.parser")
    #print(soup.prettify())
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

# Executes the SQL query according to the host, database, user and password
def execute_query(sql_query, host, database, user, password):
    try: 
        connection = mysql.connector.connect(host=host, database=database, user=user, password=password)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            try: 
                cursor.execute(sql_query)
                connection.commit()
                print("Successfully executed {}".format(sql_query))
                cursor.close()
                connection.close()
            except:
                print("Error executing {}".format(sql_query))
    except Error as e:
        print("Error while connecting to MySQL", e)

if __name__ == "__main__":
    locations_dates = generate_settings(locations, years[0], years[1], months[0], months[1])
    for (city, country), (year, month) in locations_dates:
        temperature, humidity = get_temperature_and_humidity(city, country, year, month)
        query = "INSERT INTO Weather (City, Country, Month, Year, Temp, Humidity) VALUES ('{}', '{}', {}, {}, {}, {})".format(city, country, month, year, temperature, humidity)
        execute_query(query, my_host, my_database, my_user, my_password)