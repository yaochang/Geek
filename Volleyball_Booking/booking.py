#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from pyvirtualdisplay import Display

import time, sys

display = Display(visible=0,size=(800,600))
display.start()


print "------------------login------------------------"
driver = webdriver.Firefox()
driver.get("https://members.myactivesg.com/auth")

account = driver.find_element_by_id("email")
account.send_keys("96970063")

password = driver.find_element_by_id("password")
password.send_keys("YaoChang2009")

driver.find_element_by_id("btn-submit-login").click()
driver.get("https://members.myactivesg.com/facilities")
print "-----------------end login----------------------"
print "-----------------search filter------------------"

venue = Select(driver.find_element_by_id("venue_filter"))
venue.select_by_value("435")

activity = Select(driver.find_element_by_name("activity_filter"))
activity.select_by_value("293")

day = Select(driver.find_element_by_name("day_filter"))
day.select_by_value("6")

date = driver.find_element_by_name("date_filter")
date.send_keys("Sat, 2 Aug 2014")

venue = Select(driver.find_element_by_id("venue_filter"))
venue.select_by_value("435")

driver.find_element_by_id("search").click()

print "--------------------end search-------------------------"
time.sleep(3)
#checkbox = driver.find_element_by_xpath("//input[@id='487494']")
#print checkbox
#print checkbox.is_selected()
#print checkbox.is_enabled()
#print checkbox.is_displayed()
checkbox = driver.find_element_by_id("487494")
driver.execute_script("document.getElementById('487494').style.display='block';")
while not checkbox.is_selected():
	checkbox.click()

print checkbox
print checkbox.is_selected()
print checkbox.is_enabled()
print checkbox.is_displayed()
add = driver.find_element_by_id("paynow")
add.click()
print "-------------------add cart-----------------------------"
alert = driver.switch_to_alert()
alert.accept()
gotocart = driver.switch_to_alert()
gotocart.dismiss()
driver.close()
print "-------------------Successful---------------------------"
time.sleep(5)

display.stop()
