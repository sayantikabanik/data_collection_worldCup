#importing necessary libraries 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time
import csv
import pandas as pd 
import random
import time

#locating the driver path and initiating 
driver = webdriver.Chrome(executable_path='C:/Users/SAYANTIKA BANIK/Downloads/chromedriver.exe')

#open web url for crawling
search_url = 'https://www.espncricinfo.com/series/icc-cricket-world-cup-2019-1144415/match-results'

#request initiated for given web url/link
driver.get(search_url)

#random choices for sleep, making sure IP isn't flagged by the servers
time.sleep(random.choice([0, 2, 4, 6, 8, 14,23]))

#initializing lists 
match_number, location, date, other_country_score, win_country_score = [], [], [], [], []


# contructing xpath for match number, location and date
match_details = driver.find_elements_by_xpath("//div[contains(@class, 'match-info match-info-FIXTURES')]/div[2]")
res = [i.text for i in match_details if i.text !='']
each_val = [j.split(',') for j in res] #spliting elements based on comma
for val in each_val:
	match_number.append(val[0])
	location.append(val[1])
	date.append(val[2])

#constructing the xpath for the match result
match_result = driver.find_elements_by_xpath("//div[contains(@class,'match-info match-info-FIXTURES')]/div[4]/span")
match_result_list = [det.text for det in match_result if det.text!='']

#getting the link to match report, summary and scorecard
###
match_report = driver.find_elements_by_xpath("//div[contains(@class, 'match-cta-container')]/a[1]")
link_report = [link.get_attribute("href") for link in match_report]

match_summary = driver.find_elements_by_xpath("//div[contains(@class, 'match-cta-container')]/a[2]")
link_summary = [link.get_attribute("href") for link in match_summary]

match_scorecard = driver.find_elements_by_xpath("//div[contains(@class, 'match-cta-container')]/a[3]")
link_scorecard = [link.get_attribute("href") for link in match_scorecard]
###

#other country (haven't won the match)
other_country = driver.find_elements_by_xpath("//div[contains(@class, 'match-info match-info-FIXTURES')]/div[3]/div[1]/div[1]/p")
other_country = [not_win.text for not_win in other_country if not_win.text!='']


# using Bs4 to accomodate null values for the scores for other country and winning country
import requests
page = requests.get('https://www.espncricinfo.com/series/icc-cricket-world-cup-2019-1144415/match-results')
soup = BeautifulSoup(page.content, 'html.parser')

#other country score
div_outter = soup.find_all(class_="match-info match-info-FIXTURES")
for out in div_outter:
	status = out.find(class_="status")
	for sta in status:
		info = sta.get_text()
		if info == "abandoned" or info == "no result":
			other_country_score.append("null")
		else:
			try:
				div_data = out.find(class_="team team-gray")
				forecast_items = div_data.find(class_="score").get_text()
				other_country_score.append(forecast_items)
			except:
				other_country_score.append("null")

#win country
win_country = driver.find_elements_by_xpath("//div[contains(@class, 'match-info match-info-FIXTURES')]/div[3]/div[2]/div[1]/p")
win_country = [win.text for win in win_country if win.text!='']

#win country score
div_outter = soup.find_all(class_="match-info match-info-FIXTURES")
for out in div_outter:
	status = out.find(class_="status")
	for sta in status:
		info = sta.get_text()
		if info == "abandoned" or info == "no result":
			win_country_score.append("null")
		else:
			try:
				div_data = out.find(class_="team")
				forecast_items = div_data.find(class_="score").get_text()
				win_country_score.append(forecast_items)
			except:
				win_country_score.append("null")

#validating results obtained 
print(len(match_number), len(location), len(date), len(match_result_list), len(link_report), len(link_summary), len(link_scorecard),
	len(other_country), len(win_country), len(win_country_score), len(other_country_score))

#creating data dictionary
match_ = {'match_number': match_number, 'location': location, 'date': date, 'match_result_list':match_result_list, 'link_report':link_report,
'link_summary':link_summary, 'link_scorecard':link_scorecard, 'other_country':other_country, 'win_country':win_country, 'other_country_score':other_country_score,
'win_country_score':win_country_score}

#inititizing dataframe
df = pd.DataFrame(data=match_)
#saving the data in tab seperated format
df.to_csv("07_matchResults.tsv", sep="\t") 
