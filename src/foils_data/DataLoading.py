import pandas as pd


class DataLoadingMixin:
    """
    Mixin for loading data from CSV files.
    """
    def load_data(self):
        """
        Load data from a CSV file that comes from a AFT or CFD.

        The CSV file should be prepared in a proper format (see README).
        """
        if self.results_type == 'AFT':
            self.data = pd.read_csv(self.file_path, skiprows=9)
        elif self.results_type == 'CFD':
            self.data = pd.read_csv(self.file_path, delimiter=';')
        else:
            print("Wrong results_type format !!!")
