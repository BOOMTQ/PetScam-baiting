import queue
import threading
import traceback

from selenium import webdriver
from selenium.common import TimeoutException, ElementNotInteractableException
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
from responder.Message_Replier import investigator, newbies, bargainer, impatient_consumer
from rate_calculate.calculator import calculate_success_rate
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

# 启用Chrome的日志记录
capabilities = DesiredCapabilities.CHROME
capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
chrome_options = Options()
# 启用日志记录
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
driver_path = 'C:/Program Files/Google/Chrome/Application/chromedriver.exe'
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

sol_index = 0
sols = [investigator, newbies, bargainer, impatient_consumer]

jsScript = """
(function() {
    var originalSend = XMLHttpRequest.prototype.send;
    var originalOpen = XMLHttpRequest.prototype.open;

    XMLHttpRequest.prototype.open = function(method, url) {
        this._method = method;
        this._url = url;
        return originalOpen.apply(this, arguments);
    };

    XMLHttpRequest.prototype.send = function(body) {
        this._body = JSON.stringify(body); // Keep a copy of the request body

        this.onreadystatechange = () => {
            if (this.readyState === 4) { // Request Completion
                var data = {
                    method: this._method,
                    url: this._url,
                    status: this.status,
                    statusText: this.statusText,
                    requestHeaders: this.getAllResponseHeaders(),
                    requestBody: this._body, // Use the saved copies
                    responseBody: this.responseText
                };
                var existingData = JSON.parse(localStorage.getItem('interceptedData') || '[]');
                existingData.push(data);
                localStorage.setItem('interceptedData', JSON.stringify(existingData));
            }
        };
        return originalSend.apply(this, arguments);
    };
})();

"""


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
                "data-name": ["name", "full name", "first name", "your name", "names", "your-name"],
                "placeholder": ["name", "full name", "first name", "your name", "names", "your name.",
                                "your full name"],
                "name": ["name", "full name", "first name", "your name", "names", "your-name"],
                "id": ["name", "full name", "first name", "your name", "names"]
            }
        },
        "last name": {
            "element": "input",
            "require": {
                "type": "text"
            },
            "options": {
                "data-name": ["last name", "surname", "family name"],
                "placeholder": ["last name", "surname", "family name"],
                "name": ["last name", "surname", "family name"],
                "id": ["last name", "surname", "family name"]
            }
        },
        "phone number": {
            "element": "input",
            "options": {
                "type": ["tel", "number"],
                "data-name": ["phone", "phone number", "number", "your phone", "your phone number", "telephone", "tel",
                              "your-number", "cell phone number", "cell phone", "mobile", "mobile number", "cellphone"],
                "placeholder": ["phone", "phone number", "your phone", "your phone number", "number", "telephone",
                                "tel", "your-number", "cell phone number", "cell phone", "mobile", "mobile number", "cellphone"],
                "name": ["phone", "phone number", "number", "your phone", "your phone number", "telephone", "tel",
                         "your-number", "cell phone number", "cell phone", "mobile", "mobile number", "cellphone"],
                "id": ["phone", "phone number", "number", "your phone", "your phone number", "telephone", "tel",
                       "cell phone number", "cell phone", "mobile", "mobile number", "cellphone"]
            }
        },
        "email": {
            "element": "input",
            "options": {
                "type": "email",
                "data-name": ["e-mail", "email", "email address", "enter email"],
                "placeholder": ["e-mail", "email", "email address", "your email", "enter email"],
                "name": ["e-mail", "email", "email address"],
                "id": ["e-mail", "email", "email address"]
            }
        },
        "address": {
            "element": "input",
            "require": {
                "type": "text"
            },
            "options": {
                "data-name": ["address", "your address", "home address", "residential address", "location",
                              "location address", "your location"],
                "placeholder": ["address", "your address", "home address", "residential address", "location",
                                "location address", "your location"],
                "name": ["address", "your address", "home address", "residential address", "location",
                         "location address", "your location"],
                "id": ["address", "your address", "home address", "residential address", "location",
                       "location address", "your location"]
            }
        },
        "state": {
            "element": "input",
            "require": {
                "type": "text"
            },
            "options": {
                "data-name": ["state/city", "state", "state / city", "city/state", "city / state", "your state"
                                                                                                   "state / address",
                              "location/state", "state/location", "your-state", "your-cs"],
                "placeholder": ["state/city", "state", "state / city", "city/state", "city / state",
                                "state / address", "location/state", "state/location", "your state"],
                "name": ["state/city", "state", "state / city", "city/state", "city / state",
                         "state / address", "location/state", "state/location", "your state"],
                "id": ["state/city", "state", "state / city", "city/state", "city / state",
                       "state / address", "location/state", "state/location", "your state"]
            }
        },
        "city": {
            "element": "input",
            "require": {
                "type": "text"
            },
            "options": {
                "data-name": ["city", "city / address", "province", "city / province", "province / city",
                              "province/city", "city/province", "location/city", "city/location", "your city"],
                "placeholder": ["city", "city / address", "province", "city / province", "province / city",
                                "province/city", "city/province", "location/city", "city/location", "your city"],
                "name": ["city", "city / address", "province", "city / province", "province / city",
                         "province/city", "city/province", "location/city", "city/location", "your city"],
                "id": ["city", "city / address", "province", "city / province", "province / city",
                       "province/city", "city/province", "location/city", "city/location", "your city"]
            }
        },
        "subject": {
            "element": "input",
            "require": {
                "type": "text"
            },
            "options": {
                "data-name": ["subject", "subject type", "type of subject", "your-subject"],
                "placeholder": ["subject", "subject type", "type of subject"],
                "name": ["subject", "subject type", "type of subject"],
                "id": ["subject", "subject type", "type of subject"],
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
                "data-name": ["kitten", "name kitten", "kitten name", "nameofkitten", "your kitten name",
                              "your-petname",
                              "name of kitten", "kitten of interest", "chosen kitten!", "chosen kitten",
                              "kitten's name"],
                "placeholder": ["kitten", "name kitten", "kitten name", "nameofkitten", "your kitten name",
                                "your-petname",
                                "name of kitten", "kitten of interest", "chosen kitten!", "chosen kitten",
                                "kitten's name"],
                "name": ["kitten", "name kitten", "kitten name", "nameofkitten", "your kitten name", "your-petname",
                         "name of kitten", "kitten of interest", "chosen kitten!", "chosen kitten", "kitten's name"],
                "id": ["kitten", "name kitten", "kitten name", "nameofkitten", "your kitten name", "your-petname",
                       "name of kitten", "kitten of interest", "chosen kitten!", "chosen kitten", "kitten's name"],
            }
        },
        "Puppy": {
            "element": "input",
            "require": {
                "type": "text"
            },
            "options": {
                "data-name": ["puppy", "puppyname", "name puppy", "puppy name", "nameofpuppy", "your puppy name",
                              "your-petname",
                              "name of puppy", "puppy of interest", "chosen puppy!", "chosen puppy", "puppy's name"],
                "placeholder": ["puppy", "puppyname", "name puppy", "puppy name", "nameofpuppy", "your puppy name",
                                "your-petname",
                                "name of puppy", "puppy of interest", "chosen puppy!", "chosen puppy", "puppy's name"],
                "name": ["puppy", "puppyname", "name puppy", "puppy name", "nameofpuppy", "your puppy name",
                         "your-petname",
                         "name of puppy", "puppy of interest", "chosen puppy!", "chosen puppy", "puppy's name"],
                "id": ["puppy", "puppyname", "name puppy", "puppy name", "nameofpuppy", "your puppy name",
                       "your-petname",
                       "name of puppy", "puppy of interest", "chosen puppy!", "chosen puppy", "puppy's name"],
            }
        },
        "Dog Breed": {
            "element": "input",
            "require": {
                "type": "text"
            },
            "options": {
                "data-name": ["dog breed", "dogbreed", "breed of dog", "dog breed name", "dog breedname"],
                "placeholder": ["dog breed", "dogbreed", "breed of dog", "dog breed name", "dog breedname"],
                "name": ["dog breed", "dogbreed", "breed of dog", "dog breed name", "dog breedname"],
                "id": ["dog breed", "dogbreed", "breed of dog", "dog breed name", "dog breedname"],
            }
        },
        "Cat Breed": {
            "element": "input",
            "require": {
                "type": "text"
            },
            "options": {
                "data-name": ["cat breed", "catbreed", "breed of cat", "cat breed name", "cat breedname"],
                "placeholder": ["cat breed", "catbreed", "breed of cat", "cat breed name", "cat breedname"],
                "name": ["cat breed", "catbreed", "breed of cat", "cat breed name", "cat breedname"],
                "id": ["cat breed", "catbreed", "breed of cat", "cat breed name", "cat breedname"],
            }
        }
    }
    base = driver.find_element(By.TAG_NAME, 'form')
    result = {}
    try:
        element_cache = {}
        threads = []
        share_queue = queue.Queue()
        for i, (key, value) in enumerate(tqdm(target_map.items())):
            if value["element"] not in element_cache:
                elements = base.find_elements(By.TAG_NAME, value["element"])
                element_cache[value["element"]] = elements
            else:
                elements = element_cache[value["element"]]
            thread = threading.Thread(target=parallel_worker, args=(elements, key, value, max_depth, i, share_queue))
            thread.start()
            threads.append(thread)
        for thread in tqdm(threads):
            thread.join()

        lst = []
        while not share_queue.empty():
            lst.append(share_queue.get())
        for key, value in lst:
            result[key] = value

    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred while filtering elements: {e}")

    for key, value in result.items():
        print(f"{key}: {value.get_attribute('outerHTML')}")

    return result


