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

def cauta_orasele_unei_tari(tara:str):
    orase = my_conn.execute_select_query(f'SELECT city_ascii FROM orase where country = "{tara}"')
    return [oras[0] for oras in orase]

print(cauta_orasele_unei_tari("Japan"))


# -creati un nou repository pe contul vostru de github 
# -clonati repository-ul local 
# -adaugati codul de la problema anterioara si faceti push catre repository-ul principal 
# -creati un nou branch numit implement-poo-solution
# -mutati-va pe noul branch si creati o clasa numita Country care sa aiba urmatoarele metode:
# init(name): se va crea o clasa care va retine numele tarii
# get_cities(): returneaza toate orasele tarii respective (nu le stocheaza in memorie! executa un query si intoarce rezultatul)
# get_capital(): returenaza capitala tarii respective
# get_administrative_cities(): returneaza toate orasele administrative
# get_minor_cities(): returneaza orasele minore

# -merge-uiti modificarile in branchul master