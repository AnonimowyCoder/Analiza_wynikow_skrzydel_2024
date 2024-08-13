from src.boat_analysis.Boat import Boat
from src.boat_analysis.PowerConsumption import power_consumption
from src.foils_data.FoilManager import FoilManager
from src.utilities.Constants import *
from pathlib import Path


# Module to realize the algorithm of modelling a flight

def foils_drag_analysis(rear_foil_area, front_foil_area, target_velocity, frontFoilManager: FoilManager,
                        front_target_angle_of_attack, rearFoilManager: FoilManager, rear_target_angle_of_attack):
    """
    Method to realize airfoils drag analysis based on foils areas,velocity, angles of attack of foils.

    :param rear_foil_area: Rear foil area.
    :param front_foil_area : Front foil area.
    :return rear_drag, front_drag
    Formula:

    Drag = (1 / 2) * density * (velocity ^ 2) * Area * Drag_Coefficient
    """

    front_drag = (1 / 2) * WATER_DENSITY * pow(target_velocity,
                                               2) * front_foil_area * frontFoilManager.get_interpolated_drag_coefficient(
        front_target_angle_of_attack, target_velocity)
    rear_drag = (1 / 2) * WATER_DENSITY * pow(target_velocity,
                                              2) * rear_foil_area * rearFoilManager.get_interpolated_drag_coefficient(
        rear_target_angle_of_attack, target_velocity)

    return rear_drag, front_drag


def overall_lift_analysis(target_velocity, frontFoilManager: FoilManager, front_target_angle_of_attack,
                          rearFoilManager: FoilManager, rear_target_angle_of_attack, boat: Boat):
    """
    Method to realize the whole boat lift analysis.

    :param boat: Boat model.
    :param target_velocity: Velocity for which the flight is calculated.
    :param frontFoilManager: Container of front foils data.
    :param front_target_angle_of_attack: Angle of attack of front foils for which the flight is calculated.
    :param rearFoilManager: Container of rear foils data.
    :param rear_target_angle_of_attack: Angle of attack of rear foils for which the flight is calculated.
    :return: rear_foil_area, front_foil_area
    """

    print('Target velocity is: ', target_velocity)
    print('Front target angle of attack is: ', front_target_angle_of_attack)
    print('Rear target angle of attack is: ', rear_target_angle_of_attack)

    # rear foil calculations
    rear_foil_area = calculate_foil_area(rear_target_angle_of_attack, target_velocity, boat.rear_pylon_mass,
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
    print('Area for the foil: ', foilManager.foil_name, ' is: ', foil_area, 'm^2')

    return foil_area


# Setting path for the csv file
script_dir = Path(__file__).resolve().parent
NACA6409_CFD_path = script_dir / '..' / '..' / 'data_CFD' / 'CFD_3D_skrzydla_przednie2023_batmanowe_NACA6409_Wyniki.csv'
NACA6409_CFD_path = NACA6409_CFD_path.resolve()
EPPLER908_CFD_path = script_dir / '..' / '..' / 'data_CFD' / 'CFD_3D_skrzydla_tylnie2021_eppler908_Wyniki.csv'
EPPLER908_CFD_path = EPPLER908_CFD_path.resolve()

Celka = Boat(6.039, 1.69, 190)
Celka.distribution_of_masses(2.676, 3.551, 0.725, 0.386)

# hydrofoils
data_manager_NACA6409_CFD = FoilManager('CFD', 'NACA 6409', NACA6409_CFD_path, NACA6409_TOTAL_LENGTH,
                                        NACA6409_CHORD_LENGTH, NACA6409_AREA)
data_manager_NACA6409_CFD.load_data()
data_manager_NACA6409_CFD.clean_data()
data_manager_NACA6409_CFD.multiply_forces_by_2()
data_manager_NACA6409_CFD.calculate_lift_coefficient(WATER_DENSITY)
data_manager_NACA6409_CFD.calculate_drag_coefficient(WATER_DENSITY)
data_manager_NACA6409_CFD.calculate_cl_cd()

data_manager_EPPLER908 = FoilManager('CFD', 'EPPLER 908', EPPLER908_CFD_path, 0, 0, EPPLER908_AREA)
data_manager_EPPLER908.load_data()
data_manager_EPPLER908.clean_data()
data_manager_EPPLER908.multiply_forces_by_2()
data_manager_EPPLER908.calculate_lift_coefficient(WATER_DENSITY)
data_manager_EPPLER908.calculate_drag_coefficient(WATER_DENSITY)
data_manager_EPPLER908.calculate_cl_cd()

rear_foil_area, front_foil_area = overall_lift_analysis(6.5, data_manager_NACA6409_CFD, 0.0, data_manager_EPPLER908,
                                                        0.0, Celka)
rear_drag, front_drag = foils_drag_analysis(rear_foil_area, front_foil_area, 6.5, data_manager_NACA6409_CFD, 0.0,
                                            data_manager_EPPLER908,
                                            0.0)
print("rear drag is: ", rear_drag, "front drag is: ", front_drag)

print("Overall drag from foils: ", rear_drag + 2 * front_drag, "[N]")

Celka_foils_drag = rear_drag + 2 * front_drag

print("Front foil area is for celka is: ",front_foil_area)
print("Current front foil area is: ", NACA6409_AREA)

power_consumption
# print("\n\nTEST BOAT CALCULATIONS")
# print("#############################################")
# test_boat = Boat(6, 1.7, 165)
# test_boat.center_of_mass_based_on_front_rear_mass_ratio(0.75, 3.5, 0.725, 0.386)
#
# rear_foil_area, front_foil_area = overall_lift_analysis(8, data_manager_NACA6409_CFD, 0.5, data_manager_EPPLER908, 0.5,
#                                                         test_boat)
#
# rear_drag, front_drag = foils_drag_analysis(rear_foil_area, front_foil_area, 8, data_manager_NACA6409_CFD, 0.5,
#                                             data_manager_EPPLER908,
#                                             0.5)
#
# print("rear drag is: ", rear_drag, " front drag is: ", front_drag)
#
# print("Overall drag from foils: ", rear_drag + 2 * front_drag, "[N]")
#
# test_boat_foils_drag = rear_drag + 2 * front_drag
#
# print("Difference in foils drag between new boat and Celka: ", test_boat_foils_drag - Celka_foils_drag)
#
# celka_power_consumption = power_consumption(Celka_foils_drag, 8, 0.75)
# print("Celka power consumption is: ", celka_power_consumption)
#
# test_boat_power_consumption = power_consumption(test_boat_foils_drag, 8, 0.75)
# print("Test boat power consumption is: ", test_boat_power_consumption)
#
# print("difference in power consumption: ", test_boat_power_consumption - celka_power_consumption)
