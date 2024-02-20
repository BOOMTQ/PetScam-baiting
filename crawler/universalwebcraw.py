from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
import time
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

driver_path = 'C:/Program Files/Google/Chrome/Application/chromedriver.exe'
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

url = 'http://localhost:8080/ContactUsPomeranian.html'
driver.get(url)

name_patterns = ['name', 'full_name', 'your-name']
email_patterns = ['email', 'e-mail', 'your-email']
phone_patterns = ['phone', 'telephone', 'your-phone', 'phone-number']
address_patterns = ['address', 'city', 'postcode', 'your-address']
pet_interest_patterns = ['puppy', 'kitten']
delivery_patterns = ['delivery', 'delivery_type', 'Delivery_type']
message_patterns = ['message', 'your-message']


def find_element_by_patterns(patterns, element_tag='input'):
    for pattern in patterns:
        if element_tag == 'input':
            elements = driver.find_elements(By.CSS_SELECTOR, f'input[name*="{pattern}"],textarea[name*="{pattern}"]')
        else:
            elements = driver.find_elements(By.CSS_SELECTOR, f'{element_tag}[name*="{pattern}"]')
        if elements:
            return elements[0]
    return None


def select_random_option(select_element):
    options = [option for option in select_element.options if option.get_attribute("value")]
    if options[0].text.strip() in ("—Please choose an option—", ""):
        options.pop(0)
    random_option = random.choice(options)
    select_element.select_by_visible_text(random_option.text)


pet_interest_select = Select(find_element_by_patterns(pet_interest_patterns, 'select'))
select_random_option(pet_interest_select)

delivery_select = Select(find_element_by_patterns(delivery_patterns, 'select'))
select_random_option(delivery_select)

name_field = find_element_by_patterns(name_patterns)
email_field = find_element_by_patterns(email_patterns)
phone_field = find_element_by_patterns(phone_patterns)
address_field = find_element_by_patterns(address_patterns)
message_field = find_element_by_patterns(message_patterns)

if name_field:
    name_field.send_keys('Jason')
if email_field:
    email_field.send_keys('Jason@example.com')
if phone_field:
    phone_field.send_keys('123-456-7890')
if address_field:
    address_field.send_keys('London')
if message_field:
    message_field.send_keys('I really like your pet, could you please contact me as soon as possible?')

time.sleep(3)

submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"], button[type="submit"]')
if submit_button:
    submit_button.click()
else:
    print("Submit button not found")


try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.wpcf7-mail-sent-ok"))
    )
    print("Form submitted successfully!")
except TimeoutException:
    print("Form submission failed or confirmation not found.")


driver.quit()
