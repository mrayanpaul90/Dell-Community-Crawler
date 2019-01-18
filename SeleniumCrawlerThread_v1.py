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
#cursor.execute("DROP TABLE IF EXISTS POSTS3")


#launch url
file=open("ThreadSeedList.txt","r")
urlQueue=file.readlines()
file.close()


# create a new Firefox session
driver = webdriver.Firefox()

#Visit each seed page
for url in urlQueue:
	driver.get(url)
	thereExists=True
	 
	
	#Create file path for storage of pages
	forumBreadcrumbs=driver.find_elements_by_class_name("lia-breadcrumb-node")
	filePath="C:\\DataCollection\\thread"
	pageCounter=1
	escapeChar=string.punctuation.replace("&","").replace("_","").replace("-","")
	translator = str.maketrans(escapeChar, ' '*len(escapeChar)) #map punctuation to space
	allCategories=[]
	
	for Breadcrumbs in forumBreadcrumbs:
		allCategories.append(Breadcrumbs.text.translate(translator))
		filePath=os.path.join(filePath,allCategories[-1])
		if(os.path.exists(filePath)==False):
			os.makedirs(filePath)
	
	
	message_view=driver.find_element_by_class_name("lia-component-topic-message")
	message_content=message_view.find_element_by_class_name("lia-message-body-content").text.replace("'","")
	tagList=[]
	try:
		tag_view=driver.find_element_by_class_name("MessageTagsTaplet")
		tag_view_classes=tag_view.find_element_by_class_name("lia-message-tags").find_elements_by_class_name("lia-tag-list-item")
		
		for tag_view_class in tag_view_classes:
				tagList.append(tag_view_class.text)
	except NoSuchElementException:
		print("NO tags available for URL:")
	
	print(message_content)
	print(tagList)
	
	while thereExists:
		try:
			reply_view=driver.find_element_by_class_name("lia-component-reply-list")
			reply_threads=reply_view.find_elements_by_class_name("lia-linear-display-message-view")
			replysDetailList=[]
			print(len(reply_threads))
			for reply_thread in reply_threads:
				try:
					author_name=reply_thread.find_element_by_class_name("lia-quilt-row-message-header").find_element_by_class_name("UserName").text
					author_url=reply_thread.find_element_by_class_name("lia-quilt-row-message-header").find_element_by_class_name("UserName").find_element_by_tag_name("a").get_attribute("href")
				except NoSuchElementException:
					print("Reply User Details not found-----");
					author_name="Anonymous"
					author_url=None
				date=reply_thread.find_element_by_class_name("lia-quilt-row-message-post-times").find_element_by_class_name("local-date").text
				time=reply_thread.find_element_by_class_name("lia-quilt-row-message-post-times").find_element_by_class_name("local-time").text
				reply_content=reply_thread.find_element_by_class_name("lia-quilt-row-message-body").text.replace("'","")
				kudos=(int)(reply_thread.find_element_by_class_name("lia-quilt-row-message-controls").find_element_by_class_name("MessageKudosCount").text)
				accepted="yes"
				
				try:
					reply_thread.find_element_by_class_name("lia-message-view-wrapper").find_element_by_class_name("lia-accepted-solution")
				except NoSuchElementException:
					accepted="no"
				#print([author_name,author_url,date,time,reply_content,kudos,accepted])
				replysDetailList.append((url,author_name,author_url,date,time,reply_content,kudos,accepted))

			#Save the read page
			print(os.path.join(filePath,"Page"+(str)(pageCounter)+".html"))
			file=open(os.path.join(filePath.strip(),"Page"+(str)(pageCounter)+".html"),'w',encoding="utf-8")
			file.write(driver.page_source)
			file.close()
			pageCounter=pageCounter+1
			
			navigationUrl=driver.find_element_by_class_name("lia-discussion-page-message-pager").find_element_by_class_name("lia-paging-page-next").find_element_by_tag_name("a").get_attribute("href")
			driver.get(navigationUrl)
			continue
		except NoSuchElementException:
			print("Outer NoSuchElementException-----")
			thereExists=False
			navigationUrl=None
	# Prepare SQL query to INSERT a record into the database.
	temp_data= (url,message_content,';'.join(tagList))
	print(temp_data)
	print(len(temp_data))
	sql = "INSERT INTO THREAD_DETAILS VALUES (%s, %s, %s)"
	cursor.execute(sql,temp_data)
	for replyDetail  in replysDetailList:
		print(replyDetail)
		print(len(replyDetail))
		sql = "INSERT INTO THREAD_REPLY_DETAILS (POST_URL,REPLY_AUTHOR,AUTHOR_URL,DATE,TIME,REPLY_DETAIL,KUDOS_COUNT,ACCEPTED) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %replyDetail
		cursor.execute(sql)
	db.commit()	
cursor.close()
driver.close()
