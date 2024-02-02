from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import requests
import ast
import csv

my_host = "database-1.c32yscgymlt6.us-east-1.rds.amazonaws.com"
my_database = "db1"
my_user = "evantao"
my_password = "rubyonrails"

countries = set()

# Executes the SQL query according to the host, database, user and password
def execute_query(city, country, month, year, temperature, humidity, host, database, user, password):
    try: 
        connection = mysql.connector.connect(host=host, database=database, user=user, password=password)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            try: 
                sql_query = "INSERT INTO Country (Name, Country, Month, Year, Temp, Humidity) VALUES ('{}', '{}', {}, {}, {}, {})".format(city, country, month, year, temperature, humidity)
                cursor.execute(sql_query)
                connection.commit()
                print("Successfully executed {}".format(sql_query))
                cursor.close()
                connection.close()
            except:
                print("Error executing {}".format(sql_query))
    except Error as e:
        print("Error while connecting to MySQL", e)

def insert_country(country_name):
    if country_name not in countries:
        insert("INSERT INTO Country (Name, Weather) VALUES ('{}', 'wet')".format(country_name))
        country.add(country_name)

country_row = 5

with open("medalists.csv", "rb") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        insert_country(row[country_row])
