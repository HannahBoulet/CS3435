import time
from selenium import webdriver
import json

from selenium.common.exceptions import NoSuchElementException



#Hannah Boulet
#none
#A work was having to go through all 8 pages to collect all the links for the attribute part. I had to wait each time
# it clicked the next page button due to if I hadn't it would not get the links for all the items on the current page.
DRIVER_PATH = '/Users/hannahboulet/Downloads/chromedriver_mac64/chromedriver'

driver = webdriver.Chrome(executable_path= DRIVER_PATH)
driver.maximize_window()
driver.get("https://shopgoodwill.com/home")
time.sleep(10)


cat = driver.find_element_by_xpath('//*[@id="navbarCategoryDropdown"]')
cat.click()
time.sleep(5)

clothing = driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/nav/ul/li[2]/div/ul/li[11]/a')
clothing.click()
time.sleep(5)

belt = driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/nav/ul/li[2]/div/ul/li[11]/ul/li[3]/a')
belt.click()
time.sleep(10)

next_button = driver.find_element_by_xpath('//button[@aria-label="Go to Next" and not(@disabled)]')
time.sleep(5)
hrefs = []
while not next_button.get_attribute('disabled'):
    try:
        next_button.click()
        time.sleep(10)
        baseTags = driver.find_elements_by_css_selector('a.feat-item_name')

        for tag in baseTags:
            hrefs.append(tag.get_attribute('href'))
        next_button = driver.find_element_by_xpath('//button[@aria-label="Go to Next" and not(@disabled)]')
    except NoSuchElementException:
        break
print(hrefs)

gwbelts =[]
for href in hrefs:
  driver.get(href)
  time.sleep(5)
  title = driver.find_element_by_css_selector('h1.mb-4.d-none.d-md-block').text.strip()
  try:
    price_element = driver.find_element_by_xpath('//div[contains(@class, "col-4") and contains(@class, "text-right")]//h3')
    currentp = price_element.get_attribute('textContent')
  except NoSuchElementException:
    price_element = driver.find_element_by_xpath('//p[@class="lead mb-0"]/span[@class="ng-star-inserted"]')
    currentp = price_element.text.strip()

  try:
        min_bid_element = driver.find_element_by_xpath('//div[contains(@class, "row") and contains(@class, "mb-3") and contains(@class, "ng-star-inserted")]//div[contains(@class, "col-4") and contains(@class, "text-right")]//p')
        min_bid = min_bid_element.get_attribute('textContent').strip()
  except NoSuchElementException:
      min_bid = "This is a buy now!"
  try:
    bids_element = driver.find_element_by_xpath('//a[contains(@aria-label, "bids")]')
    current_bids = bids_element.text
  except NoSuchElementException:
    current_bids = "This is a buy now!"

  gwbelts.append({
    'Title': title,
    'link':href,
    'Current Price': currentp,
    'Min Bid:':min_bid,
    'Current number Bids':current_bids
  })


with open('belts.jl', 'w') as f:
    json.dump(gwbelts, f, indent=4)
    f.write('\n')

driver.close()