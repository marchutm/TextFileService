import json


class JSONFileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_json_data()

    def load_json_data(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
            return data
        except Exception as e:
            print("Error loading JSON data:", e)
            return None

    def get_keys_count_per_element(self):
        try:
            if self.data:
                keys_count_list = [len(item.keys()) for item in self.data]
                return keys_count_list
        except Exception as e:
            print("Error getting keys count per element for JSON:", e)
            return []

    def detect_missing_values(self):
        try:
            if self.data:
                missing_values_dict = {}
                for item in self.data:
                    for key, value in item.items():
                        if value is None:
                            if key not in missing_values_dict:
                                missing_values_dict[key] = 0
                            missing_values_dict[key] += 1
                return missing_values_dict
        except Exception as e:
            print("Error detecting missing values in JSON:", e)
            return {}

    def get_data_summary(self):
        try:
            if self.data:
                num_elements = len(self.data)
                keys_list = list(self.data[0].keys()) if self.data else []
                summary = {
                    'num_elements': num_elements,
                    'keys_list': keys_list,
                    'keys_per_element': self.get_keys_count_per_element(),
                    'missing_values': self.detect_missing_values(),
                }

                return summary
        except Exception as e:
            print("Error generating data summary for JSON:", e)
            return None
