import sqlite3

## Connect to the sqlite
connection=sqlite3.connect("student.db")

## Create a cursur object to insert records,create a table 
cursor=connection.cursor()

## Create the table

table_info="""

 CREATE TABLE IF NOT EXISTS STUDENT ( NAME VARCHAR(30),CLASS VARCHAR(30),SECTION VARCHAR (30),MARKS INTEGER  );

"""
cursor.execute(table_info)

## Insert some more records

cursor.execute('''Insert Into STUDENT values ('Ajay','Data Science','A','80')''')
cursor.execute('''Insert Into STUDENT values ('Ansh','Data Science','B','70')''')
cursor.execute('''Insert Into STUDENT values ('Samarth','Data Science','A','90')''')
cursor.execute('''Insert Into STUDENT values ('Neelam','Devops','A','65')''')
cursor.execute('''Insert Into STUDENT values ('Alok','Devops','A','45')''')

## Display all the records

print("inserted records are")
data=cursor.execute('''Select * from STUDENT''')

for row in data:
    print(row)

connection.commit()
connection.close()