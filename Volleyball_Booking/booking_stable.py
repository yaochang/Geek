#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from pyvirtualdisplay import Display

import time, sys

#define some global variables
display = Display(visible=0,size=(800,600))
display.start()

accountName = "96970063"
accountPWD = "YaoChang2009"

#TARGET VENUES
#Yuying Secondary School Hall      => 435
#Bedok View Secondary School Hall  => 324
#Jurong West Secondary School Hall => 425
#Hua Yi Secondary School Hall      => 332
targetVenues = ["435","324","425","332"]


#TARGET DAYS
targetDay = ["6"]

#TARGET DATES  ==> this should be specified
targetDate = "Sat, 2 Aug 2014"
#targetDate = "Sun, 03 Aug 2014"
#TARGET ACTIVITY
targetActivity = "293"
#targetActivity = "18"

#TARGET TIME
targetTime = ["17:00:00","18:00:00","19:00:00"];

#Login Address
loginHost = "https://members.myactivesg.com/auth";
#logout address
logoutHost = "https://members.myactivesg.com/auth/logout"
#Filter Address
filterHost = "https://members.myactivesg.com/facilities"
#cartHost
cartHost = "https://members.myactivesg.com/cart"

def login(driver):
	print "[login:]Processing"
	try:
		driver.get(logoutHost)	
		driver.get(loginHost)

		account = driver.find_element_by_id("email")
		account.send_keys(accountName)

		password = driver.find_element_by_id("password")
		password.send_keys(accountPWD)

		driver.find_element_by_id("btn-submit-login").click()
		time.sleep(0.5)
		print "[Login:]Successful"
		return 1
	except:
		return 0


def search(driver,k): #k to indicate the venue 0<=k<=3
	try:
		driver.get(filterHost)
	
		print "[filter:]Processing"
		#choose venue
		print "[filter:]Choose Venue"	
		venue = Select(driver.find_element_by_id("venue_filter"))
		venue.select_by_value(targetVenues[k])
		print "[filter:]Venue=>"+targetVenues[k]

		#choose Volleyball
		print "[filter:]Choose Activity"
		activity = Select(driver.find_element_by_name("activity_filter"))
		activity.select_by_value(targetActivity)
		print "[filter:]Activity=>Volleyball"

		#choose saturday
		print "[filter:]Choose Day"
		day = Select(driver.find_element_by_name("day_filter"))
		day.select_by_value(targetDay[0])
		print "[filter:]Day=>Saturday"
	
		#choose date
		print "[filter:]Choose Date"
		date = driver.find_element_by_name("date_filter")
		date.send_keys(targetDate)
		print "[filter:]Date=>"+targetDate

		venue = Select(driver.find_element_by_id("venue_filter"))
        	venue.select_by_value(targetVenues[k])
		driver.find_element_by_id("search").click()
		time.sleep(1.5)
		print "[filter:]Successful"
		return 1
	except:
		print "[filter:]ERROR"
		return 0

def booking(driver):
	try:
		print "[booking:]Processing"
		checkboxes = driver.find_elements_by_xpath("//input[@name='timeslots[]']")
		count = 0
		#print checkboxes
		print "[booking:]Choose Available Timeslot"
		for checkbox in checkboxes:
			eleId = checkbox.get_attribute("id")
        		value = checkbox.get_attribute("value")
         		words = value.split(";")
         		if words[3] in targetTime:
                 		if (checkbox.is_enabled()) and (not checkbox.is_selected()):
					script = "document.getElementById({}).style.display='block';".format(eleId)
					driver.execute_script(script)
					while not checkbox.is_selected():
						checkbox.click()
					count = count + 1
					print "[booking:]Booked "+words[3]
			if count==2:
				break
	except:
		print "[booking:]ERROR"
		return 0
	
	if count != 0:
		print "[booking:]Add to cart"
		addCart = driver.find_element_by_id("paynow")
		addCart.click()
		time.sleep(0.5)
		try:
			alert = driver.switch_to_alert()	
			alert.accept()
			time.sleep(0.5)
		except:
			print "alert No alert"	
		try:
			gotocart = driver.switch_to_alert()
			gotocart.accept()
		except:
			print "go to cart No alert"
		print "[booking:]Successful"
		return 1
	else:
		print "[booking:]No available timeslots"
		#time.sleep(2)
		return 2

def delete(driver):	
		try:	
			driver.get(cartHost)
			time.sleep(2)			
			button = driver.find_element_by_xpath("//button[@class='btn btn-flat black btn-xs dropdown-toggle']")
			button.click()
			time.sleep(2)
			delete = driver.find_element_by_xpath("//a[@class='deleteFacility']")
			delete.click()
			time.sleep(1)
		except:
			print "[Delete:]ERROR"
			return 0
		try:
			delalert = driver.switch_to_alert()
			delalert.accept()
		except:
			print "No Alert"
		print "[Delete:]Successful"
		return 1
	

def logout(driver):
	try:
	    	driver.get(logoutHost)
		try:
			logalert = driver.switch_to_alert()
			logalert.dismiss()
		except:
			print "No Logout Alert"
		driver.close()
		print "[Logout:]Successful"
		return 1
	except:
		print "[Logout:]ERROR"
		return 0

	
def main():
	tt = 0
	retval = 0
	while tt < 10000:
		print "Loop"+str(tt)
		localtime = time.asctime( time.localtime(time.time()) )
		print "Current Time:", localtime

		tt = tt +1
		retlogin = 0
		while retlogin == 0:
			driver = webdriver.Firefox();
			retlogin = login(driver)
			if retlogin == 0:
				driver.close()
		retsearch = 0
		retsearch = search(driver,0)
		if retsearch == 0:
			driver.close()
			continue
		retbook = 0
		retbook = booking(driver)
		if retbook == 0 or retbook == 2:
			driver.close()
			continue
				
		logout(driver)

		time.sleep(10)
		
		retlogin = 0
		while retlogin == 0:
			driver = webdriver.Firefox();
			retlogin = login(driver)
			if retlogin == 0:
				driver.close()
		retdelete = 0
		retdelete = delete(driver)
		time.sleep(0.5)
		retdelete = delete(driver)
		logout(driver)
		print "******************************************"


main()
display.close()