def parallel_worker(elements, key, value, max_depth, i, share_queue: queue.Queue):
    print(f"     Thread {i} start")
    for element in elements:
        attrs = {}
        if value.get("force", False):
            share_queue.put((key, element))
            # result[key] = element
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
            share_queue.put((key, element))
    print(f"     Thread {i} end")


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
                wait.until(lambda driver: select_element.find_elements(By.TAG_NAME, 'option'))

                options = [option for option in select_object.options if
                           option.is_enabled() and option.get_attribute('value')]

                if len(options) > 1:
                    select_object.select_by_index(random.choice(range(1, len(options))))

    except Exception as e:
        print(f"An error occurred while selecting an option: {e}")


def generate_uk_phone():
    country_code = "+44"
    number = '07' + ''.join(random.choice('0123456789') for _ in range(9))
    return f"{country_code} {number}"


def generate_us_phone():
    area_code = random.choice([201, 202, 203, 205, 206, 207, 208, 209, 210, 213, 214, 215, 216, 217, 218, 219, 220, 224,
                               225, 228, 229, 231, 234, 239, 240, 248, 251, 252, 253, 254, 256, 260, 262, 267, 269, 270,
                               272, 276, 281, 301, 302, 303, 304, 305, 307, 308, 309, 310, 312, 313, 314, 315, 316, 317,
                               318, 319, 320, 321, 323, 325, 330, 331, 334, 336, 337, 339, 346, 347, 351, 352, 360, 361,
                               364, 380, 385, 386, 401, 402, 404, 405, 406, 407, 408, 409, 410, 412, 413, 414, 415, 417,
                               419, 423, 424, 425, 430, 432, 434, 435, 440, 442, 443, 445, 447, 458, 463, 469, 470, 475,
                               478, 479, 480, 484, 501, 502, 503, 504, 505, 507, 508, 509, 510, 512, 513, 515, 516, 517,
                               907, 808])

    exchange = random.randint(200, 999)
    while exchange in [411, 555]:
        exchange = random.randint(200, 999)

    subscriber = random.randint(1000, 9999)

    # Format: +1-NXX-NXX-XXXX
    return f"+1({area_code}){exchange}{subscriber}"


