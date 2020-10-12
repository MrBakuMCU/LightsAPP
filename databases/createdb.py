import sqlite3

connectionObject = sqlite3.connect("weather.db")

cursorObject = connectionObject.cursor()

# Create a table in the disk file based database

createTable = "CREATE TABLE temperature(id int, temp numeric(3,1))"

cursorObject.execute(createTable)

# Insert EOD stats into the reports table

insertValues = "INSERT INTO temperature values(1,40.1)"

cursorObject.execute(insertValues)

insertValues = "INSERT INTO temperature values(2,65.4)"

cursorObject.execute(insertValues)

queryTable = "SELECT * from temperature"

queryResults = cursorObject.execute(queryTable)

print("(CityId, Temperature)")

for result in queryResults:
    print(result)

connectionObject.close()
