import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.support.ui import WebDriverWait


class SpecTable:
    def __init__(self, title, value):
        self.title = title
        self.value = value


def request_html_parse(url: str):
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    return BeautifulSoup(res.text, 'html.parser')


def init_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("start-maximized")
    options.add_argument("enable-automation")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument('--disable-extensions')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-gpu")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)

    chrome_service = fs.Service(executable_path='../chromedriver')
    return webdriver.Chrome(service=chrome_service, options=options)


def get_all_makers() -> list:
    all_maker_url = []
    init_req = request_html_parse('https://kakaku.com/kuruma/maker/')
    maker_url = init_req.find_all(
        'dd', 'p-side_list_item c-icon_linkArrow p-side_list_item--maker')

    for maker in maker_url:
        all_maker_url.append(maker.find('a').get('href'))

    print(f'get_all_makers passed')
    return all_maker_url


def get_all_vehicle_type(all_maker_url: list) -> list:
    all_vehicle_type_url = []
    for i, maker_url in enumerate(all_maker_url):
        # TODO: remove i < 10
        if i < 10:
            time.sleep(2)
            init_req = request_html_parse(maker_url)
            all_vehicle_type = init_req.find_all('li', 'p-side_toggle_item')
            for i, body_type in enumerate(all_vehicle_type):
                url = body_type.find('a').get('href')
                all_vehicle_type_url.append(url)

    print(f'get_all_vehicle_type passed')
    return all_vehicle_type_url


def get_all_grade_name(all_vehicle_type_url: list) -> list:
    all_grade_name_url = []
    for i, vehicle_type_url in enumerate(all_vehicle_type_url):
        if i < 10:
            time.sleep(2)

            browser = init_selenium()
            browser.get(vehicle_type_url)

            if len(browser.find_elements_by_id('specTblParts')) > 0:
                iframe = browser.find_element_by_id("specTblParts")
                browser.switch_to.frame(iframe)
                all_vehicle_type = browser.find_element_by_class_name(
                    "gradeName")
                all_grade_name_url.append(
                    all_vehicle_type.get_attribute('href'))
                browser.close()

    print(f'get_all_grade_name passed')
    return all_grade_name_url


def get_spec_details(all_grade_url: list) -> list:
    all_spec_details = []
    for i, grade_url in enumerate(all_grade_url):
        # TODO: remove i < 10
        if i < 10:
            time.sleep(2)
            init_req = request_html_parse(grade_url)
            spec_detail = init_req.find(id='specDetail')
            # thはtitle, tdはvalue
            all_table = spec_detail.find_all('tr')
            for table in all_table:
                title = table.find('th').text
                value = table.find('td').text
                print(f'title: {title}, value: {value}')
                all_spec_details.append(SpecTable(title=title, value=value))

    print(f'get_spec_details passed')
    return all_spec_details


all_maker = get_all_makers()

all_vehicle_type = get_all_vehicle_type(all_maker)

all_grade_name = get_all_grade_name(all_vehicle_type)

spec_details = get_spec_details(all_grade_name)
