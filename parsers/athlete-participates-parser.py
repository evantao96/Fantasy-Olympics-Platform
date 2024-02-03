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
athlete_column = 4
medal_column = 9

medal_values = {"Gold": 3, "Silver": 2, "Bronze": 1}

# Returns all events in the csv file as a set
def generate_options(file): 
    options = set()
    with open(file, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            options.add(("{} | {} | {}".format(row[event_column_1], 
                                               row[event_column_2], 
                                               row[event_column_3]), row[athlete_column], row[medal_column]))
    return options

# Executes the SQL query according to the event, host, database, user and password
def execute_query(event, athlete, medal_value, host, database, user, password):
    try: 
        connection = mysql.connector.connect(host=host, 
                                             database=database, 
                                             user=user, 
                                             password=password)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            try:
                sql_query_1 = "SELECT ID FROM Event WHERE Name = '{}'".format(event)
                sql_query_2 = "SELECT ID FROM Athlete WHERE Name = '{}'".format(athlete)
                sql_query_3 = "SELECT e.ID, a.ID, {} FROM ({}) AS e CROSS JOIN ({}) AS a".format(medal_value, sql_query_1, sql_query_2)
                sql_query_4 = "INSERT INTO Athlete_Participates (Event_ID, Athlete_ID, Medal) {}".format(sql_query_3)

                cursor.execute(sql_query_4)
                connection.commit()
                print("Successfully executed {}".format(sql_query_4))
                cursor.close()
                connection.close()
            except:
                print("Error executing {}".format(sql_query_4))
    except Error as e:
        print("Error while connecting to MySQL", e)

# Main method
if __name__ == "__main__":
    athletes_participates = generate_options(file)
    for my_event, my_athlete, my_medal in athletes_participates:
        execute_query(my_event, my_athlete, medal_values[my_medal], my_host, my_database, my_user, my_password)
