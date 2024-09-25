from src.boat_analysis.Boat import Boat, read_boat_data
from src.boat_analysis.PowerConsumption import power_consumption
from src.foils_data.FoilManager import FoilManager
from src.foils_data.FoilPlotter import FoilPlotter
from src.utilities.Constants import *
from pathlib import Path


# Module to realize the algorithm of modelling a flight

def _calculate_foil_area(target_angle_of_attack, target_velocity, pylon_mass, foilManager: FoilManager):
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
    lift_coefficient = foilManager.get_interpolated_lift_coefficient(target_angle_of_attack, target_velocity)

    lift_force = pylon_mass * GRAVITATIONAL_ACCELERATION

    foil_area = (2 * lift_force) / (WATER_DENSITY * pow(target_velocity, 2) * lift_coefficient)
    print('Area for the foil: ', foilManager.foil_name, ' is: ', foil_area, 'm^2')

    return foil_area


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


def overall_front_drag_analysis(front_foil_area, target_velocity, front_parts_manager: FoilManager,
                                front_target_angle_of_attack):
    front_foil_drag = (1 / 2) * WATER_DENSITY * pow(target_velocity,
                                                    2) * front_foil_area * front_parts_manager.get_interpolated_drag_coefficient(
        front_target_angle_of_attack, target_velocity)

    front_pylon_drag = front_parts_manager.get_interpolated_drag_force_pylon(front_target_angle_of_attack,
                                                                             target_velocity)
    front_mocowanie_drag = front_parts_manager.get_interpolated_drag_force_mocowanie(front_target_angle_of_attack,
                                                                                     target_velocity)

    return front_foil_drag, front_pylon_drag, front_mocowanie_drag


def overall_rear_drag_analysis(rear_foil_area, target_velocity, rear_parts_manager: FoilManager,
                               rear_target_angle_of_attack=0):
    rear_foil_drag = (1 / 2) * WATER_DENSITY * pow(target_velocity,
                                                   2) * rear_foil_area * rear_parts_manager.get_interpolated_drag_coefficient(
        rear_target_angle_of_attack, target_velocity)

    rear_pylon_drag = rear_parts_manager.get_interpolated_drag_force_pylon(rear_target_angle_of_attack, target_velocity)

    rear_mocowanie_drag = rear_parts_manager.get_interpolated_drag_force_mocowanie(rear_target_angle_of_attack,
                                                                                   target_velocity)
    gondola_drag = rear_parts_manager.get_interpolated_drag_force_gondola(rear_target_angle_of_attack, target_velocity)

    return rear_foil_drag, rear_pylon_drag, rear_mocowanie_drag, gondola_drag


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
    rear_foil_area = _calculate_foil_area(rear_target_angle_of_attack, target_velocity, boat.rear_pylon_mass,
                                          rearFoilManager)

    # front foil calculations
    front_foil_area = _calculate_foil_area(front_target_angle_of_attack, target_velocity, boat.front_pylon_left_mass,
                                           frontFoilManager)
    return rear_foil_area, front_foil_area


def general_analysis():
    """
    Method to perform general analysis, based on data from boat csv file
    """
    script_dir = Path(__file__).resolve().parent
    boat_path = script_dir / '..' / '..' / 'boat_parameters' / 'boat_parameters.csv'
    boat_path = boat_path.resolve()
    boat = read_boat_data(boat_path, 0)
    sim_number = input("Choose front simulation: \n1. New boat pylon and mounting\n2. Celka old pylon and mounting\n")
    if (sim_number == '1'):
        front_path = script_dir / '..' / '..' / 'data_overall_drag' / 'CFD_3D_opory_latania_nowy_pylon.csv'
        front_path = front_path.resolve()
        front_manager = FoilManager('FRONT_DRAG', 'New Front pylons', front_path, 0, 0, NACA6409_AREA)
    elif (sim_number == '2'):
        front_path = script_dir / '..' / '..' / 'data_overall_drag' / 'CFD_3D_opory_latania_Celka_2024.csv'
        front_path = front_path.resolve()
        front_manager = FoilManager('FRONT_DRAG', 'Old Front pylons', front_path, 0, 0, NACA6409_AREA)
    else:
        print("Wrong simulation number")


