import sqlite3

connectionObject = sqlite3.connect("../databases/temp.db")

cursorObject = connectionObject.cursor()

# Create a table in the disk file based database
droptable = "DROP TABLE IF EXISTS temp_inside_db;"
createTable = "CREATE TABLE temp_inside_db (id INTEGER PRIMARY KEY AUTOINCREMENT, " \
              "timestamp TEXT DEFAULT (strftime('%Y-%m-%d %H:%M','now', 'localtime')), temp_in NUMERIC NOT NULL, \
              hum_in NUMERIC NOT NULL, psi_in NUMERIC NOT NULL)"
cursorObject.execute(createTable)

# insertValues = "INSERT INTO temperature values(1,40.1)"
# cursorObject.execute(insertValues)

queryTable = "SELECT * from temp_inside_db"
queryResults = cursorObject.execute(queryTable)

for result in queryResults:
    print(result)

connectionObject.close()
