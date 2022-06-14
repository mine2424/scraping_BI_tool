import time
from scraping.src.services.openpyxl_service import OpenpyxlService

from scraping.src.services.scraping_data_service import ScrapingDataService


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

    for maker_name in all_maker['all_maker_name']:
        for vehicle_type_name in all_vehicle_type['all_vehicle_type_name']:
            for y, grade_name in enumerate(all_grade_name['all_grade_name']):
                time.sleep(2)
                spec_details = scraping_data_service.get_spec_detail(
                    all_grade_name['all_grade_name_url'][y]
                )
                openpyxl_service.add_data_in_sheet(
                    maker_name=maker_name,
                    vehicle_type_name=vehicle_type_name,
                    grade_name=grade_name,
                    spec_details=spec_details,
                )


if __name__ == '__main__':
    main()
