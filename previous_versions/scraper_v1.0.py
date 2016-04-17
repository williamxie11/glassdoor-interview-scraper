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

# These are specific to the company and the role
companyName = "microsoft"
companyURL1 = "https://www.glassdoor.com/Interview/Microsoft-Software-Development-Engineer-Interview-Questions-EI_IE1651.0,9_KO10,39"
companyURL2 = ".htm"

def obj_dict(obj):
    return obj.__dict__
#enddef

def json_export(data):
	print "Exporting data to " + companyName + ".json"
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

def get_data(driver, URL1, URL2, startPage, endPage, data, refresh):
	URL = URL1 + URL2
	if (startPage == endPage + 1):
		return data
	elif (startPage > 1):
		URL = URL1 + "_IP" + str(startPage) + URL2 # This may be specific to the company and role
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
		get_data(driver, URL1, URL2, startPage + 1, endPage, data, True)
	else:
		print "Waiting ... CAPTCHA blocked or page hasn't loaded all reviews yet."
		time.sleep(3)
		get_data(driver, URL1, URL2, startPage, endPage, data, False)
	#endif
	return data
#enddef

if __name__ == "__main__":
    driver = init_driver()
    login(driver, username, password)
    time.sleep(2)
    data = get_data(driver, companyURL1, companyURL2, 1, 20, [], True)
    json_export(data)
    driver.quit()
#endif




