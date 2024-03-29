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
event_column_1 = 2
event_column_2 = 3
event_column_3 = 7

# Returns all events in the csv file as a set
def generate_options(file): 
    options = set()
    with open(file, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            options.add("{} | {} | {}".format(row[event_column_1], 
                                              row[event_column_2], 
                                              row[event_column_3]))
    return options

# Executes the SQL query according to the event, host, database, user and password
def execute_query(event, host, database, user, password):
    try: 
        connection = mysql.connector.connect(host=host, 
                                             database=database, 
                                             user=user, 
                                             password=password)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            try: 
                sql_query = "INSERT INTO Event (Name) VALUES ('{}')".format(event)
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
    events = generate_options(file)
    for my_event in events:
        execute_query(my_event, my_host, my_database, my_user, my_password)
