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
climates = {
'FRA': 'hot',
'GER': 'hot',
'CHN': 'hot',
'JPN': 'hot',
'POL': 'hot',
'ITA': 'dry',
'AUS': 'dry',
'HUN': 'dry',
'ROU': 'dry',
'USA': 'dry',
'SWE': 'cold',
'CAN': 'cold',
'RUS': 'cold',
'NOR': 'cold',
'URS': 'cold',
'KOR': 'wet',
'DEN': 'wet',
'ESP': 'wet',
'GBR': 'wet',
'NED': 'wet',
}

# Returns all countries in the csv file as a set
def generate_options(file): 
    options = set()
    with open(file, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            options.add(row[country_column])
    return options

def get_climate(country_id):
    if country_id in climates: 
        return climates[country_id]
    else:
        return "N/A"

# Executes the SQL query according to the country ID, host, database, user and password
def execute_query(country_id, climate, host, database, user, password):
    try: 
        connection = mysql.connector.connect(host=host, 
                                             database=database, 
                                             user=user, 
                                             password=password)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            try: 
                sql_query = "INSERT INTO Country (ID, Climate) VALUES ('{}', '{}')".format(country_id, climate)
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
    for my_country_id in countries:
        my_climate = get_climate(my_country_id)
        execute_query(my_country_id, my_climate, my_host, my_database, my_user, my_password)
