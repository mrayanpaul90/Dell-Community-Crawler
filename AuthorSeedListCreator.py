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
sql = """CREATE TABLE USER_DETAILS (
   USER_URL VARCHAR(400),
   USER_NAME VARCHAR(100),
   USER_RANK VARCHAR(100),
   POSTS_COUNT INT,
   SOLUTIONS_COUNT INT,
   KUDOS_GIVEN_COUNT INT,
   KUDOS_RECEIVED_COUNT INT,
   DATE_REGISTERED VARCHAR(10))"""

cursor.execute(sql)  
 


#launch url
file=open("AuthorSeedList.txt","w")

cursor.execute("SELECT DISTINCT AUTHOR_URL FROM MODIFIEDPOSTS WHERE AUTHOR_URL IS NOT NULL UNION SELECT DISTINCT AUTHOR_URL FROM THREAD_REPLY_DETAILS WHERE AUTHOR_URL IS NOT NULL")
row = cursor.fetchone()

while row is not None:
	file.write(row[0]+"\n")
	row = cursor.fetchone()

file.close()
db.commit()
cursor.close()
db.close()