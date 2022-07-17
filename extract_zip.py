from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os
import random
import csv
import re
import json


def ini_browser():
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
    opts = Options()
    opts.add_argument("user-agent=" + USER_AGENT)
    s=Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=s, options=opts)
    return browser

links = open("Downloads/fonts_domains_2.csv", "r")

alllinks = links.readlines()

browser = ini_browser()

global row 

row = []


for url in alllinks:
	
	try:
	
		browser.get(url.strip())
		browser.maximize_window()
		browser.get(url)
		
		time.sleep(5)
		
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
		
		
		
		impress_link = browser.find_element_by_xpath("//a[contains(text(), 'Impressum')]").get_attribute("href")
		
		impress = impress_link.strip(" ")
		
		browser.get(impress)
		
		time.sleep(5)
		
		el = browser.find_element(By.TAG_NAME, 'body')
		
		textsite = el.text
		
		
		x = re.search("(?<!\d)\d{4}(?!\d) [a-zA-Z](.+?)\s", textsite)
		
		print(x.group(0))
	
	except:
		continue
	
	
	
	zip_city = x.group(0).split()
	
	print(zip_city[1])
	
	textdivide = textsite.split()
	
	print(textdivide)
	
	streetsfile = open("gemplzstr.json")
	
	all_streets = json.load(streetsfile)["datensatz"]
	
	domain = url.strip()
	
	zipcode = zip_city[0]
	
	city = zip_city[1]
	
	streetname = ""
	
	
	for street in all_streets:
		if street["element"][5] in textdivide and street["element"][5] != "Wagner" and street["element"][5] != "Roller" and street["element"][5] != "Wien" and street["element"][5] != str(zip_city[1]):
			print(street["element"][5])
			streetname = str(street["element"][5])
			break
		else:
			continue
	
	try:
		findex = textdivide.index(streetname)
		
		indexof = int(findex) + 1
		
		number = textdivide[indexof]
	except:
		number = "None"
	
	row.append(domain)
	
	row.append(zipcode)
	
	row.append(city)
	
	row.append(streetname)
	
	row.append(number)
	
	print(row)
	
	csvfile = open("hello.csv", "a")
	csv_writer = csv.writer(csvfile)
	csv_writer.writerow(row)
	csvfile.close()
	row.clear()
	
	browser.execute_script("window.stop();")
	
		

	
	













