from httplib2 import Http
from bs4 import BeautifulSoup
import MySQLdb
import unicodedata
import string
from unidecode import unidecode

class WikiParser():


    def __init__(self, names):
        self.names = names

    def parse(self):
        result = []

# get each athlete's data and append into list
        for aid, firstname, lastname in self.names:            
            num,desc = self.__get_data(aid, firstname, lastname)
            result.append((num,desc))
            print num,desc
        return result

# parse Wikipedia page
    def __get_html(self, firstname, lastname):
        
        h = Http(".cache")
        if firstname == "":
            _, html_doc = h.request("https://en.wikipedia.org/wiki/{}".format(lastname),"GET")
        else: 
            _, html_doc = h.request("https://en.wikipedia.org/wiki/{}_{}".format(firstname, lastname),"GET")
        return html_doc

# identify athlete bios in Wikipedia pages
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
                    # take first two sentences
                    table = soup.find("table", class_='infobox').findNextSibling("p").text.split(".")[0:2]
                    if table[0] == '': 
                        table = 'N/A'
                    else:
                        if len(table) == 1 or table[1] == '':
                            table = table[0] + '.'
                        else:
                            table = table[0] + '.' + table[1] + '.'
        else: 
            if soup.find("table", class_='infobox vcard').findNextSibling('p') is None: 
                table = 'N/A'
            else: 
                # take first two instances
                table = soup.find("table", class_='infobox vcard').findNextSibling("p").text.split(".")[0:2]
                if table[0] == '': 
                    table = 'N/A'
                else: 
                    if len(table) == 1 or table[1] == '':
                        table = table[0] + '.'
                    else:
                        table = table[0] + '.' + table[1] + '.'
        return aid, table

# connect to project
db = MySQLdb.connect(
        port=3306,
        user="apoth",
        passwd="susandavidson",
        db="olympics",
        host="cis550project-mysql.cbhtjg5oqf7i.us-east-2.rds.amazonaws.com")

# remove accents from bios
def remove_accents(data): 
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters).lower()

def insert(sql):
    """
    Executes SQL command, provided as input as a string
    """
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    finally:
        cursor.close()

if __name__ == "__main__":
            
    athlete_names = []
    cursor = db.cursor()
    try: 
        # get ids and names of Athletes
        cursor.execute("Select id, name from Athlete where bio <> 'N/A' and id > 21700;")
        db.commit()
        
        for aname in cursor:
            # athlete id
            aid = aname[0]
            aname_arr = aname[1].split(", ")
            # last name
            lastname = aname_arr[0]

            # first name
            if len(aname_arr) > 1:
                firstname = aname_arr[1]
            else: 
                firstname = ""

            firstname = remove_accents(firstname.decode('utf-8'))
            firstname = firstname.capitalize()
            lastname = remove_accents(lastname.decode('utf-8'))
            lastname = lastname.capitalize()

            athlete_names.append((aid, firstname,lastname))
        
    finally:
        cursor.close()
        w = WikiParser(athlete_names)
        data = w.parse()

# insert bios into database
        for aid, val in data:
            val = unidecode(val)
            insertstr = """Update Athlete set bio = '{}' where id={};""".format(val.replace("'","''"),aid)      
            print insertstr
            insert(insertstr)
            
