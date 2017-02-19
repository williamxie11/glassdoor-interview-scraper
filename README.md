# glassdoor-interview-scraper

Glassdoor web crawler and scraper providing interview experience data for [Decoding The Interview](https://github.com/williamxie11/decoding-the-interview).

This was an academic project for CS 410 - Text and Information Systems at UIUC and is no longer maintained.

## Installation

* Python 2.7.*

* Beautiful Soup 4 (4.4.1)
```sh
$ pip install bs4
```
* Selenium Webdriver
```sh
$ pip install selenium
```

## Usage

1. Open the scraper Python script with a text editor of your choice. 
2. Add your Glassdoor account username and password
![username and password](http://i.imgur.com/gHzYwZZ.png)
3. Specify the number of pages, the company name, and the URL of the interviews page for the company on Glassdoor with your specified filters selected
![scraper settings](http://i.imgur.com/TOLZqhJ.png)
4. Run the scraper
```sh
$ python scraper_v1.2.py
```

NOTE: Glassdoor will require you to insert CAPTCHA on login or during the scraping process. The script will poll until CAPTCHA is entered during scraping.

## Results

![response](http://i.imgur.com/zY8l22v.png)

The web scraper will output a JSON with the name "[company name].json" in the same directory. Each data point in the JSON corresponds to one interview review on Glassdoor with attributes (see above) for each portion of the review.

## Changelog

###v1.2
- companyURL now accepts full path of Interview page for ease of use
- Fixed issue with pagination not working
- Fixed issue where scraper would erroneously get stuck waiting for the page to load 
- Increased initial sleep time in case of CAPTCHA
- Reduced polling time on waiting for page load or captcha input
- Now takes an additional short break every 10 pages to avoid rate limiting
- Cleaned up and added some more progress dialogue

###v1.1
- Made maxnum a global pages variable for easier use
- Removed option and dependency for URL2 as each link ends in ".htm" anyways
- Removed unnecessary concatenation of URL links at the beginning of get_data(). Glassdoor automatically redirects _IP1 link to the first interview page.
- Increased sleep time after login
- Increased sleep time in between scraping interview pages
- Added some more progess dialogue

###v1.0
- And so it begins ...
