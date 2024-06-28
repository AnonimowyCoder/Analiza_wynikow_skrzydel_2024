import pandas as pd

class DataManager:
    def __init__(self, foil_name: str,file_path: str):
        self.foil_name = foil_name
        self.file_path = file_path
        self.data = None
    
    def load_data(self):
        """
        Load data from a CSV file.
        """
        self.data = pd.read_csv(self.file_path, delimiter=';')
    
    def clean_data(self):
        """
        Clean the DataFrame by setting headers and removing unnecessary rows/columns.
        """
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
