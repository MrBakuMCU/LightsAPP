import sqlite3

connectionObject = sqlite3.connect("lights.db")

cursorObject = connectionObject.cursor()

# Create a table in the disk file based database

createTable = "CREATE TABLE lights_change(id int, time_start char(5), time_stop char(5)3,1), current_timestamp ()"
cursorObject.execute(createTable)

# insertValues = "INSERT INTO temperature values(1,40.1)"
#cursorObject.execute(insertValues)

queryTable = "SELECT * from lights_change"
queryResults = cursorObject.execute(queryTable)
print("()")

for result in queryResults:
    print(result)

connectionObject.close()
