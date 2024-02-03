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

# Returns all combinations of locations, years and months as a list of tuples
def generate_options(locations, start_year, end_year, start_month, end_month): 
    options = []
    for l in locations:
        for y in range(start_year, end_year):
            for m in range(start_month, end_month):
                options.append((l, (y, m)))
    return options

# Returns the Wikipedia page of the athlete
def get_html_page(first_name, last_name):
    url = "https://en.wikipedia.org/wiki/{}_{}".format(first_name, last_name)
    page = requests.get(url)
    return page.content

# Gets the Wikipedia bio of the athlete
def get_bio(first_name, last_name): 
    html_doc = get_html_page(first_name, last_name)
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
        print("Page has no bio section")
    return {}

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
    names = generate_options(locations, years[0], years[1], months[0], months[1])
    for my_first_name, my_last_name in names:
        my_bio = get_bio(my_first_name, my_last_name)
        execute_query(my_bio, my_host, my_database, my_user, my_password)


    def __get_data(self, aid, firstname, lastname):
        html_doc = self.__get_html(firstname, lastname)
        soup = BeautifulSoup(html_doc, 'html.parser')        
        if soup.find("table", class_='infobox vcard') is None:
            if soup.find("table", class_='infobox') is None: 
                table = 'N/A'
            else: 
                if soup.find("table", class_='infobox').findNextSibling('p') is None: 
                    table = 'N/A'
                else:     
                    table = soup.find("table", class_='infobox').findNextSibling("p").text.split(".")[0:1]
                    table = table[0]
                    table = table + "."
        else: 
            if soup.find("table", class_='infobox vcard').findNextSibling('p') is None: 
                table = 'N/A'
            else: 
                table = soup.find("table", class_='infobox vcard').findNextSibling("p").text.split(".")[0:1]
                table = table[0]
                table = table + "."

        print aid, table
        return aid, table

def remove_accents(data): 
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters).lower()


if __name__ == "__main__":
            
    athlete_names = []
    cursor = db.cursor()
    try: 
        cursor.execute("Select id, name from Athlete;")
        db.commit()
        
        for aname in cursor: 
            aid = aname[0]
            aname_arr = aname[1].split(", ")
            lastname = aname_arr[0]

            if len(aname_arr) > 1:
                firstname = aname_arr[1]
            else: 
                firstname = ""

            firstname = remove_accents(firstname.decode('utf-8'))
            firstname = firstname.capitalize()
            lastname = remove_accents(lastname.decode('utf-8'))
            lastname = lastname.capitalize()

            athlete_names.append((aid, firstname,lastname))
    
            
