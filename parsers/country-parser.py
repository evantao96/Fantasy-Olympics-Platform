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
file = "./medalists.csv"
country_column = 5

# Returns all countries in the csv file as a set
def generate_options(file): 
    options = set()
    with open(file, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            options.add(row[country_column])
    return options

# Executes the SQL query according to the country, host, database, user and password
def execute_query(country, host, database, user, password):
    try: 
        connection = mysql.connector.connect(host=host, 
                                             database=database, 
                                             user=user, 
                                             password=password)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            try: 
                sql_query = "INSERT INTO Country (Name) VALUES ('{}')".format(country)
                cursor.execute(sql_query)
                connection.commit()
                print("Successfully executed {}".format(sql_query))
                cursor.close()
                connection.close()
            except:
                print("Error executing {}".format(sql_query))
    except Error as e:
        print("Error while connecting to MySQL", e)

# Main method
if __name__ == "__main__":
    countries = generate_options(file)
    for my_country in countries:
        execute_query(my_country, my_host, my_database, my_user, my_password)
