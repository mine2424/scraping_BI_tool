
import random
import requests
from tqdm import tqdm
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome import service as fs
from selenium import webdriver
from bs4 import BeautifulSoup
import time

from models.spec_table import SpecTable


class ScrapingDataService:
    def __init__(self) -> None:
        pass

    random_seconds = random.uniform(0.234, 2.637)

    def init_BeautifulSoup(self, url: str):
        res = requests.get(url)
        res.encoding = res.apparent_encoding
        return BeautifulSoup(res.text, 'html.parser')

    def init_selenium(self):
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

    def get_all_makers(self):
        all_maker_url = []
        all_maker_name = []
        init_req = self.init_BeautifulSoup('https://kakaku.com/kuruma/maker/')
        maker_url = init_req.find_all(
            'dd', 'p-side_list_item c-icon_linkArrow p-side_list_item--maker')

        for i, maker in enumerate(maker_url):
            if i < 5:
                all_maker_url.append(maker.find('a').get('href'))
                all_maker_name.append(maker.get_text().strip())

        print(f'get_all_makers passed')
        return {'all_maker_name': all_maker_name, 'all_maker_url': all_maker_url}

    def get_all_vehicle_type(self, all_maker_url: list):
        all_vehicle_type_url = []
        all_vehicle_type_name = []
        for i, maker_url in enumerate(tqdm(all_maker_url)):
            # TODO: remove i < 10
            if i < 10:
                time.sleep(2)
                init_req = self.init_BeautifulSoup(maker_url)
                all_vehicle_type = init_req.find_all(
                    'li', 'p-side_toggle_item'
                )
                for i, body_type in enumerate(all_vehicle_type):
                    url = body_type.find('a').get('href')
                    all_vehicle_type_url.append(url)
                    all_vehicle_type_name.append(body_type.get_text())

        print(f'get_all_vehicle_type passed')
        return {'all_vehicle_type_name': all_vehicle_type_name, 'all_vehicle_type_url': all_vehicle_type_url}

    def get_all_grade_name(self, all_vehicle_type_url: list):
        all_grade_name_url = []
        all_grade_name = []
        for i, vehicle_type_url in enumerate(tqdm(all_vehicle_type_url)):
            # TODO: remove i < 10
            if i < 10:
                time.sleep(2)

                browser = self.init_selenium()
                browser.get(vehicle_type_url)

                if len(browser.find_elements(by=By.ID, value='specTblParts')) > 0:
                    iframe = browser.find_element(
                        by=By.ID, value='specTblParts'
                    )
                    browser.switch_to.frame(iframe)
                    all_vehicle_type = browser.find_element(
                        by=By.CLASS_NAME, value='gradeName'
                    )
                    all_grade_name_url.append(
                        all_vehicle_type.get_attribute('href')
                    )
                    all_grade_name.append(all_vehicle_type.text)
                    browser.close()

        print(f'get_all_grade_name passed')
        return {'all_grade_name': all_grade_name, 'all_grade_name_url': all_grade_name_url}

    def get_spec_detail(self, grade_name_url: list) -> list:
        all_spec_details = []

        init_req = self.init_BeautifulSoup(grade_name_url)
        spec_detail = init_req.find(id='specDetail')
        # thはtitle, tdはvalue
        all_table = spec_detail.find_all('tr')

        for table in all_table:
            title = table.find('th')
            value = table.find('td')
            if title is None or value is None:
                continue

            all_spec_details.append(
                SpecTable(title=title.get_text(), value=value.get_text())
            )

        return all_spec_details
