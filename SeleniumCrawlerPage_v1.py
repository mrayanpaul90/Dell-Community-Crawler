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
file=open("TopicsSeedFile.txt","r")
urlQueue=file.readlines()
file.close()

# create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(30)

#Visit each seed page
for url in urlQueue:
	driver.get(url)
	thereExists=True
	temp=url.split("/")[-1]
	pageCounter=1 if not temp.isdigit() else (int)(temp) 
	
	#Create file path for storage of pages
	forumBreadcrumbs=driver.find_elements_by_class_name("lia-breadcrumb-node")
	filePath="C:\\DataCollection_v1"
	escapeChar=string.punctuation.replace("&","").replace("_","").replace("-","")
	translator = str.maketrans(escapeChar, ' '*len(escapeChar)) #map punctuation to space

	categoryList=[]
	for forumBreadcrumb in forumBreadcrumbs:
		category=forumBreadcrumb.text.translate(translator)
		categoryList.append(category)
		filePath=os.path.join(filePath,category)
		if(os.path.exists(filePath)==False):
			os.makedirs(filePath)
	
	
	
	while thereExists:
		try:
			postsTable=driver.find_element_by_class_name("lia-list-wide")
			postsDetailList=[]
			postsList=[]
			postsList=postsTable.find_elements_by_class_name("lia-list-row")
			for post in postsList:
				msgDetails=post.find_element_by_class_name("message-subject")
				post_heading=msgDetails.find_element_by_tag_name("a").text.replace("'","''").replace("\\","\\\\")
				post_link=msgDetails.find_element_by_tag_name("a").get_attribute("href")
				try:
					usrDetails=post.find_element_by_class_name("UserName")
					user_name=usrDetails.find_element_by_tag_name("a").text.replace("'","''").replace("\\","\\\\")
					user_link=usrDetails.find_element_by_tag_name("a").get_attribute("href")
				except NoSuchElementException:
					print("User Details not found-----");
					print(post_heading)
					user_name="Anonymous"
					user_link=None
				time=post.find_element_by_class_name("local-time").text
				date=post.find_element_by_class_name("local-date").text
				try:
					kudos=(int)(post.find_element_by_class_name("cKudosCountColumn").text)
				except NoSuchElementException:
					print("Kudos not found-----");
					print(post_heading)
					kudos=0
				except ValueError:
					print("Kudos not found-----");
					print(post_heading)
					kudos=0
				try:
					replies=(int)(post.find_element_by_class_name("cRepliesCountColumn").text)
				except NoSuchElementException:
					print("Replies not found-----");
					print(post_heading)
					replies=0
				except ValueError:
					print("Replies not found-----");
					print(post_heading)
					replies=0
				views=(int)(post.find_element_by_class_name("cViewsCountColumn").text.split()[0])
				desc=post.find_element_by_class_name("triangletop").get_attribute('aria-label')
				postsDetailList.append((','.join(categoryList),post_heading,user_name,post_link,user_link,time,date,kudos,replies,views,desc))
			navigationUrl=driver.find_element_by_class_name("lia-paging-page-next").find_element_by_tag_name("a").get_attribute("href")
		except StaleElementReferenceException:
			print("StaleElementReferenceException-----")
			driver.get(url)
			continue
		except NoSuchElementException:
			print("Outer NoSuchElementException-----")
			thereExists=False
			navigationUrl=None
		
		##insert into SQL DB
		for eachPost in postsDetailList:
			#print(eachPost)
			# Prepare SQL query to INSERT a record into the database.
			sql = "INSERT INTO MODIFIEDPOSTS(CATEGORY, POST_HEADER, POST_AUTHOR, POST_URL, AUTHOR_URL, DATE, TIME, KUDOS_COUNT, REPLIES_COUNT, VIEWS_COUNT, EXTRA) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%d', '%d', '%s' )" % eachPost
			cursor.execute(sql)
		db.commit()
		print(os.path.join(filePath,"Page"+(str)(pageCounter)+".html"))
		file=open(os.path.join(filePath.strip(),"Page"+(str)(pageCounter)+".html"),'w',encoding="utf-8")
		file.write(driver.page_source)
		file.close()
		pageCounter=pageCounter+1
		if not (navigationUrl is None):
			driver.get(navigationUrl)
		#end of page
	#end of one subTopic go back
cursor.close()
db.close()
driver.close()
