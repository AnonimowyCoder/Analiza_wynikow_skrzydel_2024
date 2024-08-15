import numpy as np
from scipy.interpolate import griddata


class CFD_DataProcessingMixin:
    def calculate_lift_coefficient(self, density):
        """
        Calculate the lift coefficient using lift force.

        Formula:

        lift_coefficient = (2 * lift_force) / (density * velocity^2 * area)
        """
        self.data['lift_coefficient'] = (2 * self.data['lift_force']) / (
                density * pow(self.data['inlet_vel'], 2) * self.m2_foil_area)

    def calculate_drag_coefficient(self, density):
        """
        Calculate the drag coefficient using drag force.

        Formula:

        drag_coefficient = (2 * drag_force) / (density * velocity^2 * area)
        """
        self.data['drag_coefficient'] = (2 * self.data['drag_force']) / (
                density * pow(self.data['inlet_vel'], 2) * self.m2_foil_area)

    def calculate_cl_cd(self):
        """
        Calculate lift coefficient vs drag coefficient (effectiveness of foil).

        Formula:

        cl_cd = cl / cd
        """
        self.data['cl_cd'] = self.data['lift_coefficient'] / self.data['drag_coefficient']

    def get_interpolated_drag_coefficient(self, angle_of_attack, velocity):
        """
        Get the interpolated drag coefficient using cubic interpolation.
        """

        points = self.data[['angle_of_attack', 'inlet_vel']].values
        values = self.data['drag_coefficient'].values

        # To get interpolated value for specific points
        return griddata(points, values, (angle_of_attack, velocity), method='cubic')

    def get_interpolated_lift_coefficient(self, angle_of_attack, velocity):
        """
        Get the interpolated lift coefficient using cubic interpolation.
        """

        points = self.data[['angle_of_attack', 'inlet_vel']].values
        values = self.data['lift_coefficient'].values

        # To get interpolated value for specific points
        return griddata(points, values, (angle_of_attack, velocity), method='cubic')

    def get_interpolated_lift_force(self, angle_of_attack, velocity):
        """
        Get the interpolated lift force using cubic interpolation.
        """

        points = self.data[['angle_of_attack', 'inlet_vel']].values
        values = self.data['lift_force'].values

        # To get interpolated value for specific points
        return griddata(points, values, (angle_of_attack, velocity), method='cubic')

    def get_interpolated_drag_force_foil(self, angle_of_attack, velocity):
        """
        Get the interpolated drag force of foil using cubic interpolation.
        """

        points = self.data[['angle_of_attack', 'inlet_vel']].values
        values = self.data['drag_force'].values

        # To get interpolated value for specific points
        return griddata(points, values, (angle_of_attack, velocity), method='cubic')

    def get_interpolated_drag_force_pylon(self, angle_of_attack, velocity):
        """
        Get the interpolated drag force of pylon using cubic interpolation.
        """

        points = self.data[['angle_of_attack', 'inlet_vel']].values
        values = self.data['drag_force_pylon'].values

        # To get interpolated value for specific points
        return griddata(points, values, (angle_of_attack, velocity), method='cubic')

    def get_interpolated_drag_force_mocowanie(self, angle_of_attack, velocity):
        """
        Get the interpolated drag force of mocowanie using cubic interpolation.
        """

        points = self.data[['angle_of_attack', 'inlet_vel']].values
        values = self.data['drag_force_mocowanie'].values

        # To get interpolated value for specific points
        return griddata(points, values, (angle_of_attack, velocity), method='cubic')