def generate_uk_address():
    number = random.randint(1, 200)
    street_names = ['High', 'Church', 'London', 'Victory', 'Kings', 'Queens', 'Green']
    street_types = ['Street', 'Road', 'Way', 'Place', 'Lane']
    postcode = random.randint(10000, 99999)
    return f"{number} {random.choice(street_names)} {random.choice(street_types)}, {postcode}"


def generate_us_address():
    number = random.randint(100, 9999)
    street_names = ['Main', 'Oak', 'Pine', 'Maple', 'Cedar', 'Elm', 'Willow']
    street_types = ['St', 'Ave', 'Blvd', 'Rd', 'Dr', 'Ln']
    return f"{number} {random.choice(street_names)} {random.choice(street_types)}"


def generate_uk_city():
    cities = [
        # UK Cities
        'London', 'Birmingham', 'Manchester', 'Glasgow', 'Newcastle',
        'Sheffield', 'Liverpool', 'Leeds', 'Bristol', 'Nottingham',
        'Leicester', 'Edinburgh', 'Cardiff', 'Brighton', 'Plymouth'
    ]
    return random.choice(cities)


def generate_us_city():
    cities = [
        # US Cities
        'Springfield', 'Columbus', 'Phoenix', 'Austin', 'Jacksonville',
        'New York', 'Los Angeles', 'Chicago', 'Houston', 'San Diego',
        'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'San Francisco',
        'Indianapolis', 'Seattle', 'Denver', 'Washington', 'Boston'
    ]
    return random.choice(cities)


def generate_message():
    global sol_index
    prompt = ""
    sol = sols[sol_index]
    sol_name = sol.__name__
    message = sol(prompt)
    sol_index = (sol_index + 1) % len(sols)
    return message, sol_name


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


