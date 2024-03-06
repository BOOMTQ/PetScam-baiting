import traceback

from selenium import webdriver
from selenium.common import TimeoutException, ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
import time
import random
import names
import json
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from secret import CRAWLER_PROG_DIR

from fuzzywuzzy import process
from selenium.webdriver.common.by import By
from tqdm import tqdm
from solution_manager import get_random_addr

driver_path = 'C:/Program Files/Google/Chrome/Application/chromedriver.exe'
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)


def get_parent_element(element):
    parent_element = driver.execute_script("return arguments[0].parentNode;", element)
    return parent_element


def get_parent_element_text_iter(element, depth=2):
    if depth < 0:
        return ''
    parent_element = get_parent_element(element)
    if parent_element.text != '':
        return parent_element.text
    else:
        return get_parent_element_text_iter(parent_element, depth=depth - 1)


def get_bro_text_list_iter(element, depth=2):
    if depth < 0:
        return ['']
    parent_element = get_parent_element(element)
    result = get_bro_text_list_iter(parent_element, depth=depth - 1)
    if parent_element.text != '':
        return result + [parent_element.text]
    else:
        return result


def filter_elements(max_depth=2):
    target_map = {
        "name": {
            "element": "input",
            "require": {
                "type": "text"
            },
            "options": {
                "data-name": ["name", "full name", "first name", "last name", "your name"],
                "placeholder": ["name", "full name", "first name", "last name", "your name"],
                "name": ["name", "full name", "first name", "last name", "your name"],
                "id": ["name", "full name", "first name", "last name", "your name"]
            }
        },
        "phone number": {
            "element": "input",
            "options": {
                "type": "tel",
                "data-name": ["phone", "phone number", "number"],
                "name": ["phone", "phone number", "number"],
                "id": ["phone", "phone number", "number"]
            }
        },
        "email": {
            "element": "input",
            "options": {
                "type": "email",
                "data-name": ["E-mail", "email", "email address"],
                "placeholder": ["E-mail", "email", "email address"],
                "name": ["E-mail", "email", "email address"],
                "id": ["E-mail", "email", "email address"]
            }
        },
        "address": {
            "element": "input",
            "require": {
                "type": "text"
            },
            "options": {
                "data-name": ["address"],
                "placeholder": ["address"],
                "name": ["address"],
                "id": ["address"],
            }
        },
        "state/city": {
            "element": "input",
            "require": {
                "type": "text"
            },
            "options": {
                "data-name": ["state/city", "state", "city", "state / city", "city/state", "city / state"],
                "placeholder": ["state/city", "state", "city", "state / city", "city/state", "city / state"],
                "name": ["state/city", "state", "city", "state / city", "city/state", "city / state"],
                "id": ["state/city", "state", "city", "state / city", "city/state", "city / state"],
            }
        },
        "subject": {
            "element": "input",
            "require": {
                "type": "text"
            },
            "options": {
                "data-name": ["subject"],
                "placeholder": ["subject"],
                "name": ["subject"],
                "id": ["subject"],
            }
        },
        "message": {
            "element": "textarea",
            "force": True,
            "options": {

            }
        },
        "Kitten": {
            "element": "input",
            "require": {
                "type": "text"
            },
            "options": {
                "data-name": ["Kitten", "KittenName", "Name Kitten", "Kitten Name", "NameKitten",
                              "NameofKitten", "Name of Kitten"],
                "placeholder": ["Kitten", "KittenName", "Name Kitten", "Kitten Name", "NameKitten",
                                "NameofKitten", "Name of Kitten"],
                "name": ["Kitten", "KittenName", "Name Kitten", "Kitten Name", "NameKitten",
                         "NameofKitten", "Name of Kitten"],
                "id": ["Kitten", "KittenName", "Name Kitten", "Kitten Name", "NameKitten",
                       "NameofKitten", "Name of Kitten"],
            }
        },
        "Puppy": {
            "element": "input",
            "require": {
                "type": "text"
            },
            "options": {
                "data-name": ["Puppy", "PuppyName", "Name Puppy", "Puppy Name", "NamePuppy", "NameofPuppy",
                              "Name of Puppy"],
                "placeholder": ["Puppy", "PuppyName", "Name Puppy", "Puppy Name", "NamePuppy",
                                "NameofPuppy", "Name of Puppy"],
                "name": ["Puppy", "Name Puppy", "Puppy Name", "NamePuppy", "NameofPuppy",
                         "Name of Puppy"],
                "id": ["Puppy", "PuppyName", "Name Puppy", "Puppy Name", "PuppyName", "NamePuppy", "NameofPuppy",
                       "Name of Puppy"],
            }
        },
        "Dog Breed": {
            "element": "input",
            "require": {
                "type": "text"
            },
            "options": {
                "data-name": ["Dog Breed", "DogBreed"],
                "placeholder": ["Dog Breed", "DogBreed"],
                "name": ["Dog Breed", "DogBreed"],
                "id": ["Dog Breed", "DogBreed"],
            }
        },
        "Cat Breed": {
            "element": "input",
            "require": {
                "type": "text"
            },
            "options": {
                "data-name": ["Cat Breed", "CatBreed"],
                "placeholder": ["Cat Breed", "CatBreed"],
                "name": ["Cat Breed", "CatBreed"],
                "id": ["Cat Breed", "CatBreed"],
            }
        }
    }
    base = driver.find_element(By.TAG_NAME, 'form')
    result = {}
    try:
        for key, value in tqdm(target_map.items()):
            elements = base.find_elements(By.TAG_NAME, value["element"])
            for element in elements:
                attrs = {}
                if value.get("force", False):
                    result[key] = element
                for name, target_values in value.get("require", {}).items():
                    if element.get_attribute(name) != target_values:
                        break
                content = get_parent_element_text_iter(element, depth=max_depth)
                bro_content = get_bro_text_list_iter(element, depth=max_depth - 1)
                bro_content += [content]
                for name, target_values in value["options"].items():
                    if len(attrs.keys()) > 0:
                        break
                    if type(target_values) == str:
                        target_values = [target_values]
                    for target_value in target_values:
                        v = element.get_attribute(name)
                        if v is not None and (
                                target_value.lower() == v.lower() or (target_value.lower() in v.lower() and len(
                            v.lower().replace(target_value.lower(), '').replace(' ', '')) < 3)):
                            attrs[name] = v
                            break
                        for c in bro_content:
                            if c is not None and len(c) > 0:
                                score = process.extractOne(target_value.lower(), [c.lower()])[1]
                                if score > 90:
                                    attrs[name] = c
                                    print(f"parent text: {c} / {target_value} with score {score}")
                                    break

                if len(attrs.keys()) > 0:
                    result[key] = element
                    break
    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred while filtering elements: {e}")

    for key, value in result.items():
        print(f"{key}: {value.get_attribute('outerHTML')}")

    return result