def Celka_front_drag_analysis(angle_of_attack, velocity):
    script_dir = Path(__file__).resolve().parent
    Front_Celka_drags_path = script_dir / '..' / '..' / 'data_overall_drag' / 'CFD_3D_opory_latania_Celka_2024.csv'
    Front_Celka_drags_path = Front_Celka_drags_path.resolve()

    data_manager_Front_Celka_drags = FoilManager('FRONT_DRAG', 'Front pylons', Front_Celka_drags_path, 0, 0,
                                                 NACA6409_AREA)
    data_manager_Front_Celka_drags.load_data()
    data_manager_Front_Celka_drags.clean_data()
    data_manager_Front_Celka_drags.multiply_forces_by_2()
    data_manager_Front_Celka_drags.calculate_lift_coefficient(WATER_DENSITY)
    data_manager_Front_Celka_drags.calculate_drag_coefficient(WATER_DENSITY)

    front_foil_drag, front_pylon_drag, front_mocowanie_drag = overall_front_drag_analysis(NACA6409_AREA, velocity,
                                                                                          data_manager_Front_Celka_drags,
                                                                                          angle_of_attack)

    return front_foil_drag, front_pylon_drag, front_mocowanie_drag


def Celka_rear_drag_analysis(velocity):
    script_dir = Path(__file__).resolve().parent
    Rear_Celka_drags_path = script_dir / '..' / '..' / 'data_overall_drag' / 'CFD_3D_opory_latania_Celka_tyl_gondola.csv'
    Rear_Celka_drags_path = Rear_Celka_drags_path.resolve()

    data_manager_Rear_Celka_drags = FoilManager('REAR_DRAG', 'Front pylons', Rear_Celka_drags_path, 0, 0,
                                                EPPLER908_AREA)
    data_manager_Rear_Celka_drags.load_data()
    data_manager_Rear_Celka_drags.clean_data()
    data_manager_Rear_Celka_drags.multiply_forces_by_2()
    data_manager_Rear_Celka_drags.calculate_lift_coefficient(WATER_DENSITY)
    data_manager_Rear_Celka_drags.calculate_drag_coefficient(WATER_DENSITY)

    return overall_rear_drag_analysis(EPPLER908_AREA, velocity, data_manager_Rear_Celka_drags)

def Celka_overall_lift_analysis():
    script_dir = Path(__file__).resolve().parent
    Celka_path = script_dir / '..' / '..'/'boat_parameters'/'boat_parameters.csv'
    Celka_path = Celka_path.resolve()
    Celka = read_boat_data(Celka_path)


    # FRONT ###############################
    Front_Celka_drags_path = script_dir / '..' / '..' / 'data_overall_drag' / 'CFD_3D_opory_latania_Celka_2024.csv'
    Front_Celka_drags_path = Front_Celka_drags_path.resolve()

    data_manager_Front_Celka_drags = FoilManager('FRONT_DRAG', 'Front pylons', Front_Celka_drags_path, 0, 0,
                                                 NACA6409_AREA)
    data_manager_Front_Celka_drags.load_data()
    data_manager_Front_Celka_drags.clean_data()
    data_manager_Front_Celka_drags.multiply_forces_by_2()
    data_manager_Front_Celka_drags.calculate_lift_coefficient(WATER_DENSITY)
    data_manager_Front_Celka_drags.calculate_drag_coefficient(WATER_DENSITY)

    # REAR ##################################
    Rear_Celka_drags_path = script_dir / '..' / '..' / 'data_overall_drag' / 'CFD_3D_opory_latania_Celka_tyl_gondola.csv'
    Rear_Celka_drags_path = Rear_Celka_drags_path.resolve()

    data_manager_Rear_Celka_drags = FoilManager('REAR_DRAG', 'Front pylons', Rear_Celka_drags_path, 0, 0,
                                                EPPLER908_AREA)
    data_manager_Rear_Celka_drags.load_data()
    data_manager_Rear_Celka_drags.clean_data()
    data_manager_Rear_Celka_drags.multiply_forces_by_2()
    data_manager_Rear_Celka_drags.calculate_lift_coefficient(WATER_DENSITY)
    data_manager_Rear_Celka_drags.calculate_drag_coefficient(WATER_DENSITY)

    target_velocity = 7.7
    front_target_aoa = 0.5
    rear_target_aoa = 0

    rear_foil_area, front_foil_area = overall_lift_analysis(target_velocity, data_manager_Front_Celka_drags,
                                                            front_target_aoa,
                                                            data_manager_Rear_Celka_drags, rear_target_aoa, Celka)

    print("Rear foil area = ", rear_foil_area)
    print("Front foil area = ", front_foil_area)


