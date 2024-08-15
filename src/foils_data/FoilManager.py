import pandas as pd

from src.foils_data.DataLoading import DataLoadingMixin
from src.foils_data.DataCleaning import DataCleaningMixin
from src.foils_data.AFT_DataProcessing import AFT_DataProcessingMixin
from src.foils_data.CFD_DataProcessing import CFD_DataProcessingMixin


class FoilManager(DataLoadingMixin, DataCleaningMixin, AFT_DataProcessingMixin, CFD_DataProcessingMixin):
    def __init__(self, results_type: str, foil_name: str, file_path: str, m_foil_total_length: float = 0.0,
                 m_foil_chord_length: float = 0.0, m2_foil_area: float = 0.0):
        """
        Initializes DataManager which stores single profile's data.

        Parameters:
            results_type (str): type of format of results, eg. AFT, CFD.
            foil_name (str): name of foil.
            file_path (str): path to the csv data of foil.
            m_foil_total_length (int): total length in m of foil.
            m_foil_chord_length (int): chord length in m of foil.
            m2_foil_area (int): area of foil in m2.
        """
        self.foil_name = foil_name
        self.results_type = results_type
        self.mmfoil_total_length = m_foil_total_length
        self.m_foil_chord_length = m_foil_chord_length
        self.m2_foil_area = m2_foil_area
        self.file_path = file_path
        self.data = None

        # Set display options to show all columns
        pd.set_option('display.max_columns', None)

    def filter_data_by_velocity(self, velocity):
        """
        Filter the data by a specific inlet velocity.
        
        Parameters:
            velocity (float): The inlet velocity to filter by.

        Returns:
            pd.DataFrame: Filtered DataFrame.
        """
        return self.data[self.data['inlet_vel'] == velocity]

    def filter_data_by_angle(self, angle):
        """
        Filter the data by a specific angle of attack.
        
        Parameters:
        angle (float): The angle of attack to filter by.

        Returns:
        pd.DataFrame: Filtered DataFrame.
        """
        return self.data[self.data['angle_of_attack'] == angle]
