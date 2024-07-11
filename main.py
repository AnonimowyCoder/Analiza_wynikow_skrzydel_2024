from matplotlib import pyplot as plt
from src.FoilManager import FoilManager
from src.FoilPlotter import FoilPlotter

def select_and_plot(plotter):
    while True:
        # User interaction for selecting the plot
        print("Select the plot you want to show:")
        print("1. Lift vs Angle Comparison for Different Velocities")
        print("2. Lift vs Velocity Comparison for Different Angles")
        print("3. 3D Scatter Plot of Lift vs Velocity and Angle of Attack")
        print("4. 3D Surface Plot of Lift vs Velocity and Angle of Attack")
        print("5. Exit")
        
        choice = input("Enter the number of your choice: ")

        if choice == '1':
            velocities = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
            plotter.plot_lift_vs_angle_comparison(velocities)
        elif choice == '2':
            angles = [0, 1, 2, 3, 4, 5]
            plotter.plot_lift_vs_velocity_comparison(angles)
        elif choice == '3':
            plotter.plot_3d_lift_vs_velocity_and_angle_scatter()
        elif choice == '4':
            plotter.plot_3d_lift_vs_velocity_and_angle_surface()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

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


def main():

    # Apply a style 
    plt.style.use('ggplot')

    # File paths to the CSV files
    NACA6409_CFD_path = 'data_CFD/CFD_3D_skrzydla_przednie2023_batmanowe_NACA6409_Wyniki.csv'
    NACA64A715_CFD_path = 'data_CFD/CFD_3D_skrzydla_przednie2021_owalne_NACA64A715_Wyniki.csv'
    NACA6409_AFT_path = 'data_AFT/xf-n6409-il-1000000-n5.csv'

    # Initialize DataManager and load data
    data_manager_NACA6409_CFD = FoilManager('CFD','NACA 6409',NACA6409_CFD_path,732,100,64219)
    data_manager_NACA6409_CFD.load_data()
    data_manager_NACA6409_CFD.clean_data()

    data_manager_NACA6409_AFT = FoilManager('AFT','NACA 6409',NACA6409_AFT_path)
    data_manager_NACA6409_AFT.load_data()
    data_manager_NACA6409_AFT.clean_data()
    print(data_manager_NACA6409_AFT.data.head(10))

    data_manager_NACA64A715_CFD = FoilManager('CFD','NACA 64A715',NACA64A715_CFD_path,830,105,68615)
    data_manager_NACA64A715_CFD.load_data()
    data_manager_NACA64A715_CFD.clean_data()

    plotter_NACA6409 = FoilPlotter(data_manager_NACA6409_CFD)
    plotter_NACA64A715 = FoilPlotter(data_manager_NACA64A715_CFD)

    compare_foils_lift(plotter_NACA6409,plotter_NACA64A715)

    compare_foils_drag(plotter_NACA6409, plotter_NACA64A715)

    exit_call = input("Press whatever to exit")


if __name__ == '__main__':
    main()