def Celka_overall_drag_analysis():
    velocity = 7
    front_angle_of_attack = 2
    front_foil_drag, front_pylon_drag, front_mocowanie_drag = Celka_front_drag_analysis(front_angle_of_attack, velocity)

    rear_foil_drag, rear_pylon_drag, rear_mocowanie_drag, gondola_drag = Celka_rear_drag_analysis(velocity)
    print("################################################")
    print("Velocity = ", velocity)
    print("Front angle of attack = ", front_angle_of_attack, "\n")

    front_part_drag = front_foil_drag + front_pylon_drag + front_mocowanie_drag
    print("Single front part drag (foil + pylon + mocowanie) = ", front_part_drag)
    rear_part_drag = rear_foil_drag + rear_pylon_drag + rear_mocowanie_drag + gondola_drag
    print("Rear part drag (foil + pylon + mocowanie + GONDOLA) = ", rear_part_drag)
    print("\n\n")
    overall_celka_drag = 2 * front_part_drag + rear_part_drag
    print("Overall Celka drag = ", overall_celka_drag)


def new_boat_front_drag_analysis():
    script_dir = Path(__file__).resolve().parent
    New_Boat_drags_path = script_dir / '..' / '..' / 'data_overall_drag' / 'CFD_3D_opory_latania_nowy_pylon.csv'
    New_Boat_drags_path = New_Boat_drags_path.resolve()

    data_manager_New_Boat_drags = FoilManager('FRONT_DRAG', 'New Front pylons', New_Boat_drags_path, 0, 0,
                                              NACA6409_AREA)
    data_manager_New_Boat_drags.load_data()
    data_manager_New_Boat_drags.clean_data()
    data_manager_New_Boat_drags.multiply_forces_by_2()
    data_manager_New_Boat_drags.calculate_lift_coefficient(WATER_DENSITY)
    data_manager_New_Boat_drags.calculate_drag_coefficient(WATER_DENSITY)

    EPPLER908_CFD_path = script_dir / '..' / '..' / 'data_CFD' / 'CFD_3D_skrzydla_tylnie2021_eppler908_Wyniki_p.csv'
    EPPLER908_CFD_path = EPPLER908_CFD_path.resolve()

    data_manager_EPPLER908 = FoilManager('CFD', 'EPPLER 908', EPPLER908_CFD_path, 0, 0, EPPLER908_AREA)
    data_manager_EPPLER908.load_data()
    data_manager_EPPLER908.clean_data()
    data_manager_EPPLER908.multiply_forces_by_2()
    data_manager_EPPLER908.calculate_lift_coefficient(WATER_DENSITY)
    data_manager_EPPLER908.calculate_drag_coefficient(WATER_DENSITY)
    data_manager_EPPLER908.calculate_cl_cd()

    Celka = Boat(6.039, 1.69, 170)
    Celka.distribution_of_masses(2.676, 3.551, 0.725, 0.386)

    #############################################
    target_velocity = 8.0
    front_angle_of_attack = 0.0
    #############################################
    rear_foil_area, front_foil_area = overall_lift_analysis(target_velocity, data_manager_New_Boat_drags,
                                                            front_angle_of_attack, data_manager_EPPLER908, 0.0, Celka)

    print("Front foil area from CFD data with NEW mountings and pylons")
    print("Parameters:")
    print("Boat mass: ", Celka.mass)
    print("velocity: ", target_velocity)
    print("target angle of attack: ", front_angle_of_attack)
    print("front foil area is: ", front_foil_area)
    print("rear foil area is: ", rear_foil_area)
    print("CURRENT CELKA'S front foil area is: ", NACA6409_AREA)
    print("CURRENT CELKA'S rear foil area is: ", EPPLER908_AREA)

    front_foil_drag, front_pylon_drag, front_mocowanie_drag = overall_front_drag_analysis(front_foil_area,
                                                                                          target_velocity,
                                                                                          data_manager_New_Boat_drags,
                                                                                          front_angle_of_attack)
    rear_foil_drag, front_foil_drag_SYF = foils_drag_analysis(rear_foil_area, front_foil_area, target_velocity,
                                                              data_manager_New_Boat_drags, front_angle_of_attack,
                                                              data_manager_EPPLER908, 0)

    print("Overall drag results:")
    print("front foil drag = ", front_foil_drag)
    print("front pylon drag = ", front_pylon_drag)
    print("front mocowanie drag = ", front_mocowanie_drag)
    print("\nSUM =                ", front_foil_drag + front_pylon_drag + front_mocowanie_drag)

    print("\n\n\n")
    print("rear foil drag = ", rear_foil_drag)
    print("\n\n\n")
    print("Whole boat drag results:")
    whole_boat_drag = 2 * (front_foil_drag + front_pylon_drag + front_mocowanie_drag) + rear_foil_drag
    print("whole boat drag = ", whole_boat_drag)
    print("\n")
    print("!!!!! IT DOESN'T CONSIDER DRAG GENERATED BY GONDOLA !!!!!!")

    return FoilPlotter(data_manager_New_Boat_drags), data_manager_New_Boat_drags


