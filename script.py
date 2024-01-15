import csv
import parameters
from time import sleep
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def validate_field(field):
    if field:
        pass
    else:
        field = ''
    return field

writer = csv.writer(open(parameters.file_name, 'wb'))
writer.writerow(['Name', 'Job Title', 'School', 'Location', 'URL'])

driver = webdriver.Chrome('G://documents//Savefiles//chromeDriver//chromedriver.exe')
driver.get('https://www.linkedin.com')

username = driver.find_element_by_class_name('login-email')
username.send_keys(parameters.linkedin_username)
sleep(.5)

password = driver.find_element_by_id('login-password')
password.send_keys(parameters.linkedin_password)
sleep(.5)

enter = driver.find_element_by_xpath('//*[@type="submit"]')
enter.click()
sleep(2.9)

driver.get('http://www.google.com')
sleep(2.2)

goo_search = driver.find_element_by_name('q')
goo_search.send_keys(parameters.serach_query)
sleep(.7)

goo_search.send_keys(Keys.RETURN)
sleep(2.6)

linkedin_urls = driver.find_elements_by_tag_name('cite')
linkedin_urls = [url.text for url in linkedin_urls]
sleep(.4)

for linkedin_url in linkedin_urls:
    driver.get(linkedin_url)
    sleep(1.3)

    sel = Selector(text=driver.page_source)

    name = sel.xpath('//h1/text()').extract_first()
    if name:
        name = name.strip()

    job_title = sel.xpath('//h2/text()').extract_first()
    if job_title:
        job_title = job_title.strip()

    school = sel.xpath('//*[starts-with(@class, "pv-top-card-v2-section__entity-name")]/text()').extract_first()
    if school:
        school = school.strip()

    location = sel.xpath('//*[starts-with(@class, "pv-top-card-section__location")]/text()').extract_first()
    if location:
        location = location.strip()

    linkedin_url = driver.current_url

    name = validate_field(name)
    job_title = validate_field(job_title)
    school = validate_field(school)
    location = validate_field(location)
    linkedin_url = validate_field(linkedin_url)

    print '\n'
    print 'Name: ' + name
    print 'Job Title: ' + job_title
    print 'School: ' + school
    print 'Location: ' + location
    print 'URL: ' + linkedin_url
    print '\n'

    writer.writerow([name.encode("utf-8"),
                     job_title.encode("utf-8"),
                     school.encode("utf-8"),
                     location.encode("utf-8"),
                     linkedin_url.encode("utf-8")])


driver.quit()
