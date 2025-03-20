import numpy as np
from scipy.interpolate import griddata, interp1d, Rbf


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

    def calculate_pressure_center(self, x1=0.0):
        """
        Calculate the pressure center of a foil, where the returning value is value (0,1) representing position on the foil

        Formula

        Xcp = x1 - Cm1/Cl

        where:
        Xcp - position of pressure center
        x1 - position of the axis on the chord for which moment force is calculated
        Cm1 - Moment force over axis x1
        Cl - Lift Force of the foil

        Parameters:
            x1 - position of the axis on the chord for which moment force is calculated
        """
        self.data['pressure_center'] = x1 - self.data['moment'] / self.data['lift_force']

    def get_interpolated_value(self, column_name, angle_of_attack, velocity):
        """
        Generic method to get the interpolated value for a given column using cubic interpolation.

        Parameters:
        - column_name: str, the name of the column to interpolate.
        - angle_of_attack: float or array-like, the angle(s) of attack at which to interpolate.
        - velocity: float or array-like, the velocity(ies) at which to interpolate.

        Returns:
        - Interpolated value(s) at the specified angle(s) of attack and velocity(ies).
        """
        unique_aoa = np.unique(self.data['angle_of_attack'].values)

        if len(unique_aoa) == 1:
            # Only one unique angle of attack in the dataset
            data_aoa = unique_aoa[0]
            if not np.isclose(angle_of_attack, data_aoa):
                raise ValueError(f"Requested angle of attack {angle_of_attack}° is not available in the dataset.")

            # Perform 1D interpolation over velocity
            vel = self.data['inlet_vel'].values
            values = self.data[column_name].values
            interpolator = interp1d(vel, values, kind='cubic')
            return interpolator(velocity)
        else:
            # Perform 2D interpolation over (angle_of_attack, velocity) using RBF with extrapolation
            aoa = self.data['angle_of_attack'].values
            vel = self.data['inlet_vel'].values
            values = self.data[column_name].values

            # Create RBF interpolator
            interpolator = Rbf(aoa, vel, values, function='multiquadric')

            # Interpolate at the requested point
            return interpolator(angle_of_attack, velocity)

    def get_interpolated_lift_force(self, angle_of_attack, velocity):
        """
        Get the interpolated lift force.
        """
        return self.get_interpolated_value('lift_force', angle_of_attack, velocity)

    def get_interpolated_drag_coefficient(self, angle_of_attack, velocity):
        """
        Get the interpolated drag coefficient.
        """
        return self.get_interpolated_value('drag_coefficient', angle_of_attack, velocity)

    def get_interpolated_lift_coefficient(self, angle_of_attack, velocity):
        """
        Get the interpolated lift coefficient.
        """
        return self.get_interpolated_value('lift_coefficient', angle_of_attack, velocity)

    def get_interpolated_drag_force_foil(self, angle_of_attack, velocity):
        """
        Get the interpolated drag force of the foil.
        """
        return self.get_interpolated_value('drag_force', angle_of_attack, velocity)

    def get_interpolated_drag_force_pylon(self, angle_of_attack, velocity):
        """
        Get the interpolated drag force of the pylon.
        """
        return self.get_interpolated_value('drag_force_pylon', angle_of_attack, velocity)

    def get_interpolated_drag_force_mocowanie(self, angle_of_attack, velocity):
        """
        Get the interpolated drag force of the mocowanie.
        """
        return self.get_interpolated_value('drag_force_mocowanie', angle_of_attack, velocity)

    def get_interpolated_drag_force_gondola(self, angle_of_attack, velocity):
        """
        Get the interpolated drag force of the gondola.
        """
        return self.get_interpolated_value('drag_force_gondola', angle_of_attack, velocity)

    def get_interpolated_moment(self, angle_of_attack, velocity):
        """
        Get the interpolated moment.
        """
        return self.get_interpolated_value('moment', angle_of_attack, velocity)

    def get_interpolated_pressure_center(self,angle_of_attack, velocity):
        """
        Get the interpolated pressure center of a foil.
        """
        return self.get_interpolated_value('pressure_center',angle_of_attack,velocity)
