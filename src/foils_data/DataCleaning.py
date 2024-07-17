import numpy as np
import pandas as pd


class DataCleaningMixin:
    def clean_data(self):
        """
        Clean the DataFrame by setting headers and removing unnecessary rows/columns.

        Depending on which type of results is being processed, the method does different things.
        """
        if self.results_type == "AFT":
            self._clean_data_AFT()
        elif self.results_type == "CFD":
            self._clean_data_CFD()
        else:
            print("Wrong results_type format !!!")

    def _clean_data_CFD(self):
        self.data.columns = self.data.iloc[0]
        self.data = self.data[1:]
        self.data.reset_index(drop=True, inplace=True)

        # Convert to numeric
        self.data['inlet_vel'] = pd.to_numeric(self.data['inlet_vel'], errors='coerce').astype('float64')
        self.data['angle_of_attack'] = pd.to_numeric(self.data['angle_of_attack'], errors='coerce').astype('float64')
        self.data['moment'] = pd.to_numeric(self.data['moment'], errors='coerce').astype('float64')
        self.data['lift_force'] = pd.to_numeric(self.data['lift_force'], errors='coerce').astype('float64')
        self.data['drag_force'] = pd.to_numeric(self.data['drag_force'], errors='coerce').astype('float64')
        self.data['lift_coefficient'] = pd.to_numeric(self.data['lift_coefficient'], errors='coerce').astype('float64')
        self.data['drag_coefficient'] = pd.to_numeric(self.data['drag_coefficient'], errors='coerce').astype('float64')

    def multiply_forces_by_2(self):

        # Multiplies by 2 the moment, lift force and drag force column
        # It is done because results from simulation are for symmetry
        self.data['moment'] = self.data['moment'] * 2
        self.data['lift_force'] = self.data['lift_force'] * 2
        self.data['drag_force'] = self.data['drag_force'] * 2

    def _clean_data_AFT(self):
        # deleting unnecessary columns
        columns_to_drop = ['Cdp', 'Top_Xtr', 'Bot_Xtr']
        self.data.drop(columns=columns_to_drop, inplace=True)

        # changing names
        column_mapping = {
            'Alpha': 'angle_of_attack',
            'Cl': 'lift_coefficient',
            'Cd': 'drag_coefficient',
            'Cm': 'moment_coefficient',
        }
        self.data.rename(columns=column_mapping, inplace=True)

        # Filter out rows where angle_of_attack has a fractional part of 0.25 or 0.75
        self.data = self.data[~((self.data['angle_of_attack'] % 1 == 0.25) | (self.data['angle_of_attack'] % 1 == 0.75))]

        # Filter out rows where angle_of_attack is lower than -4 deg
        self.data = self.data[~(self.data['angle_of_attack'] < (-4.0))]

        # Filer out rows where angle_of_attack is higher than 7.5 deg
        self.data = self.data[~(self.data['angle_of_attack'] > 7.5)]

        # adding rows so the dataframe will match the CFD dataframe
        velocities = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0]

        # Repeat the rows of the second DataFrame to match the number of velocity values
        self.data = self.data.loc[self.data.index.repeat(len(velocities))].reset_index(drop=True)

        # Tile the velocity values to match the number of rows in the expanded DataFrame
        self.data['inlet_vel'] = np.tile(velocities, len(self.data) // len(velocities))