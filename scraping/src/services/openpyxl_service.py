from openpyxl import Workbook
from openpyxl import load_workbook

from scraping.src.constants.openpyxl_constants import OpenPyxlConstants


class OpenpyxlService:
    def __init__(self) -> None:
        self.sheet = None
        self.excelFile = ''
        self.max_col = 0
        self.max_row = 0

    def init_openpyxl(self, fileName: str):
        initializedSheet = Workbook()
        exfile = "sample_car_data"
        self.excelFile = f'../excel_data/{fileName}.xlsx'
        initializedSheet.save(self.excelFile)
        book = load_workbook(self.excelFile)
        self.sheet = book.worksheets[0]
        return self.sheet

    def save_sheet(self):
        self.sheet.save(self.excelFile)

    def add_max_col(self):
        self.max_col += 1

    def add_max_row(self):
        self.max_row += 1

    def clear_max_col_row(self):
        self.max_col = 0
        self.max_row = 0

    def create_title(self):
        for i, indexTitle in enumerate(OpenPyxlConstants.titles):
            self.sheet.cell(row=i+1, column=1).value = indexTitle
        self.save_sheet()

    def add_title(self):
        self.save_sheet()

    def add_data_in_sheet(self, maker_name: str, vehicle_type_name: str, grade_name: str, spec_details: list):
        self.sheet.cell(row=1, column=self.max_col).value = maker_name
        self.add_max_col()

        self.sheet.cell(row=2, column=self.max_col).value = vehicle_type_name
        self.add_max_col()

        self.sheet.cell(row=3, column=self.max_col).value = grade_name
        self.add_max_col()

        for i, spec_detail in enumerate(spec_details):
            self.sheet.cell(row=i+4, column=self.max_col).value = spec_detail
            self.max_col()
