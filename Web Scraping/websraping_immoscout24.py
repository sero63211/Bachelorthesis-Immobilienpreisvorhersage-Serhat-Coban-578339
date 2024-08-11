import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service


# Funktion zur CAPTCHAs-Umgehung
def wait_and_click_captcha(driver):
    try:
        print("Waiting for CAPTCHA...")
        captcha_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".geetest_radar_tip"))
        )
        captcha_button.click()
        print("CAPTCHA clicked.")
        time.sleep(5)
    except TimeoutException:
        print("CAPTCHA not found or not clickable within the timeout period.")


# Funktion zum Expandieren aller gruppierten Immobilienangebote
def expand_all_grouped_listings(driver):
    print("Starting to expand all grouped listings...")
    last_check = False

    while True:
        expand_buttons = driver.find_elements(By.CSS_SELECTOR, ".padding-left-none.link-text-secondary.button")
        if not expand_buttons and not last_check:
            print("No expand buttons found, re-checking after a pause...")
            time.sleep(1)
            last_check = True
            continue
        elif not expand_buttons and last_check:
            print("No more expand buttons found after final check.")
            break

        last_check = False
        for button in expand_buttons:
            if button.is_displayed() and button.is_enabled():
                driver.execute_script("arguments[0].click();", button)
                print("Button clicked.")
        time.sleep(0.5)

    print("Checked and expanded grouped listings where possible.")
    return True


# Funktion zur sicheren Element-Suche
def find_element_safe(driver, by, value, fallback_selector=None):
    try:
        return driver.find_element(by, value).text
    except NoSuchElementException:
        if fallback_selector:
            try:
                return driver.find_element(By.CSS_SELECTOR, fallback_selector).text
            except NoSuchElementException:
                return "nil"
        else:
            return "nil"


# Funktion zur Extraktion der Immobiliendetails
def extract_details(driver):
    try:
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.is24-ex-details")))
    except TimeoutException:
        print("Timeout beim Laden der Details. Überprüfe den Selector oder die Internetverbindung.")
        return None

    details = {
        'title': find_element_safe(driver, By.CSS_SELECTOR, "h1[data-qa='expose-title']"),
        'price': find_element_safe(driver, By.CSS_SELECTOR, "div.is24qa-kaufpreis-main span", "span.is24-preis-value"),
        'address': find_element_safe(driver, By.CSS_SELECTOR, "span[data-qa='is24-expose-address'] div.address-block"),
        'rooms': find_element_safe(driver, By.CSS_SELECTOR, "div.is24qa-zi-main"),
        'living_space': find_element_safe(driver, By.CSS_SELECTOR, "dd.is24qa-wohnflaeche-ca"),
        'property_area': find_element_safe(driver, By.CSS_SELECTOR, "dd.is24qa-grundstueck-ca"),
        'price_per_m2': find_element_safe(driver, By.CSS_SELECTOR, "dd.is24qa-preism²"),
        'type': find_element_safe(driver, By.CSS_SELECTOR, "dd.is24qa-typ"),
        'usable_area': find_element_safe(driver, By.CSS_SELECTOR, "dd.is24qa-nutzflaeche-ca"),
        'available_from': find_element_safe(driver, By.CSS_SELECTOR, "dd.is24qa-bezugsfrei-ab"),
        'bedrooms': find_element_safe(driver, By.CSS_SELECTOR, "dd.is24qa-schlafzimmer"),
        'bathrooms': find_element_safe(driver, By.CSS_SELECTOR, "dd.is24qa-badezimmer"),
        'garage_parking': find_element_safe(driver, By.CSS_SELECTOR, "dd.is24qa-garage-stellplatz"),
        'buyer_commission': find_element_safe(driver, By.CSS_SELECTOR, "dd.is24qa-provision"),
    }

    criteria_spans = driver.find_elements(By.CSS_SELECTOR, "span[class^='is24qa']")
    criteria = {span.get_attribute('class').split()[0]: span.text.strip() for span in criteria_spans}
    details['criteriagroup_boolean_listing'] = criteria

    print(f"Details extracted: {details}")
    return details


# Funktion zur Sammlung aller Immobilienlinks
def collect_all_links(driver):
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-exp-id]'))
    )

    links = []
    selectors = [
        "a[data-exp-id][data-exp-referrer='RESULT_LIST_LISTING']",
        "a[data-exp-id][data-exp-referrer='RESULT_LIST_GROUPED']",
        "a[data-exp-id][data-exp-referrer='RESULT_LIST_LISTING_HOMEBUILDER_GROUPED']"
    ]

    for selector in selectors:
        link_elements = driver.find_elements(By.CSS_SELECTOR, selector)
        for link_element in link_elements:
            link = link_element.get_attribute('href')
            if link and not link.startswith("http"):
                link = "https://www.immobilienscout24.de" + link
            if link not in links:
                links.append(link)

    print(f"Total links collected: {len(links)}")
    return links


# Funktion zur Bestimmung der Gesamtseitenanzahl
def get_total_pages(driver):
    retry_attempts = 0
    max_retries = 2
    while retry_attempts <= max_retries:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.reactPagination')))
            pagination_links = driver.find_elements(By.CSS_SELECTOR, 'ul.reactPagination li:not(.p-prev):not(.p-next) a')
            pages_numbers = [link.text for link in pagination_links if link.text.isdigit()]
            max_page = max(map(int, pages_numbers)) if pages_numbers else 1
            print(f"Total pages found: {max_page}")
            return max_page
        except Exception as e:
            print(f"Error fetching pagination info on attempt {retry_attempts}: {e}")
            time.sleep(2)
            retry_attempts += 1
    print("Failed to find pagination after all retries.")
    return 1


# Hauptprogramm zur Ausführung des Scraping-Vorgangs
def main(locations, start_page=1):
    service = Service(executable_path="./chromedriver/chromedriver")
    driver = webdriver.Chrome(service=service)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")
    for location in locations:
        current_page = start_page
        is_first_iteration = True
        driver.get(get_url(location, current_page))
        if is_first_iteration:
            wait_and_click_captcha(driver)
            total_pages = get_total_pages(driver)
            is_first_iteration = False
        while current_page <= total_pages:
            print(f"Accessing {location} page {current_page}...")
            if current_page != start_page:
                driver.get(get_url(location, current_page))
            if expand_all_grouped_listings(driver):
                links = collect_all_links(driver)
                all_data = []
                for link in links:
                    driver.get(link)
                    details = extract_details(driver)
                    all_data.append(details)
                save_data_to_csv(all_data, location, current_page)
            current_page += 1
    driver.quit()
    print("Data collection complete.")


# Funktion zur URL-Generierung
def get_url(location, page_number=1):
    return f"https://www.immobilienscout24.de/Suche/de/{location}/haus-kaufen?pagenumber={page_number}"


# Funktion zum Speichern der Daten in eine CSV-Datei
def save_data_to_csv(all_data, location, current_page):
    with open(f'HAUS_property_data_{location}_page_{current_page}.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=all_data[0].keys())
        writer.writeheader()
        writer.writerows(all_data)
    print(f"Data for {location}, page {current_page} saved to CSV.")


locations = ['baden-wuerttemberg', 'bayern', 'berlin', 'brandenburg', 'bremen', 'hamburg',
             'hessen', 'mecklenburg-vorpommern', 'niedersachsen', 'nordrhein-westfalen',
             'rheinland-pfalz', 'saarland', 'sachsen', 'sachsen-anhalt', 'schleswig-holstein', 'thueringen']

main(locations)
