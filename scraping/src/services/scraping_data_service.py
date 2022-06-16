
from models.spec_table import SpecTable
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from tqdm import tqdm
import random
import requests
import concurrent.futures


class ScrapingDataService:
    def __init__(self) -> None:
        pass

    random_seconds = random.uniform(0.234, 1.000)

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
        """
            全国産の自動車メーカーのurlを取得する
        """

        all_maker_url = []
        all_maker_name = []
        init_req = self.init_BeautifulSoup('https://kakaku.com/kuruma/maker/')
        maker_url = init_req.find_all(
            'dd', 'p-side_list_item c-icon_linkArrow p-side_list_item--maker')

        for i, maker in enumerate(maker_url):
            all_maker_url.append(maker.find('a').get('href'))
            all_maker_name.append(maker.get_text().strip())

        print(f'get_all_makers passed')
        return {'all_maker_name': all_maker_name, 'all_maker_url': all_maker_url}

    def get_all_vehicle_type(self, all_maker_url: list):
        """
           各自動車メーカーの自動車種別のurlと車種名（アクア、カローラ）を取得する
        """

        all_vehicle_type_url = []
        all_vehicle_type_name = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i, maker_url in enumerate(tqdm(all_maker_url)):
                time.sleep(self.random_seconds)
                init_req = executor.submit(self.init_BeautifulSoup, maker_url)
                if init_req.result() is None:
                    continue

                all_vehicle_type = init_req.result().find_all(
                    'li', 'p-side_toggle_item'
                )
                for i, body_type in enumerate(all_vehicle_type):
                    url = body_type.find('a').get('href')
                    all_vehicle_type_url.append(url)
                    all_vehicle_type_name.append(body_type.get_text())

        print(f'get_all_vehicle_type passed')
        return {'all_vehicle_type_name': all_vehicle_type_name, 'all_vehicle_type_url': all_vehicle_type_url}

    def get_all_grade_name(self, all_vehicle_type_url: list):
        """
            各自動車種別の自動車グレードのurlとグレード名を取得する
        """

        all_grade_name_url = []
        all_grade_name = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i, vehicle_type_url in enumerate(tqdm(all_vehicle_type_url)):
                if i < 10:
                    time.sleep(0.5)

                    browserResult = executor.submit(self.init_selenium)
                    if browserResult.result() is None:
                        continue
                    browser = browserResult.result()
                    browser.set_page_load_timeout(20)

                    try:
                        browser.get(vehicle_type_url)
                        # executor.submit(browser.get, vehicle_type_url)

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
                        else:
                            # 0件の場合は空白を挿入できるようにしたい
                            # TODO: urlが空白の場合の他のメソッドの対応
                            # all_grade_name_url.append('')
                            # all_grade_name.append('')
                            browser.close()
                    except Exception as e:
                        print(f"time out!: {e}")

        print(f'get_all_grade_name passed')
        return {'all_grade_name': all_grade_name, 'all_grade_name_url': all_grade_name_url}

    def get_spec_detail(self, grade_name_url) -> list:
        """
            各自動車グレードのスペック・仕様を取得する
        """

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

        # TODO: もっといいアルゴリズムがあるはず
        # これはあくまで応急処置、
        # 本当はget_all_grade_nameのif len(browser.find_elements(by=By.ID, value='specTblParts')) > 0:
        # のelse部分空白を挿入すべき？
        for i, all_spec_detail in enumerate(all_spec_details):
            if all_spec_detail.value == '電気':
                # 所定の場所から３ます空白を挿入する
                all_spec_details.insert(
                    i + 2, SpecTable(title='', value=''))
                all_spec_details.insert(
                    i + 3, SpecTable(title='', value=''))
                all_spec_details.insert(
                    i + 4, SpecTable(title='', value=''))
                all_spec_details.insert(
                    i + 8, SpecTable(title='', value=''))
                all_spec_details.insert(
                    i + 9, SpecTable(title='', value=''))
                all_spec_details.insert(
                    i + 10, SpecTable(title='', value=''))
                all_spec_details.insert(
                    i + 11, SpecTable(title='', value=''))
                all_spec_details.insert(
                    i + 12, SpecTable(title='', value=''))
                all_spec_details.insert(
                    i + 13, SpecTable(title='', value=''))
            # TODO: ここでbreakしても大丈夫？
            # break

        return all_spec_details
