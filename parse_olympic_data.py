import MySQLdb
import csv

# haven't succeeded in doing this yet
db = MySQLdb.connect(
        port=3306,
        user="apoth",
        passwd="susandavidson",
        db="olympics",
        host="cis550project-mysql.cbhtjg5oqf7i.us-east-2.rds.amazonaws.com"
)

# Globals
events = set()
countries = set()
athletes = set()

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
        db.rollback()
    finally:
        cursor.close()

#these functions will populate the database

def insert_event(event_name):
    if event_name not in events:
        insert("INSERT INTO Event (Name) VALUES ('{}')".format(event_name))
        events.add(event_name)

def insert_country(country_name):
    if country_name not in countries:
        insert("INSERT INTO Country (Name, Weather) VALUES ('{}', 'wet')".format(country_name))
        country.add(country_name)

def insert_athlete(athlete_name, country_name):
    if athlete_name not in athletes:
        cursor = db.cursor()
        try:
            cursor.execute("SELECT Id FROM Country WHERE Name='{}'".format(country_name))
            country_id = cursor.fetchone()
            cursor.close()

            insert("INSERT INTO Athlete (Name, Country_Id) VALUES ('{}', {}".format(athlete_name, country_name))
            athletes.add(athlete_name)
        except:
            print "Error Looking up Country_Id"



def insert_athlete_participates(name, event, medal):
    return

athlete_name_row = 4
country_row = 5
event_row = 7
medal_row = 8


with open("medalists.csv", "rb") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        insert_event(row[event_row])
        insert_country(row[country_row])
        insert_athlete(row[athlete_name_row], row[country_row])
        # insert_athlete_participates(athlete_name_row, event_row, medal_row)
