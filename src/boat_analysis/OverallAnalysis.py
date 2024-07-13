from src.boat_analysis.Boat import Boat
from src.foils_data.FoilManager import FoilManager
from src.utilities.Constants import *
from pathlib import Path


# Module to realize the algorithm of modelling a flight

def overall_lift_analysis(target_velocity, frontFoilManager: FoilManager, front_target_angle_of_attack,
                          rearFoilManager: FoilManager, rear_target_angle_of_attck, boat: Boat):
    """
    Method to realize the whole boat lift analysis.

    :param boat: Boat model.
    :param target_velocity: Velocity for which the flight is calculated.
    :param frontFoilManager: Container of front foils data.
    :param front_target_angle_of_attack: Angle of attack of front foils for which the flight is calculated.
    :param rearFoilManager: Container of rear foils data.
    :param rear_target_angle_of_attck: Angle of attack of rear foils for which the flight is calculated.
    :return: rear_foil_area, front_foil_area
    """

    print('Target velocity is: ', target_velocity)
    print('Front target angle of attack is: ', front_target_angle_of_attack)
    print('Rear target angle of attck is: ', rear_target_angle_of_attck)

    # rear foil calculations
    rear_foil_area = calculate_foil_area(rear_target_angle_of_attck, target_velocity, boat.rear_pylon_mass,
                                         rearFoilManager)

    # front foil calculations
    front_foil_area = calculate_foil_area(front_target_angle_of_attack, target_velocity, boat.front_pylon_left_mass,
                                          frontFoilManager)
    return rear_foil_area, front_foil_area


def calculate_foil_area(target_angle_of_attack, target_velocity, pylon_mass, foilManager: FoilManager):
    """
    Method to calculate the area of the foil to model a flight.
    Formula: area = (2 * lift_force) / (density * velocity^2 * lift_coefficient) [m^2]

    :param pylon_mass: mass on selected pylon (the argument should be an attribute of Boat)
    :param target_velocity: velocity for which the flight is being calculated.
    :param target_angle_of_attack: angle of attack for which the flight is calculated.
    :param foilManager: container with selected foil data.
    :return: foil_area
    """
    # data preparation
    filtered_velocity_data = foilManager.filter_data_by_velocity(target_velocity)
    lift_coefficient = filtered_velocity_data.loc[
        filtered_velocity_data['angle_of_attack'] == target_angle_of_attack, 'lift_coefficient'].values[0]

    lift_force = pylon_mass * GRAVITATIONAL_ACCELERATION

    foil_area = (2 * lift_force) / (WATER_DENSITY * pow(target_velocity, 2) * lift_coefficient)
    print('Area for the foil is: ', foil_area, 'm^2')

    return foil_area


# Setting path for the csv file
script_dir = Path(__file__).resolve().parent
NACA6409_CFD_path = script_dir / '..' / '..' / 'data_CFD' / 'CFD_3D_skrzydla_przednie2023_batmanowe_NACA6409_Wyniki.csv'
NACA6409_CFD_path = NACA6409_CFD_path.resolve()

Celka = Boat(6.039, 1.69, 193, 2.676)
Celka.distribution_of_masses(3.551, 0.725, 0.386)
data_manager_NACA6409_CFD = FoilManager('CFD', 'NACA 6409', NACA6409_CFD_path, NACA6409_TOTAL_LENGTH,
                                        NACA6409_CHORD_LENGTH, NACA6409_AREA)
data_manager_NACA6409_CFD.load_data()
data_manager_NACA6409_CFD.clean_data()
data_manager_NACA6409_CFD.calculate_lift_coefficient(WATER_DENSITY)
data_manager_NACA6409_CFD.calculate_drag_coefficient(WATER_DENSITY)
data_manager_NACA6409_CFD.calculate_cl_cd()

#calculate_foil_area(1.5, 6, Celka.front_pylon_left_mass, data_manager_NACA6409_CFD)
overall_lift_analysis(6, data_manager_NACA6409_CFD, 0.5, data_manager_NACA6409_CFD, 0.5, Celka)
