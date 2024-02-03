from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import requests
import ast
import unicodedata
import string

my_host = "database-1.c32yscgymlt6.us-east-1.rds.amazonaws.com"
my_database = "db1"
my_user = "evantao"
my_password = "rubyonrails"

# Returns all athlete first names and last names as a list
def generate_options(host, database, user, password): 
    options = []
    try: 
        connection = mysql.connector.connect(host=host, 
                                             database=database, 
                                             user=user, 
                                             password=password)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            try: 
                sql_query = "SELECT ID, Name FROM Athlete"
                cursor.execute(sql_query)
                print("Successfully executed {}".format(sql_query))
                for c in cursor: 
                    options.append((c[0], c[1]))
                cursor.close()
                connection.close()
            except:
                print("Error executing {}".format(sql_query))
    except Error as e:
        print("Error while connecting to MySQL", e)
    return options

# Returns the Wikipedia page of the athlete
def get_html_page(name):
    url = "https://en.wikipedia.org/wiki/{}".format(name)
    page = requests.get(url)
    return page.content

def remove_accents(data): 
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters or x == "_" or x == "-" )

# Gets the Wikipedia bio of the athlete
def get_bio(name): 
    name_parts = name.split(", ")
    if len(name_parts) > 1: 
        formatted_name = "{}_{}".format(name_parts[1], name_parts[0].lower().capitalize())
    else: 
        formatted_name = name_parts[0].lower().capitalize()
    formatted_name = formatted_name.replace(" ", "_")
    formatted_name = remove_accents(formatted_name)
    html_doc = get_html_page(formatted_name)
    soup = BeautifulSoup(html_doc, "html.parser")
    profile_table = soup.find("table", {"class": "infobox vcard"})
    if profile_table is not None: 
        profile_bio = profile_table.findNextSibling("p").text
        if profile_bio is not None: 
            if len(profile_bio) > 250: 
                profile_bio = profile_bio[:250] + "..."
            return profile_bio
        else:
            print("Page for {} has no bio section".format(formatted_name))
    else:
        print("Page for {} has no table".format(formatted_name))
    return "N/A"

# Executes the SQL query according to the host, database, user and password
def execute_query(bio, athlete_id, host, database, user, password):
    try: 
        connection = mysql.connector.connect(host=host, database=database, user=user, password=password)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            try: 
                sql_query = "UPDATE Athlete SET bio = '{}' WHERE id={}".format(bio, athlete_id)
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
    ids_names = generate_options(my_host, my_database, my_user, my_password)
    for my_athlete_id, my_name in ids_names:
        my_bio = get_bio(my_name)
        execute_query(my_bio, my_athlete_id, my_host, my_database, my_user, my_password)

# if __name__ == "__main__":
            
#     athlete_names = []
#     cursor = db.cursor()
#     try: 
#         cursor.execute("Select id, name from Athlete;")
#         db.commit()
        
#         for aname in cursor: 
#             aid = aname[0]
#             aname_arr = aname[1].split(", ")
#             lastname = aname_arr[0]

#             if len(aname_arr) > 1:
#                 firstname = aname_arr[1]
#             else: 
#                 firstname = ""

#             firstname = remove_accents(firstname.decode('utf-8'))
#             firstname = firstname.capitalize()
#             lastname = remove_accents(lastname.decode('utf-8'))
#             lastname = lastname.capitalize()

#             athlete_names.append((aid, firstname,lastname))
    
            
