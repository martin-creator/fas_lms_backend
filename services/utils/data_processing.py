import pandas as pd

class DataProcessor:
    @staticmethod
    def process_data(file_path):
        data = pd.read_csv(file_path)
        # Perform data processing
        processed_data = data  # Example placeholder
        return processed_data
