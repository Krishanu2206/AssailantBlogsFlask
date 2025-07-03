import pymysql

# Establish the connection
mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="Krishanu@2206",
    database="users"
)

# Create a cursor object
my_cursor = mydb.cursor()

# CREATE DATABASE
# my_cursor.execute("CREATE DATABASE users;")

##SHOW DATABASES
my_cursor.execute("SHOW DATABASES;")

for db in my_cursor:
    print(db)

# Fetch and print the result
database_name = my_cursor.fetchone()
print("Connected to database:", database_name)

# Close the cursor and connection
my_cursor.close()
mydb.close()