def save_to_cache(email, sol_name, username, url):
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

    form_filled_time = round(time.time())

    cache_data.append({
        "bait_email": email,
        "sol": sol_name,
        "username": username,
        "url": url,
        "form_filled_time": form_filled_time
    })

    with open(cache_file_path, 'w') as file:
        json.dump(cache_data, file, indent=4)


def read_urls_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def write_urls_to_json(file_path, url_list):
    with open(file_path, 'w') as file:
        json.dump(url_list, file, indent=4)


class AnyOf:  # Custom condition class: check if any of the given conditions are satisfied
    def __init__(self, *args):
        self.conditions = args

    def __call__(self, driver):
        for condition in self.conditions:
            try:
                if condition(driver):
                    return True
            except:
                continue
        return False


# Define a counter at the global scope
i = 0


def autofill_form():
    global i
    data = {}
    matched_elements = filter_elements(max_depth=2)

    email = get_random_addr()
    username = names.get_first_name()
    lastname = names.get_last_name()
    message, sol_name = generate_message()

    if i % 2 == 0:  # Even: UK data
        phone = generate_uk_phone()
        address = generate_uk_address()
        city = generate_uk_city()
    else:  # Odd: US data
        phone = generate_us_phone()
        address = generate_us_address()
        city = generate_us_city()

    data.update({
        "name": username,
        "last name": lastname,
        "phone number": phone,
        "email": email,
        "address": address,
        "state": city,
        "city": city,
        "subject": "Inquiry",
        "message": message,
        "Kitten": generate_kitten(),
        "Puppy": generate_puppy(),
        "Dog Breed": generate_dog_breed(),
        "Cat Breed": generate_kitten_breed()
    })

    for field_name, field_element in matched_elements.items():
        if field_element and field_name in data:
            try:
                wait = WebDriverWait(driver, timeout=5)
                wait.until(EC.visibility_of(field_element))
                field_element.clear()
                field_element.send_keys(data[field_name])
            except Exception as e:
                print(f"Error interacting with field: {field_name}, error: {e}")

    i += 1

    # Checkboxes and select elements
    select_random_checkbox()
    select_random_option()
    time.sleep(3)

    try:
        submit_button = driver.find_element(By.CSS_SELECTOR,
                                            'button[type="submit"], input[type="submit"]')
        if submit_button:
            driver.execute_script(jsScript)
            print("click button")
            submit_button.click()
            TIMEOUT = 10
            start = time.time()
            submission_successful = False
            print("start wait log")
            while time.time() - start < TIMEOUT:
                time.sleep(0.5)
                data = driver.execute_script("return localStorage.getItem('interceptedData');")
                if data:
                    intercepted_requests = json.loads(data)
                    for intercepted_request in intercepted_requests:
                        if intercepted_request['method'] == 'POST':
                            if intercepted_request['status'] == 200 and "fail" not in intercepted_request['responseBody']:
                                submission_successful = True
                            else:
                                break
            print("end for wait")
            if not submission_successful:
                submission_successful = WebDriverWait(driver, 10).until(AnyOf(
                    EC.url_changes(driver.current_url),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Thank you')]")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Thanks')]")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'success')]")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'was sent')]")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'has been sent')]")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'received')]")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'successful')]")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'successfully')]"))
                ))
            if submission_successful:
                current_url = driver.current_url
                save_to_cache(email, sol_name, username, current_url)
                print("Form submitted successfully!")
                return True
            else:
                current_url = driver.current_url
                save_to_cache(email, sol_name, username, current_url)
                print("Form submission might not be successful, but the info is also saved in cache.")
                return False
        else:
            print("Submit button not found")
            return False

    except TimeoutException:
        current_url = driver.current_url
        save_to_cache(email, sol_name, username, current_url)
        print("Form submission failed or confirmation not found, but the info is also saved in cache.")
    pass


def main():
    input_file = 'success/form3.json'
    urls = read_urls_from_json(input_file)
    start_time = int(time.time())

    success_urls = []
    fail_urls = []
    attempted_links = 0

    for url in urls:
        attempted_links += 1
        try:
            driver.get(url)
            if autofill_form():
                success_urls.append(url)
            else:
                fail_urls.append(url)
            time.sleep(2)
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred with {url}: {e}")
            fail_urls.append(url)
            # continue

    driver.quit()

    success_file = 'success/form-fill3.json'
    fail_file = "fail/form-fill3.json"
    write_urls_to_json(success_file, success_urls)
    write_urls_to_json(fail_file, fail_urls)

    success_rate = calculate_success_rate("formfill_crawl", success_urls, attempted_links, start_time)
    print(f"Success rate: {success_rate:.2f}%")


if __name__ == '__main__':
    main()