##################################################################################################

# ANALIZA WPŁYWU PRZENIESIENIA ŚRODA MASY NA OPORY - JAK PRZY ZAŁOŻENIU TAKICH SAMYM POWIERZCHNI SKRZYDEŁ
# ZWIĘKSZĄ SIĘ OPORY, JEŚLI SKRZYDŁA BĘDĄ MUSIAŁY KOMPENSOWAĆ ZA DUŻĄ MASĘ KĄTEM NATARCIA
# WYKRESY:
# 1. SIŁA OPORU OD KĄTA NATARCIA W ZAKRESIE ODPOWIADAJĄYM PRĘDKOŚCI W JAKIEJ BĘDZIE LATAĆ ŁÓDŹ
# 2. SIŁA OPORU OD KĄTA NATARCIA PRZY ZAŁOŻONEJ PRĘDKOŚCI, Z ZAZNACZONYM ZAKRESEM DLA MASY NA PYLONIE
# (NIERÓWNYM ROZKŁADZIE MASY)

def not_centered_mass_analysis():
    # Creation of boat
    # Delta Parameters:
    mass = 170
    front_pylon_y_position = 4.3
    front_pylon_x_width = 0.72
    rear_pylon_y_position = 0.7
    front_mass_ratio = 0.66
    ############################

    Delta = Boat(6, 1.6, mass, front_pylon_y_position, front_pylon_x_width, rear_pylon_y_position)
    Delta.center_of_mass_based_on_front_rear_mass_ratio(front_mass_ratio, front_pylon_y_position, front_pylon_x_width,
                                                        rear_pylon_y_position)

    # Foil data preparation
    script_dir = Path(__file__).resolve().parent
    New_Boat_drags_path = script_dir / '..' / '..' / 'data_overall_drag' / 'CFD_3D_opory_latania_nowy_pylon.csv'
    New_Boat_drags_path = New_Boat_drags_path.resolve()

    data_manager_New_Boat_drags = FoilManager('FRONT_DRAG', 'New Front pylons', New_Boat_drags_path, 0, 0,
                                              NACA6409_AREA)
    data_manager_New_Boat_drags.load_data()
    data_manager_New_Boat_drags.clean_data()
    data_manager_New_Boat_drags.multiply_forces_by_2()
    data_manager_New_Boat_drags.calculate_lift_coefficient(WATER_DENSITY)
    data_manager_New_Boat_drags.calculate_drag_coefficient(WATER_DENSITY)

    ################################
    # ASSUMPTIONS
    # target_velocity is the velocity for which the boat is designed. At that velocity the boat should have optimal aoa
    # on foils - at the highest cl/cd value. That is at +1 deg for NACA6409
    target_velocity = 6.5
    front_target_aoa = 1
    rear_target_aoa = 1

    rear_foil_area, front_foil_area = overall_lift_analysis(target_velocity, data_manager_New_Boat_drags,
                                                            front_target_aoa,
                                                            data_manager_New_Boat_drags, rear_target_aoa, Delta)

    print("Rear foil area is: ", rear_foil_area)
    print("Front foil area is: ", front_foil_area)


#####################################
#               KODZIK
#####################################

# Celka_overall_drag_analysis()
# not_centered_mass_analysis()
Celka_overall_lift_analysis()
