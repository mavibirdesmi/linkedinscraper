from selenium import webdriver
from parsel import Selector
import parameters
from time import sleep
import csv

# Uses chromedriver and Google Chrome so please ensure that your Google Chrome version and chromedriver version is same or very close
# This script uses the specified parameters in the parameters.py, so if you want to change something please control parameters.py
# The count for getting linkedin accounts is not limited but it can be limited through linkedin.com or if there is not enough search results

# If your internet is slow please increase the delay time from the parameters.py or you may get empty spaces even though
# there is information on the user's linkedin page.


driver = webdriver.Chrome(executable_path= parameters.chrome_driver_path)
file = open(parameters.file_name, 'w', encoding= 'utf-8')
writer = csv.writer(file)
writer.writerow(['Name', 'Job Title', 'Company', 'Collage', 'Location', 'URL'])



def isValid (value):
    """Checks if the given value is available at the user's linkedin page, if not returns 'Not available'"""
    if (value == None) or (value == ''):
        return 'Not available'
    else:
        return value.strip()

def toSearchWords (list_of_keywords):
    """Transforms the list of keywords to a string required for search bar on google"""
    output = "site:linkedin.com/in/ "
    for keyword in list_of_keywords:
        output += 'AND "{}" '.format(keyword)
    return output


#Logining into linkedin with the given credentials
driver.get('https://tr.linkedin.com/')
login_page = driver.find_element_by_class_name("nav__button-secondary").get_attribute('href')
driver.get(login_page)

email_section = driver.find_element_by_id("username")
password_section = driver.find_element_by_id("password")

button = driver.find_elements_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[3]/button')[0]

email_section.send_keys(parameters.email)
password_section.send_keys(parameters.password)
button.click()

#Navigating to google for searching
driver.get("https://www.google.com/")

search_query = driver.find_element_by_name('q')
search_query.send_keys(toSearchWords(parameters.keywords))
search_query.submit()

#Now we are in the search area and we are going to get the links by going through page
web_results = driver.find_element_by_xpath('//*[@id="rso"]')
url_list = []
k = 1
for i in range(1, parameters.count + 1):

    url_list.append(driver.find_element_by_xpath('//*[@id="rso"]/div[{}]/div/div[1]/a'.format(k)).get_attribute('href'))
    k += 1
    if (i % 10 == 0):
        next_page = driver.find_element_by_xpath('//*[@id="pnnext"]').get_attribute('href')
        driver.get(next_page)
        k = 1

#Lastly we will scrape the data in the linkedin urls to the specified csv file 
for url in url_list:
    driver.get(url)
    sleep(parameters.delay)
    sel = Selector(text=driver.page_source)

    name = isValid(sel.xpath('//*[@id="ember51"]/div[2]/div[2]/div[1]/ul[1]/li[1]/text()').extract_first())
    company = isValid(sel.xpath('//*[@id="ember94"]/text()').extract_first())
    education = isValid(sel.xpath('//*[@id="ember98"]/text()').extract_first())
    job_title = isValid(sel.xpath('//*[@id="ember51"]/div[2]/div[2]/div[1]/h2/text()').extract_first())
    location = isValid(sel.xpath('//*[@id="ember51"]/div[2]/div[2]/div[1]/ul[2]/li[1]/text()').extract_first())

    writer.writerow([
        name,
        job_title,
        company,
        education,
        location,
        url,
    ])
