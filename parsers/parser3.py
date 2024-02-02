from httplib2 import Http
from bs4 import BeautifulSoup
import MySQLdb
import unicodedata
import string

class WikiParser():


    def __init__(self, names):
        self.names = names

    def parse(self):
        result = []

        for aid, firstname, lastname in self.names:            
            result.append(self.__get_data(aid, firstname, lastname))

        return result

    def __get_html(self, firstname, lastname):
        
        h = Http(".cache")
        if firstname == "":
            _, html_doc = h.request("https://en.wikipedia.org/wiki/{}".format(lastname),"GET")
        else: 
            _, html_doc = h.request("https://en.wikipedia.org/wiki/{}_{}".format(firstname, lastname),"GET")
        return html_doc

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

db = MySQLdb.connect(
        port=3306,
        user="apoth",
        passwd="susandavidson",
        db="olympics",
        host="cis550project-mysql.cbhtjg5oqf7i.us-east-2.rds.amazonaws.com")

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
        
    finally:
        cursor.close()
        w = WikiParser(athlete_names)
        data = w.parse()

        for aid, val in data:
            insertstr = "Update Athlete set bio = '{}' where id={};".format(val,aid) 
            print insertstr
            insert(insertstr)
            