def select_random_checkbox():
    try:
        checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"], input[type="radio"]')
        interactable_checkboxes = [checkbox for checkbox in checkboxes if
                                   checkbox.is_displayed() and checkbox.is_enabled()]

        if interactable_checkboxes:
            checkbox = random.choice(interactable_checkboxes)
            WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, checkbox.get_attribute('id'))))
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
                wait = WebDriverWait(driver, 4)
                wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'option')))

                option_indexes = list(range(len(select_object.options)))
                if option_indexes:
                    option_indexes.pop(0)
                if option_indexes:
                    select_object.select_by_index(random.choice(option_indexes))
    except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
        print(f"An error occurred while selecting an option: {e}")


def generate_phone():  # phone range include European countries and US
    # EU or US format
    if random.choice([True, False]):
        # EU format (country code + area code + local number)
        country_code = random.choice(
            ['+49', '+33', '+39', '+34', '+48', '+44', '+31', '+32', '+46', '+47', '+358'])  # country codes
        area_code = random.randint(100, 999)
        local_number = random.randint(1000, 9999)
        return f"{country_code} {area_code} {local_number}"
    else:
        # US format (3-digit area code + 3-digit exchange code + 4-digit subscriber number)
        area_code = random.randint(200, 999)
        exchange = random.randint(200, 999)
        subscriber = random.randint(1000, 9999)
        return f"({area_code}) {exchange}-{subscriber}"


def generate_address():  # address range include European countries and US
    # EU
    if random.choice([True, False]):
        number = random.randint(1, 200)
        street_names = ['High', 'Church', 'London', 'Victory', 'Kings', 'Queens', 'Green']
        street_types = ['Street', 'Road', 'Way', 'Place', 'Lane']
        postcode = random.randint(10000, 99999)
        return f"{number} {random.choice(street_names)} {random.choice(street_types)}, {postcode}"
    else:
        # US
        number = random.randint(100, 9999)
        street_names = ['Main', 'Oak', 'Pine', 'Maple', 'Cedar', 'Elm', 'Willow']
        street_types = ['St', 'Ave', 'Blvd', 'Rd', 'Dr', 'Ln']
        return f"{number} {random.choice(street_names)} {random.choice(street_types)}"


def generate_city():  # real city names in EU and US
    cities = [
        'Springfield', 'Columbus', 'Phoenix', 'Austin', 'Jacksonville',  # US Cities
        'Berlin', 'Munich', 'Hamburg',  # German Cities
        'Paris', 'Marseille', 'Lyon',  # French Cities
        'Rome', 'Milan', 'Naples',  # Italian Cities
        'Madrid', 'Barcelona', 'Valencia',  # Spanish Cities
        'Warsaw', 'Krakow', 'Wroclaw',  # Polish Cities
        'London', 'Birmingham', 'Manchester',  # UK Cities
        'Amsterdam', 'Rotterdam', 'The Hague',  # Dutch Cities
        'Brussels', 'Antwerp', 'Bruges',  # Belgian Cities
        'Stockholm', 'Gothenburg', 'Malmö',  # Swedish Cities
        'Oslo', 'Bergen', 'Trondheim',  # Norwegian Cities
        'Helsinki', 'Espoo', 'Tampere',  # Finnish Cities
    ]
    return random.choice(cities)


