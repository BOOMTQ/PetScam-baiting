from selenium import webdriver
from selenium.common import TimeoutException, ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
import time
import random

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

from fuzzywuzzy import process
from selenium.webdriver.common.by import By
import json


def find_elements_by_match(targets, element_tags=None,
                           score_threshold=70):
    if element_tags is None:
        element_tags = ['input', 'textarea', 'select', 'label', 'text']
    found_elements = {}

    # Fetch all elements once to avoid repeated calls to driver.find_elements
    elements = {tag: driver.find_elements(By.TAG_NAME, tag) for tag in element_tags}

    # Loop over each target field to find matching elements
    for target in targets:
        matched_element = None
        highest_score = 0

        # Check for matching elements by 'name', 'aria-label', 'placeholder', 'data-aid'
        for element_tag, elems in elements.items():
            # Check 'name' attribute first
            for elem in elems:
                name = elem.get_attribute('name')
                if name:
                    score = process.extractOne(target, [name])[1]
                    if score > highest_score:
                        matched_element = elem
                        highest_score = score

        # If 'name' attribute did not match well, check for 'aria-label' in labels
        if highest_score < score_threshold:
            labels = driver.find_elements(By.XPATH, "//label[@aria-label]")
            for label in labels:
                aria_label = label.get_attribute('aria-label')
                if aria_label:
                    score = process.extractOne(target, [aria_label])[1]
                    if score > highest_score:
                        # Get the corresponding input element by the 'id' that the label is for
                        elem_id = label.get_attribute('for')
                        try:
                            input_element = driver.find_element(By.ID, elem_id)
                            matched_element = input_element
                            highest_score = score
                        except NoSuchElementException:
                            # Handle the case where the element does not exist
                            print(f"No element found with ID {elem_id}")
                        break

        # Fallback to 'placeholder' and 'data-aid' attributes if needed
        if highest_score < score_threshold:
            for elem in elements.get('input', []) + elements.get('textarea', []):
                placeholder = elem.get_attribute('placeholder')
                if placeholder:
                    score = process.extractOne(target, [placeholder])[1]
                    if score > highest_score:
                        matched_element = elem
                        highest_score = score

                data_aid = elem.get_attribute('data-aid')
                if data_aid:
                    score = process.extractOne(target, [data_aid])[1]
                    if score > highest_score:
                        matched_element = elem
                        highest_score = score

        # After all checks,
        if highest_score >= score_threshold and matched_element:
            found_elements[target] = matched_element

    return found_elements


def select_random_checkbox():
    try:
        checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"], input[type="radio"]')
        interactable_checkboxes = [checkbox for checkbox in checkboxes if
                                   checkbox.is_displayed() and checkbox.is_enabled()]

        if interactable_checkboxes:
            checkbox = random.choice(interactable_checkboxes)
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, checkbox.get_attribute('id'))))
            checkbox.click()
    except TimeoutException:
        print("Timeout waiting for the checkbox to become clickable.")
    except ElementNotInteractableException:
        print("The checkbox is not interactable.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def select_random_option():
    try:
        select_elements = driver.find_elements(By.TAG_NAME, 'select')

        for select_element in select_elements:
            if select_element.is_displayed() and select_element.is_enabled():
                select_object = Select(select_element)
                wait = WebDriverWait(driver, 5)
                wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'option')))

                option_indexes = list(range(len(select_object.options)))
                if option_indexes:
                    option_indexes.pop(0)
                if option_indexes:
                    select_object.select_by_index(random.choice(option_indexes))
    except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
        print(f"An error occurred while selecting an option: {e}")


def autofill_form():
    fields_to_match = ["name", "phone number", "email", "address", "state", "city", "subject", "message", "Kitten",
                       "Puppy"]
    matched_elements = find_elements_by_match(fields_to_match)

    data = {
        "name": "John Doe",
        "phone number": "1234567890",
        "email": "john.doe@example.com",
        "address": "123 Main St",
        "state": "NY",
        "city": "New York",
        "subject": "Inquiry",
        "message": "Hi, I am interested with your pet, could you please contact me as soon as possible?",
        "Kitten": "Whiskers",
        "Puppy": "Spot"
    }

    for field_name, field_element in matched_elements.items():
        if field_element and field_name in data:
            try:
                wait = WebDriverWait(driver, timeout=5)
                wait.until(EC.visibility_of(field_element))
                field_element.send_keys(data[field_name])
            except Exception as e:
                print(f"Error interacting with field: {field_name}, error: {e}")

    select_random_checkbox()
    select_random_option()
    time.sleep(5)

    try:
        submit_button = driver.find_element(By.CSS_SELECTOR,
                                            'button[type="submit"], input[type="submit"]')
        if submit_button:
            submit_button.click()
            print("Form submitted successfully!")
        else:
            print("Submit button not found")
        # WebDriverWait(driver, 3).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "div.wpcf7-mail-sent-ok"))
        # )
        # print("Form submitted successfully!")
    except TimeoutException:
        print("Form submission failed or confirmation not found.")
    pass


def read_urls_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def write_urls_to_json(file_path, url_list):
    with open(file_path, 'w') as file:
        json.dump(url_list, file, indent=4)


driver_path = 'C:/Program Files/Google/Chrome/Application/chromedriver.exe'
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

if __name__ == '__main__':

    # urls = ['http://localhost:8080/RoyalBoxersHome.html',
    # 'http://localhost:8080/AmericanBullyPuppyParadise.html', 'http://localhost:8080/ShiraDachshunds.html',]

    input_file = 'urls/input_urls.json'
    urls = read_urls_from_json(input_file)

    success_urls = []
    fail_urls = []

    for url in urls:
        try:
            driver.get(url)
            autofill_form()
            success_urls.append(url)  # 如果没有异常发生，则添加到成功列表
            time.sleep(3)
        except Exception as e:
            print(f"An error occurred with {url}: {e}")
            fail_urls.append(url)  # 如果有异常发生，则添加到失败列表
            continue

    driver.quit()

    success_file = 'urls/success_urls.json'
    fail_file = 'urls/fail_urls.json'
    write_urls_to_json(success_file, success_urls)
    write_urls_to_json(fail_file, fail_urls)
