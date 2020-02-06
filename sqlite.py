import sqlite3

conn = sqlite3.connect('flags.db')

c = conn.cursor()

'''c.execute("""CREATE TABLE flags (
            countries text,
            iso text,
            file text
            )""")'''

with open("list-of-countries.txt") as list:
 countries = list.read()


#c.execute(f'INSERT INTO flags VALUES ("Yummy","Bummy","Uuuuu")')

c.execute("SELECT * FROM flags WHERE iso='Bummy'")

print(c.fetchone())

conn.commit()

conn.close()