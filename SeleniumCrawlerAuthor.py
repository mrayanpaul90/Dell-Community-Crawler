from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import mysql.connector
import os
import string
import os.path
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

# Open database connection
db = mysql.connector.connect(user='ayan',password='Intern@2018',host='127.0.0.1',database='WebCrawler')
# prepare a cursor object using cursor() method
cursor = db.cursor(buffered=True)
# execute SQL query using execute() method.
cursor.execute("SHOW DATABASES")
# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print ("Database version : %s " % data)


 

#launch url
file=open("AuthorSeedList.txt","r")
urlQueue=file.readlines()
file.close()


# create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(30)


#Visit each seed page
for url in urlQueue:
	driver.get(url)
	user_id=url.split("/")[-1]
	filePath="C:\\DataCollection"
	filePath=os.path.join(filePath,"Users")
	if(os.path.exists(filePath)==False):
		os.makedirs(filePath)
	#Create file path for storage of pages
	
	try:
		row_header_view=driver.find_element_by_class_name("lia-quilt-row-header")
		user_name=row_header_view.find_element_by_class_name("UserName").text
		user_rank=row_header_view.find_element_by_class_name("lia-user-rank").text
		member_stats_view=driver.find_element_by_class_name("MyStatisticsBeanDisplay")
		posted = (int)member_stats_view.find_element_by_class_name("messagesPosted").text
		solutions = (int)member_stats_view.find_element_by_class_name("solutions").text
		kudos_given = (int)member_stats_view.find_element_by_class_name("kudosGiven").text
		kudos_received = (int)member_stats_view.find_element_by_class_name("kudosReceived").text
		date_registered = member_stats_view.find_element_by_class_name("dateRegistered").text
		#print([user_name,user_rank,posted,solutions,kudos_given,kudos_received,date_registered])
	except:
		print("Failure in URL:"+url)
	sql = "INSERT INTO USER_DETAILS VALUES (%s, %s, %d, %d, %d, %d, %s)"
	cursor.execute(sql,(user_name,user_rank,posted,solutions,kudos_given,kudos_received,date_registered))
	db.commit()
	print(os.path.join(filePath,(str)(user_id)+".html"))
	file=open(os.path.join(filePath.strip(),(str)(user_id)+".html"),'w',encoding="utf-8")
	file.write(driver.page_source)
	file.close()
		
	'''
	print(len(member_stats_view))
	'''
cursor.close()
driver.close()
