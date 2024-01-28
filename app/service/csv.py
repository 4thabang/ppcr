from typing import List

class CSVParser:
    def __init__(self, csv):
        self.csv = csv

    def read(self, file_path) -> List:
        with open(file_path, 'r') as file:
            values = self.csv.DictReader(file)
            return self.__filter_rows(values)

    def write(self, file_path, csv_content):
        headers = ["review_id", "review", "violation_category", "flagged_reason", "email_body"]
        file_path = f"{file_path}"
        with open(file_path, "w", newline='') as file:
            writer = self.csv.DictWriter(file, headers)
            writer.writeheader()
            writer.writerows(csv_content)

    def __filter_rows(self, csv_values):
        reviews_buffer = []
        for csv_value in csv_values:
            reviews_buffer.append(csv_value)
        return reviews_buffer
