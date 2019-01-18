import mysql.connector

# Open database connection
db = mysql.connector.connect(user='ayan',password='Intern@2018',host='127.0.0.1',database='WebCrawler')
# prepare a cursor object using cursor() method
cursor = db.cursor(buffered=True)
# execute SQL query using execute() method.
cursor.execute("SHOW DATABASES")
# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print ("Database version : %s " % data)

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS THREAD_DETAILS")

# Create table as per requirement
sql = """CREATE TABLE THREAD_DETAILS (
   POST_URL VARCHAR(400),
   POST_DETAIL VARCHAR(30000),
   TAGS VARCHAR(500))"""
cursor.execute(sql)  


# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS THREAD_REPLY_DETAILS")

# Create table as per requirement
sql = """CREATE TABLE THREAD_REPLY_DETAILS (
   POST_URL VARCHAR(400),
   REPLY_AUTHOR VARCHAR(100) NOT NULL,
   AUTHOR_URL VARCHAR(400),
   DATE VARCHAR(10),
   TIME VARCHAR(10),
   REPLY_DETAIL VARCHAR(30000),
   KUDOS_COUNT INT,
   ACCEPTED VARCHAR(5))"""

cursor.execute(sql)  
 


#launch url
file=open("ThreadSeedList.txt","w")

cursor.execute("SELECT DISTINCT POST_URL FROM MODIFIEDPOSTS")
row = cursor.fetchone()

while row is not None:
	file.write(row[0]+"\n")
	row = cursor.fetchone()

file.close()
db.commit()
cursor.close()
db.close()