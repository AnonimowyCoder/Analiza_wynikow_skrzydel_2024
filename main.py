from matplotlib import pyplot as plt
from src.foils_data.FoilManager import FoilManager
from src.foils_data.FoilPlotter import FoilPlotter
from src.utilities.Constants import *


def compare_foils_lift(plotterA, plotterB):
    # Create a single figure with a 2x2 grid of subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Lift Force vs. Angle of Attack Comparison for Different Velocities', fontsize=16)

    # Define the velocities to plot
    velocities = [5.0, 6.0, 7.0, 8.0]

    # Plot each comparison on a different subplot
    for i, velocity in enumerate(velocities):
        row, col = divmod(i, 2)
        ax = axs[row, col]

        plotterA.plot_lift_vs_angle_compare_foils_on_axis(velocity, plotterB.data_manager, ax)

    # Adjust layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Display the plot
    plt.show()


def compare_foils_drag(plotterA, plotterB):
    # Create a single figure with a 2x2 grid of subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Drag Force vs. Angle of Attack Comparison for Different Velocities', fontsize=16)

    # Define the velocities to plot
    velocities = [5.0, 6.0, 7.0, 8.0]

    # Plot each comparison on a different subplot
    for i, velocity in enumerate(velocities):
        row, col = divmod(i, 2)
        ax = axs[row, col]

        plotterA.plot_drag_vs_angle_compare_foils_on_axis(velocity, plotterB.data_manager, ax)

    # Adjust layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Display the plot
    plt.show()


def analysis_AFT_vs_CFD(plotterA, plotterB):
    compare_foils_lift(plotterA, plotterB)
    compare_foils_drag(plotterA, plotterB)


def eppler_396_test_analysis():
    EPPLER396_CFD_path = 'data_CFD/CFD_2D_EPPLER_396_WYNIKI.csv'

    data_manager_EPPLER396 = FoilManager('CFD', 'EPPLER396', EPPLER396_CFD_path)

    data_manager_EPPLER396.load_data()
    data_manager_EPPLER396.clean_data()
    print(data_manager_EPPLER396.data.head(10))


def main():
    # Apply a style
    plt.style.use('ggplot')

    # # File paths to the CSV files
    # NACA6409_CFD_path = 'data_CFD/CFD_3D_skrzydla_przednie2023_batmanowe_NACA6409_Wyniki.csv'
    # NACA64A715_CFD_path = 'data_CFD/CFD_3D_skrzydla_przednie2021_owalne_NACA64A715_Wyniki.csv'
    # NACA6409_AFT_path = 'data_AFT/xf-n6409-il-1000000-n5.csv'
    #
    # # Initialize DataManagers
    # ############################################################
    # data_manager_NACA6409_CFD = FoilManager('CFD', 'NACA 6409', NACA6409_CFD_path, NACA6409_TOTAL_LENGTH,
    #                                         NACA6409_CHORD_LENGTH, NACA6409_AREA)
    # data_manager_NACA6409_CFD.load_data()
    # data_manager_NACA6409_CFD.clean_data()
    # data_manager_NACA6409_CFD.multiply_forces_by_2()
    # data_manager_NACA6409_CFD.calculate_lift_coefficient(WATER_DENSITY)
    # data_manager_NACA6409_CFD.calculate_drag_coefficient(WATER_DENSITY)
    # data_manager_NACA6409_CFD.calculate_cl_cd()
    #
    # #############################################################
    # data_manager_NACA6409_AFT = FoilManager('AFT', 'NACA 6409', NACA6409_AFT_path, NACA6409_TOTAL_LENGTH,
    #                                         NACA6409_CHORD_LENGTH, NACA6409_AREA)
    # data_manager_NACA6409_AFT.load_data()
    # data_manager_NACA6409_AFT.clean_data()
    # data_manager_NACA6409_AFT.calculate_lift(WATER_DENSITY)
    # data_manager_NACA6409_AFT.calculate_drag(WATER_DENSITY)
    # data_manager_NACA6409_AFT.calculate_cl_cd()
    #
    # ##############################################################
    # data_manager_NACA64A715_CFD = FoilManager('CFD', 'NACA 64A715', NACA64A715_CFD_path, NACA64A715_TOTAL_LENGTH,
    #                                           NACA64A715_CHORD_LENGTH, NACA64A715_AREA)
    # data_manager_NACA64A715_CFD.load_data()
    # data_manager_NACA64A715_CFD.clean_data()
    # data_manager_NACA64A715_CFD.multiply_forces_by_2()
    # data_manager_NACA64A715_CFD.calculate_lift_coefficient(WATER_DENSITY)
    # data_manager_NACA64A715_CFD.calculate_drag_coefficient(WATER_DENSITY)
    # data_manager_NACA64A715_CFD.calculate_cl_cd()
    #
    # plotter_NACA6409_CFD = FoilPlotter(data_manager_NACA6409_CFD)
    # plotter_NACA6409_AFT = FoilPlotter(data_manager_NACA6409_AFT)
    # plotter_NACA64A715_CFD = FoilPlotter(data_manager_NACA64A715_CFD)
    #
    # analysis_AFT_vs_CFD(plotter_NACA6409_CFD, plotter_NACA6409_AFT)
    #
    # compare_foils_lift(plotter_NACA6409_CFD, plotter_NACA64A715_CFD)
    # compare_foils_drag(plotter_NACA6409_CFD, plotter_NACA64A715_CFD)

    eppler_396_test_analysis()

    exit_call = input("Press whatever to exit")


if __name__ == '__main__':
    main()
