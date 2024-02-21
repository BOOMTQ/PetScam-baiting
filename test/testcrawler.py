from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver_path = 'C:/Program Files/Google/Chrome/Application/chromedriver.exe'
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

url = 'http://localhost:8080/test.html'
driver.get(url)

time.sleep(2)

name_field = driver.find_element(By.ID, 'name')
email_field = driver.find_element(By.ID, 'email')
PhoneNumber_field = driver.find_element(By.ID, 'PhoneNumber')
city_field = driver.find_element(By.ID, 'city')
state_field = driver.find_element(By.ID, 'state')
message_field = driver.find_element(By.ID, 'message')
send_message = driver.find_element(By.XPATH, '//button[@type="submit"]')

name_field.send_keys('John Smith')
email_field.send_keys('john.smith@example.com')
PhoneNumber_field.send_keys('00000000')
city_field.send_keys('London')
state_field.send_keys('UK')
message_field.send_keys('This is a test message.')

time.sleep(5)

send_message.click()

time.sleep(5)

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "success_message"))
    )
    print("Form submitted successfully!")
except TimeoutException:
    print("Form submission failed or confirmation not found.")

driver.quit()


# import requests
# from urllib.parse import urljoin
# from bs4 import BeautifulSoup
#
# # Start a session to maintain cookies
# session = requests.Session()
#
# # URL of the page with the form
# url = ' http://127.0.0.1:8080/test'
#
# # GET request to retrieve the form
# response = session.get(url)
# print(response.text)
# soup = BeautifulSoup(response.text, 'html.parser')
#
# # Find the form action
# form = soup.find('form')
# form_action = form['action']
# submit_url = urljoin(url, form_action)  # Create the full URL for form submission
#
# # Data to submit
# form_data = {
#     'name': 'John Smith',
#     'email': 'john.smith@example.com',
#     'PhoneNumber': '00000000',
#     'city': 'London',
#     'state': 'UK',
#     'message': 'This is a test message.'
# }
#
# # POST request to submit the form
# response = session.post(submit_url, data=form_data)
#
# # Check for success
# if response.ok:
#     # Further validation may be required here to check the response content
#     print('Contact information submitted successfully.')
# else:
#     print('Failed to submit contact information.')
