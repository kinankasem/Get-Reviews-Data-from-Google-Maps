from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import pandas as pd

#  WebDriver (Edge, Chrome, or Firfox) depending waht browser you use, then change sitting below:
edge_driver_path = "Web Brwoser Driver Path"
service = Service(edge_driver_path)
options = webdriver.EdgeOptions()
driver = webdriver.Edge(service=service, options=options)

#  Google Maps url for the location that you want to get data about it (Please get the full URL after you select the review tab in the location)
url = "Url of the location"
driver.get(url)

try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jftiEf"))
    )
except:
    print("❌ Did not get the Location's Data.")
    driver.quit()
    exit()

scrollable_div = driver.find_element(By.XPATH, '//div[contains(@class, "m6QErb DxyBCb kA9KIf dS8AEf")]')

last_height = 0
retries = 0
while retries < 10:
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
    time.sleep(2)
    new_height = driver.execute_script('return arguments[0].scrollHeight', scrollable_div)
    if new_height == last_height:
        retries += 1
    else:
        retries = 0
    last_height = new_height

review_blocks = driver.find_elements(By.XPATH, '//div[contains(@class, "jftiEf fontBodyMedium")]')
reviews_data = []

for block in review_blocks:
    try:
        name = block.find_element(By.CLASS_NAME, 'd4r55').text
    except:
        name = "N/A"

    try:
        review = block.find_element(By.CLASS_NAME, 'wiI7pd').text
    except:
        review = "N/A"

    try:
        rating_elem = block.find_element(By.XPATH, './/span[contains(@aria-label, "star")]')
        rating_text = rating_elem.get_attribute("aria-label")
        rating = rating_text.split(" ")[0]
    except:
        rating = "N/A"

    try:
        time_posted = block.find_element(By.CLASS_NAME, 'rsqaWe').text
    except:
        time_posted = "N/A"

    reviews_data.append((name, review, rating, time_posted))

with open("reviews.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Review', 'Rating', 'Time Posted'])
    writer.writerows(reviews_data)

df = pd.DataFrame(reviews_data, columns=["Name", "Review", "Rating", "Time Posted"])
df.to_excel("Dubai Land Department Reviews.xlsx", index=False)

print(f"✅ Done  {len(reviews_data)}   ")
driver.quit()
