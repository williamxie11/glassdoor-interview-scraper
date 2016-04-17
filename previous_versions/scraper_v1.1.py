import time
import json
import Review
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
  
username = "example@email.com" # your email here
password = "password" # your password here

# Manual options for the company, num pages to scrape, and URL
pages = 197
companyName = "google"
companyURL = "https://www.glassdoor.com/Interview/Google-Software-Engineer-Interview-Questions-EI_IE9079.0,6_KO7,24"

def obj_dict(obj):
    return obj.__dict__
#enddef

def json_export(data):
	jsonFile = open(companyName + ".json", "w")
	jsonFile.write(json.dumps(data, indent=4, separators=(',', ': '), default=obj_dict))
	jsonFile.close()
#enddef

def init_driver():
    driver = webdriver.Chrome(executable_path = "./chromedriver")
    driver.wait = WebDriverWait(driver, 10)
    return driver
#enddef
 
def login(driver, username, password):
    driver.get("http://www.glassdoor.com/profile/login_input.htm")
    try:
        user_field = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "username")))
        pw_field = driver.find_element_by_class_name("signin-password")
        login_button = driver.find_element_by_id("signInBtn")
        user_field.send_keys(username)
        user_field.send_keys(Keys.TAB)
        time.sleep(1)
        pw_field.send_keys(password)
        time.sleep(1)
        login_button.click()
    except TimeoutException:
        print("TimeoutException! Username/password field or login button not found on glassdoor.com")
#enddef

def parse_reviews_HTML(reviews, data):
	for review in reviews:
		length = "-"
		gotOffer = "-"
		experience = "-"
		difficulty = "-"
		date = review.find("time", { "class" : "date" }).getText().strip()
		role = review.find("span", { "class" : "reviewer"}).getText().strip()
		outcomes = review.find_all("div", { "class" : ["tightLt", "col"] })
		if (len(outcomes) > 0):
			gotOffer = outcomes[0].find("span", { "class" : "middle"}).getText().strip()
		#endif
		if (len(outcomes) > 1):
			experience = outcomes[1].find("span", { "class" : "middle"}).getText().strip()
		#endif
		if (len(outcomes) > 2):
			difficulty = outcomes[2].find("span", { "class" : "middle"}).getText().strip()
		#endif
		appDetails = review.find("p", { "class" : "applicationDetails"})
		if (appDetails):
			appDetails = appDetails.getText().strip()
			tookFormat = appDetails.find("took ")
			if (tookFormat >= 0):
				start = appDetails.find("took ") + 5
				length = appDetails[start :].split('.', 1)[0]
			#endif
		else:
			appDetails = "-"
		#endif
		details = review.find("p", { "class" : "interviewDetails"})
		if (details): 
			s = details.find("span", { "class" : ["link", "moreLink"] })
			if (s):
				s.extract() # Remove the "Show More" text and link if it exists
			#endif
			details = details.getText().strip()
		#endif
		questions = []
		qs = review.find_all("span", { "class" : "interviewQuestion"})
		if (qs):
			for q in qs:
				s = q.find("span", { "class" : ["link", "moreLink"] })
				if (s):
					s.extract() # Remove the "Show More" text and link if it exists
				#endif
				questions.append(q.getText().encode('utf-8').strip())
			#endfor
		#endif
		r = Review.Review(date, role, gotOffer, experience, difficulty, length, details, questions)
		data.append(r)
	#endfor
	return data
#enddef

def get_data(driver, URL, startPage, endPage, data, refresh):
	if (startPage == endPage + 1):
		return data
	#endif
	URL = URL + "_IP" + str(startPage) + ".htm"
	#endif
	time.sleep(1)
	if (refresh):
		driver.get(URL)
	#endif
	HTML = driver.page_source
	soup = BeautifulSoup(HTML, "html.parser")
	reviews = soup.find_all("li", { "class" : ["empReview", "padVert"] })
	if (reviews):
		data = parse_reviews_HTML(reviews, data)
		print "PAGE " + str(startPage) + " scraped."
		get_data(driver, URL, startPage + 1, endPage, data, True)
	else:
		print "Waiting ... page still loading or CAPTCHA input required"
		time.sleep(3)
		get_data(driver, URL, startPage, endPage, data, False)
	#endif
	return data
#enddef

if __name__ == "__main__":
	driver = init_driver()
	print "Logging into Glassdoor account ..."
	login(driver, username, password)
	time.sleep(5)
	print "Starting data scraping ..."
	data = get_data(driver, companyURL, 1, pages, [], True)
	print "Exporting data to " + companyName + ".json"
	json_export(data)
	driver.quit()
#endif




