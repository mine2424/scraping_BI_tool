import random
import time
import concurrent.futures

from tqdm import tqdm
from services.openpyxl_service import OpenpyxlService

from services.scraping_data_service import ScrapingDataService


def main():
    scraping_data_service = ScrapingDataService()
    openpyxl_service = OpenpyxlService()

    ### スクレイピングしてデータを取得する実装 ###

    # data: {'all_maker_name': ['ホンダ'], 'all_maker_url': all_maker_url}
    all_maker = scraping_data_service.get_all_makers()

    # data: {'all_vehicle_type_name': all_vehicle_type_name, 'all_vehicle_type_url': all_vehicle_type_url}
    all_vehicle_type = scraping_data_service.get_all_vehicle_type(
        all_maker['all_maker_url']
    )

    # data: {'all_grade_name': all_grade_name, 'all_grade_name_url': all_grade_name_url}
    all_grade_name = scraping_data_service.get_all_grade_name(
        all_vehicle_type['all_vehicle_type_url']
    )

    ### csvに出力する実装 ###

    random_seconds = random.uniform(0.234, 1.000)
    openpyxl_service.init_openpyxl(fileName='sample_car_data')

    for i, maker_name in enumerate(tqdm(all_maker['all_maker_name'])):
        if i < 3:
            for j, vehicle_type_name in enumerate(all_vehicle_type['all_vehicle_type_name']):
                if j < 10:
                    for y, grade_name in enumerate(all_grade_name['all_grade_name']):
                        time.sleep(random_seconds)
                        spec_details = scraping_data_service.get_spec_detail(
                            grade_name_url=all_grade_name['all_grade_name_url'][y]
                        )

                        openpyxl_service.add_data_in_sheet(
                            maker_name, vehicle_type_name, grade_name, spec_details
                        )

    openpyxl_service.remove_space_col()
    openpyxl_service.create_title()

    print(f'all data wrote csv')


if __name__ == '__main__':
    main()
