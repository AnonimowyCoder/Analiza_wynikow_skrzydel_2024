import pandas as pd

class FoilManager:
    def __init__(self, results_type:str , foil_name: str, file_path: str, mm_foil_total_length=0,mm_foil_chord_length=0, mm2_foil_area=0):
        """
        Initializes DataManager which stores single profile's data.

        Parameters:
            results_type (str): type of format of results, eg. AFT, CFD.
        """
        self.foil_name = foil_name
        self.results_type = results_type
        self.mm_foil_total_length = mm_foil_total_length
        self.mm_foil_chord_length = mm_foil_chord_length
        self.mm2_foil_area = mm2_foil_area
        self.file_path = file_path
        self.data = None

    def load_data(self):
        """
        Load data from a CSV file that comes from a AFT or CFD.

        The CSV file should be prepared in a proper format (see README).
        """
        if(self.results_type == 'AFT'):
            self.data = pd.read_csv(self.file_path, skiprows=9)
        elif(self.results_type == 'CFD'):
            self.data = pd.read_csv(self.file_path, delimiter=';')
        else:
            print("Wrong results_type format !!!")
    
    def clean_data(self):
        """
        Clean the DataFrame by setting headers and removing unnecessary rows/columns.

        Depending which type of results is being processed, method does different things.
        """
        if(self.results_type == "AFT"):
            self._clean_data_AFT()
        elif(self.results_type == "CFD"):
            self._clean_data_CFD()
        else:
            print("Wrong results_type format !!!")

    def _clean_data_CFD(self):

        self.data.columns = self.data.iloc[0]
        self.data = self.data[1:]
        self.data.reset_index(drop=True, inplace=True)

        # Convert to numeric
        self.data['inlet_vel'] = pd.to_numeric(self.data['inlet_vel'], errors='coerce')
        self.data['angle_of_attack'] = pd.to_numeric(self.data['angle_of_attack'], errors='coerce')
        self.data['moment'] = pd.to_numeric(self.data['moment'], errors='coerce')
        self.data['lift_force'] = pd.to_numeric(self.data['lift_force'], errors='coerce')
        self.data['drag_force'] = pd.to_numeric(self.data['drag_force'], errors='coerce')
        
        # Drop rows with NaN values in specific columns
        self.data.dropna(subset=['inlet_vel', 'angle_of_attack', 'moment', 'lift_force', 'drag_force'], inplace=True)

        #Multiplies by 2 the moment, lift force and drag force column
        #It is done because results from simulation are for symmetry

        self.data['moment'] = self.data['moment']*2
        self.data['lift_force'] = self.data['lift_force']*2        
        self.data['drag_force'] = self.data['drag_force']*2


    def _clean_data_AFT(self):
        
        columns_to_drop = ['Cdp','Top_Xtr','Bot_Xtr']

        self.data.drop(columns = columns_to_drop, inplace=True)

        column_mapping = {
        'Alpha': 'angle_of_attack',
        'Cl': 'lift_coefficient',
        'Cd': 'drag_coefficient',
        'Cm': 'moment_coefficient',
        }

        self.data.rename(columns=column_mapping, inplace=True)


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