def generate_kitten():
    kittenname = ['SNOW', 'CHLOE', 'KIARA', 'WINSTON', 'NEO', 'ELINA', 'RUBY', 'RIVER', 'Chleo', 'Luke', 'Ella', 'Joy',
                  'Nick', 'Joel', 'Platon', 'Brie', 'Ozzy']
    return random.choice(kittenname)


def generate_puppy():
    puppyname = ['ELENA', 'NORA', 'AMELIA', 'SALLY', 'OZEN', 'LEO', 'CARL', 'MARK', 'Emma', 'SUSU', 'SOPHIE', 'LAURA',
                 'MACKO', 'TERRO', 'PRINCE', 'WILLY', 'LOVI', 'JAX', 'SUZY', 'MAX']
    return random.choice(puppyname)


def generate_dog_breed():
    breed = ['French Bulldog', 'Pomeranian', 'Siberian Husky', 'Akita Inu', 'Labrador Retriever', 'German Shepherd',
             'Golden Retriever', 'Beagle', 'Poodle', 'Dachshund', 'Doberman Pinscher', 'Australian Shepherd']
    return random.choice(breed)


def generate_kitten_breed():
    breed = ['Chinese Li Hua', 'Persian', 'Siamese', 'Bengal', 'British Shorthair', 'Maine Coon', 'Ragdoll',
             'Scottish Fold',
             'Sphynx', 'Russian Blue', 'Norwegian Forest Cat', ]
    return random.choice(breed)


def save_to_cache(email, username, url):
    cache_file_path = CRAWLER_PROG_DIR
    if not os.path.exists(os.path.dirname(cache_file_path)):
        os.makedirs(os.path.dirname(cache_file_path))

    cache_data = []
    if os.path.exists(cache_file_path):
        with open(cache_file_path, 'r') as file:
            try:
                cache_data = json.load(file)
                if not isinstance(cache_data, list):
                    raise ValueError("Cache data is not a list")
            except json.JSONDecodeError:
                cache_data = []

    cache_data.append({
        "bait_email": email,
        "username": username,
        "url": url
    })

    with open(cache_file_path, 'w') as file:
        json.dump(cache_data, file, indent=4)


def read_urls_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def write_urls_to_json(file_path, url_list):
    with open(file_path, 'w') as file:
        json.dump(url_list, file, indent=4)


def autofill_form():
    data = {}
    fields_to_match = ["name", "phone number", "email", "address", "state", "city", "state/city", "subject", "message",
                       "Kitten", "Puppy", "Dog Breed", "Cat Breed"]
    matched_elements = filter_elements()

    email = get_random_addr()
    username = names.get_first_name()

    data.update({
        "name": username,
        "phone number": generate_phone(),
        "email": email,
        "address": generate_address(),
        "subject": "Inquiry",
        "message": "Hi, I am interested with your pet, could you please contact me as soon as possible?",  # use gpt API
        "Kitten": generate_kitten(),
        "Puppy": generate_puppy(),
        "Dog Breed": generate_dog_breed(),
        "Cat Breed": generate_kitten_breed()
    })

    # Check if the form has "state/city" combined field
    if "state/city" in fields_to_match:
        data["state/city"] = generate_city()  # Call only generate_random_city
    else:
        data["state"] = generate_city()
        data["city"] = generate_city()

    for field_name, field_element in matched_elements.items():
        if field_element and field_name in data:
            try:
                wait = WebDriverWait(driver, timeout=4)
                wait.until(EC.visibility_of(field_element))
                field_element.send_keys(data[field_name])
            except Exception as e:
                print(f"Error interacting with field: {field_name}, error: {e}")

    select_random_checkbox()
    select_random_option()
    time.sleep(4)

    try:
        submit_button = driver.find_element(By.CSS_SELECTOR,
                                            'button[type="submit"], input[type="submit"]')
        if submit_button:
            submit_button.click()
            current_url = driver.current_url
            save_to_cache(username, email, current_url)
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.wpcf7-mail-sent-ok"))
            )
            print("Form submitted successfully!")
        else:
            print("Submit button not found")

    except TimeoutException:
        print("Form submission failed or confirmation not found.")
    pass


if __name__ == '__main__':
    input_file = 'urls/input_urls.json'
    urls = read_urls_from_json(input_file)

    success_urls = []
    fail_urls = []

    for url in urls:
        try:
            driver.get(url)
            autofill_form()
            success_urls.append(url)
            time.sleep(2)
        except Exception as e:
            print(f"An error occurred with {url}: {e}")
            fail_urls.append(url)
            continue

    driver.quit()

    success_file = 'urls/success_urls.json'
    fail_file = 'urls/fail_urls.json'
    write_urls_to_json(success_file, success_urls)
    write_urls_to_json(fail_file, fail_urls)
