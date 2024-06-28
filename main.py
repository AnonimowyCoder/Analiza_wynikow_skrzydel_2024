from src.data_manager import DataManager
from src.plotter import Plotter

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


def main():
    # File paths to the CSV files
    NACA6409_data = 'data/CFD_3D_skrzydla_przednie2023_batmano3we_NACA6409_Wyniki.csv'
    NACA64A715_data = 'data/CFD_3D_skrzydla_przednie2021_owalne_NACA64A715_Wyniki.csv'

    # Initialize DataManager and load data
    data_manager_NACA6409 = DataManager('NACA 6409',NACA6409_data)
    data_manager_NACA6409.load_data()
    data_manager_NACA6409.clean_data()

    data_manager_NACA64A715 = DataManager('NACA 64A715',NACA64A715_data)
    data_manager_NACA64A715.load_data()
    data_manager_NACA64A715.clean_data()

    # Call the plot selection and plotting logic
    select_and_plot(Plotter(data_manager_NACA6409))
    select_and_plot(Plotter(data_manager_NACA64A715))


if __name__ == '__main__':
    main()