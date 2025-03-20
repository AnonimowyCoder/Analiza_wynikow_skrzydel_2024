from matplotlib import pyplot as plt
from src.foils_data.FoilManager import FoilManager, foil_manager_procedure
from src.foils_data.FoilPlotter import FoilPlotter, compare_foils_lift, compare_foils_drag
from src.utilities.Constants import *


def main():
    # Apply a style
    plt.style.use('ggplot')

    # File paths to the CSV files
    NACA6409_CFD_path = 'data_CFD/CFD_3D_skrzydla_przednie2023_batmanowe_NACA6409_Wyniki_p.csv'
    NACA64A715_CFD_path = 'data_CFD/CFD_3D_skrzydla_przednie2021_owalne_NACA64A715_Wyniki_p.csv'
    EPPLER396_CFD_path = 'data_CFD/CFD_2D_EPPLER_396_WYNIKI.csv'
    NACA6409_AFT_path = 'data_AFT/xf-n6409-il-1000000-n5.csv'
    EPPLER908_CFD_path = 'data_CFD/CFD_3D_skrzydla_tylnie2021_eppler908_Wyniki_p.csv'
    NACA_0_033_path = 'data_CFD/CFD_3D_naca_6409_pow_0.033.csv'

    # Initialize DataManagers
    ############################################################

    data_manager_NACA_0_033 = foil_manager_procedure('CFD', 'NACA_0_033', NACA_0_033_path, NACA_0_033_AREA,
                                                     NACA_0_033_CHORD_LENGTH)

    ############################################################
    data_manager_NACA6409 = foil_manager_procedure('CFD', 'NACA 6409', NACA6409_CFD_path,
                                                   NACA6409_AREA, NACA6409_CHORD_LENGTH)

    ##############################################################
    data_manager_NACA64A715 = foil_manager_procedure('CFD', 'NACA 64A715', NACA64A715_CFD_path,
                                                     NACA64A715_AREA, NACA64A715_CHORD_LENGTH)

    ##############################################################
    data_manager_EPPLER908 = foil_manager_procedure('CFD', 'EPPLER908', EPPLER908_CFD_path, EPPLER908_AREA, 0.0, True,
                                                    False)

    plotter_NACA6409_CFD = FoilPlotter(data_manager_NACA6409)
    plotter_NACA64A715_CFD = FoilPlotter(data_manager_NACA64A715)
    plotter_EPPLER908_CFD = FoilPlotter(data_manager_EPPLER908)
    plotter_NACA_0_033_CFD = FoilPlotter(data_manager_NACA_0_033)

    plotter_NACA_0_033_CFD.plot_pressure_center_vs_angle_at_target_velocities({6, 8, 10, 12})
    plotter_NACA6409_CFD.plot_pressure_center_vs_angle_at_target_velocities({6, 8, 10, 12})

    #plotter_NACA_0_033_CFD.plot_lift_vs_velocity_compare_angles([-2,0,2,4])
    #plotter_NACA_0_033_CFD.plot_lift_vs_velocity_compare_angles([-2,0,2,4,6,8])
    plotter_NACA_0_033_CFD.plot_cl_cd_at_target_velocities([6, 8, 10, 12])

    #compare_foils_lift(plotter_EPPLER908_CFD, plotter_NACA6409_CFD)
    # compare_foils_drag(plotter_EPPLER908_CFD, plotter_NACA6409_CFD)
    # plotter_EPPLER908_CFD.plot_cl_cd_at_target_velocity_compare_foils(8, data_manager_NACA6409_CFD_bad)
    #plotter_EPPLER908_CFD.plot_cl_cd_at_target_velocities({6, 6.5, 7, 7.5})
    # plotter_EPPLER908_CFD.plot_lift_coefficient_at_target_velocity_compare_foils(8, data_manager_NACA6409_CFD_bad)

    # analysis_AFT_vs_CFD(plotter_NACA6409_CFD, plotter_NACA6409_AFT)
    # compare_foils_lift(plotter_NACA6409_CFD, plotter_NACA64A715_CFD)
    # compare_foils_drag(plotter_NACA6409_CFD, plotter_EPPLER908_CFD)
    #
    # plotter_NACA6409_CFD.plot_cl_cd_at_target_velocity_compare_foils(7, data_manager_EPPLER396)
    #plotter_EPPLER908_CFD.plot_lift_vs_angle_compare_velocities({7, 7.5, 8},53*GRAVITATIONAL_ACCELERATION)
    #plotter_NACA6409_CFD.plot_cl_cd_at_target_velocities({7, 8})
    #plotter_NACA6409_CFD.plot_drag_force_target_velocity_compare_foils(8)
    exit_call = input("Press whatever to exit")


if __name__ == '__main__':
    main()
