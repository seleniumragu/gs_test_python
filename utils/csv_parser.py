import csv


class CsvParser(object):
    """
    This is class to parse .csv files
    TODO: Introduce datatable so we can put all data into datatable
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.whole_data_as_dict = []
        with open(self.file_path) as csv_file:
            self.csv_reader = csv.DictReader(csv_file)
            for row in self.csv_reader:
                self.whole_data_as_dict.append(row)

    def read_entire_csv(self):
        """
        Get entire csv file parsed as ordered dictionary
        :return: Ordered dictionary of entire csv
        """
        return self.whole_data_as_dict

    def read_by_column_name(self, column_name):
        """
        Get entire column value by giving column name
        :param column_name: String, csv header name
        :return: Whole column value under giving header
        """
        entire_column_value = []
        for row in self.whole_data_as_dict:
            entire_column_value.append(row[column_name])
        return entire_column_value
