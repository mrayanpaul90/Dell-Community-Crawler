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

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS MODIFIEDPOSTS")

# Create table as per requirement
sql = """CREATE TABLE MODIFIEDPOSTS (
   CATEGORY VARCHAR(300),
   POST_HEADER VARCHAR(700) NOT NULL,
   POST_AUTHOR VARCHAR(100) NOT NULL,
   POST_URL VARCHAR(400),
   AUTHOR_URL VARCHAR(400),
   DATE VARCHAR(10),
   TIME VARCHAR(10),
   KUDOS_COUNT INT,
   REPLIES_COUNT INT,
   VIEWS_COUNT INT,
   EXTRA VARCHAR(50))"""
cursor.execute(sql)  
 


#launch url
file=open("TopicsSeedFile.txt","w")
urlQueue=["https://www.dell.com/community/Laptops/ct-p/Laptops",
"https://www.dell.com/community/Cloud/ct-p/ESCloud",
"https://www.dell.com/community/Networking/ct-p/ESNetwork",
"https://www.dell.com/community/Desktops/ct-p/Desktops",
"https://www.dell.com/community/Converged-Infrastructure/ct-p/ESConverged-platforms",
"https://www.dell.com/community/Electronics/ct-p/Electronics-Accessories",
"https://www.dell.com/community/Security/ct-p/ESSecurity",
"https://www.dell.com/community/Servers/ct-p/ESServers",
"https://www.dell.com/community/Software/ct-p/Software-and-operating-system",
"https://www.dell.com/community/Data-Protection/ct-p/Data-Protection-Solutions",
"https://www.dell.com/community/Solutions/ct-p/ESPlatform-solutions",
"https://www.dell.com/community/DellEMC-Technical-Webinars/ct-p/DellEMCWebcasts",
"https://www.dell.com/community/SupportAssist-Enterprise/ct-p/ESSupport-Assist",
"https://www.dell.com/community/Tablets/ct-p/Tablets",
"https://www.dell.com/community/Gateways-Embedded-PC-s/ct-p/ESInternet-of-Things",
"https://www.dell.com/community/Education/ct-p/ESEducation",
"https://www.dell.com/community/Thin-Clients/ct-p/ESClientMobile",
"https://www.dell.com/community/Workstations/ct-p/Workstations"]


# create a new Firefox session
driver = webdriver.Firefox()

#Visit each seed page
while len(urlQueue)>0:
	url=urlQueue.pop()
	driver.get(url)
	thereExists=True
	try:
		boardView=driver.find_element_by_class_name("custom-board-browser")
		catViewList=boardView.find_elements_by_class_name("cat-card")
		for catView in catViewList:
			urlQueue.append(catView.find_element_by_class_name("cat-card-title").find_element_by_tag_name("a").get_attribute("href"))
	except NoSuchElementException:
		print(url)
		file.write(url+"\n")
	
file.close()
driver.close()