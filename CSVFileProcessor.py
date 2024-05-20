import pandas as pd


class CSVFileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r') as file:
            first_line = file.readline().strip()
        has_header = any(c.isalpha() for c in first_line)
        if has_header:
            self.df = pd.read_csv(file_path, header=0)
        else:
            self.df = pd.read_csv(file_path, header=None)

    def extract_unique_values(self):
        try:
            unique_values_dict = {}
            for column_name in self.df.columns:
                unique_values = self.df[column_name].unique().tolist()
                unique_values_dict[column_name] = unique_values
            return unique_values_dict
        except Exception as e:
            print("Error extracting unique values:", e)
            return None

    def calculate_statistics(self):
        try:
            numeric_columns = self.df.select_dtypes(include='number').columns
            statistics_dict = {}
            for column_name in numeric_columns:
                column = self.df[column_name]
                statistics = {
                    'sum': column.sum(),
                    'mean': column.mean(),
                    'median': column.median(),
                    'standard_deviation': column.std(),
                    'max': column.max(),
                    'min': column.min()
                }
                statistics_dict[column_name] = statistics
            return statistics_dict
        except Exception as e:
            print("Error calculating statistics:", e)
            return None

    def file_dimensions_and_columns(self):
        num_rows, num_cols = self.df.shape

        columns_list = self.df.columns.tolist()

        return num_rows, num_cols, columns_list

    def get_data_summary(self):
        try:
            unique_values = self.extract_unique_values()
            statistics = self.calculate_statistics()
            num_rows, num_cols, columns_list = self.file_dimensions_and_columns()

            data_summary = {
                'num_rows': num_rows,
                'num_cols': num_cols,
                'columns_list': columns_list,
                'unique_values': unique_values,
                'statistics': statistics,
            }

            return data_summary
        except Exception as e:
            print("Error generating data summary for CSV file:", e)
            return None
