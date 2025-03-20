import pandas as pd

from src.foils_data.DataLoading import DataLoadingMixin
from src.foils_data.DataCleaning import DataCleaningMixin
from src.foils_data.AFT_DataProcessing import AFT_DataProcessingMixin
from src.foils_data.CFD_DataProcessing import CFD_DataProcessingMixin


def foil_manager_procedure(data_type, foil_name, path, area, chord_length, multiply_by_2: bool = True,
                           calculate_pressure_center: bool = True):
    data_manager = FoilManager(data_type, foil_name, path, area, chord_length)

    data_manager.load_data()
    data_manager.clean_data()
    if multiply_by_2:
        data_manager.multiply_forces_by_2()
    data_manager.calculate_lift_coefficient()
    data_manager.calculate_drag_coefficient()
    if calculate_pressure_center:
        data_manager.calculate_moment_coefficient()
        data_manager.calculate_pressure_center()
    data_manager.calculate_cl_cd()

    return data_manager


class FoilManager(DataLoadingMixin, DataCleaningMixin, AFT_DataProcessingMixin, CFD_DataProcessingMixin):
    def __init__(self, results_type: str, foil_name: str, file_path: str, m2_foil_area: float, m_chord_length=0.0):
        """
        Initializes DataManager which stores single profile's data.

        Parameters:
            results_type (str): type of format of results, eg. AFT, CFD.
            foil_name (str): foil_name of foil.
            file_path (str): path to the csv data of foil.
            m2_foil_area (float): area of foil in m2.
            m_chord_length (float): length of chord of foil in m.
        """
        self.foil_name = foil_name
        self.results_type = results_type
        self.m2_foil_area = m2_foil_area
        self.file_path = file_path
        self.m_chord_length = m_chord_length
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
