# creati o baza de date numita orase care face tabelul orase
#cititi din fisierul...csv si scrie in baza de date 
#o functie care ia ca parametru tara si returneaza toate orasele din acea tara sub forma unei liste
import mysql.connector ,csv

with open("psw.txt","r") as file:
    PASSWORD = file.readline()

class ConnectionToDatabase():
    """Cu ajutorl acestei clase instantiem conexiunea la baza de date si modificam baza de date."""
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.mydb = mysql.connector.connect(
            user = 'root',
            host = 'localhost',
            password = PASSWORD,
            database = 'orase'
        )
        self.mycursor = self.mydb.cursor()
    
    def execute_insert_query(self, query: str):
        self.mycursor.execute(query)
        self.mydb.commit()
        
    def execute_select_query(self, query: str):
        self.mycursor.execute(query)
        return self.mycursor.fetchall()
    
    def execute_update_query(self, query: str):
        self.mycursor.execute(query)
        self.mydb.commit()
    
    def execute_delete_query(self, query: str):
        self.mycursor.execute(query)
        self.mydb.commit()
        
my_conn = ConnectionToDatabase()

def copiaza_cvs_in_baza():
    with open("curs38\worldcities.csv","r",encoding = "UTF-8") as my_csv_file:
        content = csv.reader(my_csv_file)
        for index,row in enumerate(content):
            if index != 0:
                if not row[9]:
                    row[9] = 0
                query = f"""INSERT INTO orase values(Null,"{row[1]}","{row[4]}","{row[5]}","{row[6]}","{row[8]}",{row[9]})"""
                print(query)
                try:
                    my_conn.execute_insert_query(query)
                except Exception as e:
                    with open("curs38\fail.txt",'a') as txt_file:
                        txt_file.write(str(e) +"  "+ query)

class Country():
    def __init__(self,name):
        self.name = name
    
    def get_cities(self):
        orase = my_conn.execute_select_query(f'SELECT city_ascii FROM orase where country = "{self.name}"')
        return [oras[0] for oras in orase]
    
    def get_capital(self):
        capitala = my_conn.execute_select_query(f"SELECT city_ascii FROM orase where country ='{self.name}' and capital = 'primary' ")
        return capitala[0][0]
    
    def get_administrative_cities(self):
        admin_cit = my_conn.execute_select_query(f"SELECT city_ascii FROM orase where country ='{self.name}' and capital = 'admin' ")
        return [oras[0] for oras in admin_cit]
    
    def get_minor_cities(self):
        minor_cit = my_conn.execute_select_query(f"SELECT city_ascii FROM orase where country ='{self.name}' and capital = 'minor' ")
        return [oras[0] for oras in minor_cit]


my_country = Country("Japan")

print(my_country.get_cities())
print("===============================================")
print(my_country.get_capital())
print("===============================================")
print(my_country.get_administrative_cities())
print("===============================================")
print(my_country.get_minor_cities())
