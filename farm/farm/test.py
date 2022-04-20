
import sqlite3

# Accès à la base de données

conn = sqlite3.connect('farm.db')

# Le curseur permettra l'envoi des commandes SQL
cursor = conn.cursor()
#create_table = open("schema.sql").read()
#cursor.executescript(create_table)
sqlfile = open("sql/insert_types.sql")
sqlfile1 = open("sql/insert_velages_complications.sql")
i=sqlfile.read()
j=sqlfile1.read()
cursor.executescript(i)
cursor.executescript(j)
# utilisation de la base de données

# Si on a fait des modifications à la base de données
conn.commit()

# Toujours fermer la connexion quand elle n'est plus utile
conn.close()