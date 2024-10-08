from matplotlib import pyplot as plt
from src.foils_data.FoilManager import FoilManager
from src.foils_data.FoilPlotter import FoilPlotter, compare_foils_lift, compare_foils_drag
from src.utilities.Constants import *


def analysis_AFT_vs_CFD(plotterA, plotterB):
    compare_foils_lift(plotterA, plotterB)
    compare_foils_drag(plotterA, plotterB)


def main():
    # Apply a style
    plt.style.use('ggplot')

    # File paths to the CSV files
    NACA6409_CFD_path = 'data_CFD/CFD_3D_skrzydla_przednie2023_batmanowe_NACA6409_Wyniki_p.csv'
    NACA64A715_CFD_path = 'data_CFD/CFD_3D_skrzydla_przednie2021_owalne_NACA64A715_Wyniki_p.csv'
    EPPLER396_CFD_path = 'data_CFD/CFD_2D_EPPLER_396_WYNIKI.csv'
    NACA6409_AFT_path = 'data_AFT/xf-n6409-il-1000000-n5.csv'
    EPPLER908_CFD_path = 'data_CFD/CFD_3D_skrzydla_tylnie2021_eppler908_Wyniki_p.csv'

    # Initialize DataManagers
    ############################################################
    data_manager_NACA6409_CFD = FoilManager('CFD', 'NACA 6409', NACA6409_CFD_path, NACA6409_TOTAL_LENGTH,
                                            NACA6409_CHORD_LENGTH, NACA6409_AREA)
    data_manager_NACA6409_CFD.load_data()
    data_manager_NACA6409_CFD.clean_data()
    data_manager_NACA6409_CFD.multiply_forces_by_2()
    data_manager_NACA6409_CFD.calculate_lift_coefficient(WATER_DENSITY)
    data_manager_NACA6409_CFD.calculate_drag_coefficient(WATER_DENSITY)
    data_manager_NACA6409_CFD.calculate_cl_cd()

    #############################################################
    data_manager_NACA6409_AFT = FoilManager('AFT', 'NACA 6409', NACA6409_AFT_path, NACA6409_TOTAL_LENGTH,
                                            NACA6409_CHORD_LENGTH, NACA6409_AREA)
    data_manager_NACA6409_AFT.load_data()
    data_manager_NACA6409_AFT.clean_data()
    data_manager_NACA6409_AFT.calculate_lift(WATER_DENSITY)
    data_manager_NACA6409_AFT.calculate_drag(WATER_DENSITY)
    data_manager_NACA6409_AFT.calculate_cl_cd()

    ##############################################################
    data_manager_NACA64A715_CFD = FoilManager('CFD', 'NACA 64A715', NACA64A715_CFD_path, NACA64A715_TOTAL_LENGTH,
                                              NACA64A715_CHORD_LENGTH, NACA64A715_AREA)
    data_manager_NACA64A715_CFD.load_data()
    data_manager_NACA64A715_CFD.clean_data()
    data_manager_NACA64A715_CFD.multiply_forces_by_2()
    data_manager_NACA64A715_CFD.calculate_lift_coefficient(WATER_DENSITY)
    data_manager_NACA64A715_CFD.calculate_drag_coefficient(WATER_DENSITY)
    data_manager_NACA64A715_CFD.calculate_cl_cd()

    #############################################################
    data_manager_EPPLER396 = FoilManager('CFD', 'EPPLER396', EPPLER396_CFD_path)
    data_manager_EPPLER396.load_data()
    data_manager_EPPLER396.clean_data()
    data_manager_EPPLER396.calculate_cl_cd()

    ##############################################################
    data_manager_EPPLER908 = FoilManager('CFD', 'EPPLER908', EPPLER908_CFD_path, 0, 0, EPPLER908_AREA)
    data_manager_EPPLER908.load_data()
    data_manager_EPPLER908.clean_data()
    data_manager_EPPLER908.multiply_forces_by_2()
    data_manager_EPPLER908.calculate_lift_coefficient(WATER_DENSITY)
    data_manager_EPPLER908.calculate_drag_coefficient(WATER_DENSITY)
    data_manager_EPPLER908.calculate_cl_cd()

    plotter_NACA6409_CFD = FoilPlotter(data_manager_NACA6409_CFD)
    plotter_NACA6409_AFT = FoilPlotter(data_manager_NACA6409_AFT)
    plotter_NACA64A715_CFD = FoilPlotter(data_manager_NACA64A715_CFD)
    plotter_EPPLER908_CFD = FoilPlotter(data_manager_EPPLER908)

    # compare_foils_lift(plotter_EPPLER908_CFD, plotter_NACA6409_CFD)
    # compare_foils_drag(plotter_EPPLER908_CFD, plotter_NACA6409_CFD)
    # plotter_EPPLER908_CFD.plot_cl_cd_at_target_velocity_compare_foils(8, data_manager_NACA6409_CFD_bad)
    # plotter_EPPLER908_CFD.plot_cl_cd_at_target_velocities({6, 6.5, 7, 7.5})
    # plotter_EPPLER908_CFD.plot_lift_coefficient_at_target_velocity_compare_foils(8, data_manager_NACA6409_CFD_bad)

    # analysis_AFT_vs_CFD(plotter_NACA6409_CFD, plotter_NACA6409_AFT)
    # compare_foils_lift(plotter_NACA6409_CFD, plotter_NACA64A715_CFD)
    # compare_foils_drag(plotter_NACA6409_CFD, plotter_EPPLER908_CFD)
    #
    # plotter_NACA6409_CFD.plot_cl_cd_at_target_velocity_compare_foils(7, data_manager_EPPLER396)
    #plotter_EPPLER908_CFD.plot_lift_vs_angle_compare_velocities({7, 7.5, 8},53*GRAVITATIONAL_ACCELERATION)
    #plotter_NACA6409_CFD.plot_cl_cd_at_target_velocities({7, 8})
    plotter_NACA6409_CFD.plot_drag_force_target_velocity_compare_foils(8)
    exit_call = input("Press whatever to exit")


if __name__ == '__main__':
    main()
