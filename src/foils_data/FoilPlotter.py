import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import make_interp_spline

matplotlib.use('TkAgg')


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

        plotterA._plot_lift_vs_angle_compare_foils_on_axis(velocity, plotterB.data_manager, ax)

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

        plotterA._plot_drag_vs_angle_compare_foils_on_axis(velocity, plotterB.data_manager, ax)

    # Adjust layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Display the plot
    plt.show()


class FoilPlotter:

    def __init__(self, data_manager):
        self.data_manager = data_manager

    def plot_lift_vs_angle_compare_velocities(self, velocities, highlight_value=None):
        colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'black']

        # Create a figure and an axis
        fig, ax = plt.subplots()

        # Plot data for each velocity
        for idx, velocity in enumerate(velocities):
            # Filter data for the current velocity
            df_filtered = self.data_manager.filter_data_by_velocity(velocity)

            if not df_filtered.empty:
                # Sort data to avoid interpolation issues
                df_filtered = df_filtered.sort_values(by='angle_of_attack')

                x = df_filtered['angle_of_attack'].values
                y = df_filtered['lift_force'].values

                # Generate smooth interpolation
                if len(x) > 2:  # Need at least 3 points for quadratic interpolation
                    x_smooth = np.linspace(x.min(), x.max(), 200)
                    spline = make_interp_spline(x, y, k=2)  # Quadratic interpolation
                    y_smooth = spline(x_smooth)

                    ax.plot(x_smooth, y_smooth, color=colors[idx % len(colors)], label=f'Lift Force at {velocity} m/s')
                else:
                    ax.plot(x, y, color=colors[idx % len(colors)], label=f'Lift Force at {velocity} m/s')

                # Plot original data points
                ax.scatter(x, y, color=colors[idx % len(colors)], marker='x')

        if highlight_value is not None:
            ax.axhline(y=highlight_value, color='red', linestyle='--', label=f'Highlight: {highlight_value} N')

        # Customize the plot
        ax.set_xlabel('Angle of Attack (degrees)')
        ax.set_ylabel('Lift Force (N)')
        ax.set_title(f'Lift Force vs. Angle of Attack for {self.data_manager.foil_name}')
        ax.grid(True)
        ax.legend()

        # Display the plot
        plt.show(block=True)

    def plot_lift_coefficient_at_target_velocity_compare_foils(self, velocity, other_data_manager):
        colors = ['blue', 'green']  # Colors for two different foils

        # Create a figure and an axis
        fig, ax = plt.subplots()

        # Plot data for the main data manager (self.data_manager)
        df_filtered_main = self.data_manager.filter_data_by_velocity(velocity)
        if not df_filtered_main.empty:
            ax.plot(df_filtered_main['angle_of_attack'], df_filtered_main['lift_coefficient'],
                    label=f'{self.data_manager.foil_name} - cl at {velocity} m/s',
                    color=colors[0], marker='x')

        # Plot data for the other data manager (other_data_manager)
        df_filtered_other = other_data_manager.filter_data_by_velocity(velocity)
        if not df_filtered_other.empty:
            ax.plot(df_filtered_other['angle_of_attack'], df_filtered_other['lift_coefficient'],
                    label=f'{other_data_manager.foil_name} - cl at {velocity} m/s',
                    color=colors[1], marker='x')

        # Customize the plot
        ax.set_xlabel('Angle of Attack (degrees)')
        ax.set_ylabel('Lift coefficient')
        ax.set_title(
            f'cl vs. AoA for {self.data_manager.foil_name} and {other_data_manager.foil_name}')
        ax.grid(True)
        ax.legend()

        # Display the plot
        plt.show(block=True)

    def plot_drag_coefficient_at_target_velocity_compare_foils(self, velocity, other_data_manager):
        colors = ['blue', 'green']  # Colors for two different foils

        # Create a figure and an axis
        fig, ax = plt.subplots()

        # Plot data for the main data manager (self.data_manager)
        df_filtered_main = self.data_manager.filter_data_by_velocity(velocity)
        if not df_filtered_main.empty:
            ax.plot(df_filtered_main['angle_of_attack'], df_filtered_main['drag_coefficient'],
                    label=f'{self.data_manager.foil_name} - cd at {velocity} m/s',
                    color=colors[0], marker='x')

        # Plot data for the other data manager (other_data_manager)
        df_filtered_other = other_data_manager.filter_data_by_velocity(velocity)
        if not df_filtered_other.empty:
            ax.plot(df_filtered_other['angle_of_attack'], df_filtered_other['drag_coefficient'],
                    label=f'{other_data_manager.foil_name} - cd at {velocity} m/s',
                    color=colors[1], marker='x')

        # Customize the plot
        ax.set_xlabel('Angle of Attack (degrees)')
        ax.set_ylabel('Drag coefficient')
        ax.set_title(
            f'cd vs. AoA for {self.data_manager.foil_name} and {other_data_manager.foil_name}')
        ax.grid(True)
        ax.legend()

        # Display the plot
        plt.show(block=True)

    def plot_drag_force_target_velocity_compare_foils(self, velocity, *other_data_managers):
        # Define a list of colors for the plots. Using 'tab20' for more distinctive colors
        colors = plt.cm.get_cmap('tab20', len(other_data_managers) + 1)  # Including the instance's data manager

        # Create a figure and an axis
        fig, ax = plt.subplots()

        # Plot data for the instance's own data manager
        df_filtered_main = self.data_manager.filter_data_by_velocity(velocity)
        if not df_filtered_main.empty:
            ax.plot(df_filtered_main['angle_of_attack'], df_filtered_main['drag_force'],
                    label=f'{self.data_manager.foil_name} - drag at {velocity} m/s',
                    color=colors(0), marker='x')

        # Loop through each additional data manager and plot its data
        for idx, dm in enumerate(other_data_managers):
            df_filtered = dm.filter_data_by_velocity(velocity)
            if not df_filtered.empty:
                ax.plot(df_filtered['angle_of_attack'], df_filtered['drag_force'],
                        label=f'{dm.foil_name} - drag at {velocity} m/s',
                        color=colors(idx + 1), marker='x')

        # Customize the plot
        ax.set_xlabel('Angle of Attack (degrees)')
        ax.set_ylabel('drag force [N]')
        ax.set_title(f'drag vs. AoA at {velocity} m/s')
        ax.grid(True)
        ax.legend()

        # Enable interactive mode
        plt.ion()

        # Display the plot
        plt.show()

        # Keep the plot open for interaction
        plt.pause(0.001)

        # To keep the plot open indefinitely, use plt.show(block=True) at the end
        plt.show(block=True)

    def plot_cl_cd_at_target_velocity_compare_foils(self, velocity, *other_data_managers):
        # Define a list of colors for the plots. Using 'tab20' for more distinctive colors
        colors = plt.cm.get_cmap('tab20', len(other_data_managers) + 1)  # Including the instance's data manager

        # Create a figure and an axis
        fig, ax = plt.subplots()

        # Plot data for the instance's own data manager
        df_filtered_main = self.data_manager.filter_data_by_velocity(velocity)
        if not df_filtered_main.empty:
            ax.plot(df_filtered_main['angle_of_attack'], df_filtered_main['cl_cd'],
                    label=f'{self.data_manager.foil_name} - cl/cd at {velocity} m/s',
                    color=colors(0), marker='x')

        # Loop through each additional data manager and plot its data
        for idx, dm in enumerate(other_data_managers):
            df_filtered = dm.filter_data_by_velocity(velocity)
            if not df_filtered.empty:
                ax.plot(df_filtered['angle_of_attack'], df_filtered['cl_cd'],
                        label=f'{dm.foil_name} - cl/cd at {velocity} m/s',
                        color=colors(idx + 1), marker='x')

        # Customize the plot
        ax.set_xlabel('Angle of Attack (degrees)')
        ax.set_ylabel('cl/cd')
        ax.set_title(f'cl/cd vs. AoA at {velocity} m/s')
        ax.grid(True)
        ax.legend()

        # Enable interactive mode
        plt.ion()

        # Display the plot
        plt.show()

        # Keep the plot open for interaction
        plt.pause(0.001)

        # To keep the plot open indefinitely, use plt.show(block=True) at the end
        plt.show(block=True)

    def plot_cl_cd_at_target_velocities(self, velocities):
        colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'black']

        # Create a figure and an axis
        fig, ax = plt.subplots()

        # Plot data for each velocity
        for idx, velocity in enumerate(velocities):
            # Filter data for the current velocity
            df_filtered = self.data_manager.filter_data_by_velocity(velocity)

            if not df_filtered.empty:
                # Sort data to avoid interpolation issues
                df_filtered = df_filtered.sort_values(by='angle_of_attack')

                x = df_filtered['angle_of_attack'].values
                y = df_filtered['cl_cd'].values

                # Generate smooth quadratic interpolation
                if len(x) > 2:  # At least 3 points needed for quadratic interpolation
                    x_smooth = np.linspace(x.min(), x.max(), 200)
                    spline = make_interp_spline(x, y, k=3)  # Quadratic interpolation
                    y_smooth = spline(x_smooth)

                    ax.plot(x_smooth, y_smooth, color=colors[idx % len(colors)], label=f'cl/cd at {velocity} m/s')
                else:
                    ax.plot(x, y, color=colors[idx % len(colors)], label=f'cl/cd at {velocity} m/s')

                # Plot original data points
                ax.scatter(x, y, color=colors[idx % len(colors)], marker='x')

        # Customize the plot
        ax.set_xlabel('Angle of Attack')
        ax.set_ylabel('cl/cd')
        ax.set_title(f'cl/cd at Different Velocities for {self.data_manager.foil_name}')
        ax.grid(True)
        ax.legend()

        # Display the plot
        plt.show(block=True)

    def plot_lift_vs_velocity_compare_angles(self, angles):
        colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'black']

        # Create a figure and an axis
        fig, ax = plt.subplots()

        # Plot data for each angle
        for idx, angle in enumerate(angles):
            # Filter data for the current angle
            df_filtered = self.data_manager.filter_data_by_angle(angle)

            if not df_filtered.empty:
                # Sort data to avoid interpolation issues
                df_filtered = df_filtered.sort_values(by='inlet_vel')

                x = df_filtered['inlet_vel'].values
                y = df_filtered['lift_force'].values

                # Generate smooth quadratic interpolation
                if len(x) > 2:  # At least 3 points needed for quadratic interpolation
                    x_smooth = np.linspace(x.min(), x.max(), 200)
                    spline = make_interp_spline(x, y, k=2)  # Quadratic interpolation
                    y_smooth = spline(x_smooth)

                    ax.plot(x_smooth, y_smooth, color=colors[idx % len(colors)], label=f'Lift Force at {angle}°')
                else:
                    ax.plot(x, y, color=colors[idx % len(colors)], label=f'Lift Force at {angle}°')

                # Plot original data points
                ax.scatter(x, y, color=colors[idx % len(colors)], marker='x')

        # Customize the plot
        ax.set_xlabel('Velocity (m/s)')
        ax.set_ylabel('Lift Force (N)')
        ax.set_title(f'Lift Force vs. Velocity for {self.data_manager.foil_name}')
        ax.grid(True)
        ax.legend()

        # Display the plot
        plt.show(block=True)

    def plot_3d_lift_vs_velocity_and_angle_scatter(self):
        """
        Create a 3D plot with velocity on x-axis, angle of attack on y-axis, and lift force on z-axis.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        data_corrected = self.data_manager.data[self.data_manager.data['inlet_vel'] >= 3.0]

        x = data_corrected['inlet_vel']
        y = data_corrected['angle_of_attack']
        z = data_corrected['lift_force']

        ax.scatter(x, y, z, c='b', marker='o')

        # Set labels
        ax.set_xlabel('Velocity (m/s)')
        ax.set_ylabel('Angle of Attack (degrees)')
        ax.set_zlabel('Lift Force (N)')

        # Set title
        ax.set_title(f'3D Plot of Lift Force vs Velocity and Angle of Attack for {self.data_manager.foil_name}')

        # Show plot
        plt.show(block=False)

    def plot_3d_lift_vs_velocity_and_angle_surface(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        data_corrected = self.data_manager.data[self.data_manager.data['inlet_vel'] >= 3.0]

        x = data_corrected['inlet_vel']
        y = data_corrected['angle_of_attack']
        z = data_corrected['lift_force']

        ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')

        # Set labels
        ax.set_xlabel('Velocity (m/s)')
        ax.set_ylabel('Angle of Attack (degrees)')
        ax.set_zlabel('Lift Force (N)')

        # Set title
        ax.set_title(f'3D Surface Plot of Lift Force vs Velocity and Angle of Attack for {self.data_manager.foil_name}')

        # Show plot
        plt.show(block=False)

    def plot_lift_vs_angle_compare_foils(self, velocity, other_data_manager):
        """
        Compare lift force vs. angle of attack for two different foils.
        
        Parameters:
        velocity (float): The inlet velocity to compare for.
        other_data_manager (DataManager): Another instance of DataManager containing data for the other foil.
        """
        colors = ['blue', 'green']  # Colors for two different foils

        # Create a figure and an axis
        fig, ax = plt.subplots()

        # Plot data for the main data manager (self.data_manager)
        df_filtered_main = self.data_manager.filter_data_by_velocity(velocity)
        if not df_filtered_main.empty:
            ax.plot(df_filtered_main['angle_of_attack'], df_filtered_main['lift_force'],
                    label=f'{self.data_manager.foil_name} - Lift Force at {velocity} m/s',
                    color=colors[0], marker='x')

        # Plot data for the other data manager (other_data_manager)
        df_filtered_other = other_data_manager.filter_data_by_velocity(velocity)
        if not df_filtered_other.empty:
            ax.plot(df_filtered_other['angle_of_attack'], df_filtered_other['lift_force'],
                    label=f'{other_data_manager.foil_name} - Lift Force at {velocity} m/s',
                    color=colors[1], marker='x')

        # Customize the plot
        ax.set_xlabel('Angle of Attack (degrees)')
        ax.set_ylabel('Lift Force (N)')
        ax.set_title(
            f'Lift Force vs. Angle of Attack Comparison for {self.data_manager.foil_name} vs. {other_data_manager.foil_name}')
        ax.grid(True)
        ax.legend()

        # Display the plot
        plt.show(block=True)

    def _plot_lift_vs_angle_compare_foils_on_axis(self, velocity, other_data_manager, ax):
        """
        Compare lift force vs. angle of attack for two different foils on a given axis.
        
        Parameters:
        velocity (float): The inlet velocity to compare for.
        other_data_manager (DataManager): Another instance of DataManager containing data for the other foil.
        ax (matplotlib.axes.Axes): The axis to plot on.
        """
        colors = ['blue', 'green']  # Colors for two different foils

        # Plot data for the main data manager (self.data_manager)
        df_filtered_main = self.data_manager.filter_data_by_velocity(velocity)
        if not df_filtered_main.empty:
            ax.plot(df_filtered_main['angle_of_attack'], df_filtered_main['lift_force'],
                    label=f'{self.data_manager.foil_name}, {self.data_manager.results_type}',
                    color=colors[0], marker='x')

        # Plot data for the other data manager (other_data_manager)
        df_filtered_other = other_data_manager.filter_data_by_velocity(velocity)
        if not df_filtered_other.empty:
            ax.plot(df_filtered_other['angle_of_attack'], df_filtered_other['lift_force'],
                    label=f'{other_data_manager.foil_name}, {other_data_manager.results_type}',
                    color=colors[1], marker='x')

        # Customize the plot
        ax.set_xlabel('Angle of Attack (degrees)')
        ax.set_ylabel('Lift Force (N)')
        ax.set_title(f'Lift Force vs. AoA at {velocity} m/s')
        ax.grid(True)
        ax.legend()

    def _plot_drag_vs_angle_compare_foils_on_axis(self, velocity, other_data_manager, ax):
        """
        Compare drag force vs. angle of attack for two different foils on a given axis.
        
        Parameters:
        velocity (float): The inlet velocity to compare for.
        other_data_manager (DataManager): Another instance of DataManager containing data for the other foil.
        ax (matplotlib.axes.Axes): The axis to plot on.
        """
        colors = ['blue', 'green']  # Colors for two different foils

        # Plot data for the main data manager (self.data_manager)
        df_filtered_main = self.data_manager.filter_data_by_velocity(velocity)
        if not df_filtered_main.empty:
            ax.plot(df_filtered_main['angle_of_attack'], df_filtered_main['drag_force'],
                    label=f'{self.data_manager.foil_name}, {self.data_manager.results_type}',
                    color=colors[0], marker='x')

        # Plot data for the other data manager (other_data_manager)
        df_filtered_other = other_data_manager.filter_data_by_velocity(velocity)
        if not df_filtered_other.empty:
            ax.plot(df_filtered_other['angle_of_attack'], df_filtered_other['drag_force'],
                    label=f'{other_data_manager.foil_name}, {other_data_manager.results_type}',
                    color=colors[1], marker='x')

        # Customize the plot
        ax.set_xlabel('Angle of Attack (degrees)')
        ax.set_ylabel('Drag Force (N)')
        ax.set_title(f'Drag Force vs. AoA at {velocity} m/s')
        ax.grid(True)
        ax.legend()

    def plot_pressure_center_vs_angle_at_target_velocities(self, velocities):
        colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'black']

        fig, ax = plt.subplots()

        for idx, velocity in enumerate(velocities):
            df_filtered = self.data_manager.filter_data_by_velocity(velocity)

            if df_filtered.empty:
                print(f'Brak danych dla prędkości {velocity} m/s')
                continue

            df_filtered = df_filtered.sort_values(by='angle_of_attack')

            x = df_filtered['angle_of_attack'].values
            y = df_filtered['pressure_center'].values

            # Interpolacja dla płynniejszej krzywej
            if len(x) > 2:
                x_smooth = np.linspace(x.min(), x.max(), 200)
                spline = make_interp_spline(x, y, k=3)
                y_smooth = spline(x_smooth)
                ax.plot(x_smooth, y_smooth, color=colors[idx % len(colors)], label=f'Pressure Center at {velocity} m/s')
            else:
                ax.plot(x, y, color=colors[idx % len(colors)], label=f'Pressure Center at {velocity} m/s')

            # Oryginalne punkty danych
            ax.scatter(x, y, color=colors[idx % len(colors)], marker='x')

        # Konfiguracja wykresu
        ax.set_xlabel('Angle of Attack (°)')
        ax.set_ylabel('Pressure Center Position on Chord')
        ax.set_title(f'Pressure Center vs Angle of Attack for {self.data_manager.foil_name}')
        ax.grid(True)
        ax.legend()

        plt.show(block=True)
