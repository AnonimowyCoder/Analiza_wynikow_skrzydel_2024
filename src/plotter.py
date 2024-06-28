import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

class Plotter:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def plot_lift_vs_angle_comparison(self, velocities):
        colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'black']
        
        # Create a figure and an axis
        fig, ax = plt.subplots()
        
        # Plot data for each velocity
        for idx, velocity in enumerate(velocities):
            # Filter data for the current velocity
            df_filtered = self.data_manager.filter_data_by_velocity(velocity)
            
            if not df_filtered.empty:
                # Plot Lift Force vs. Angle of Attack for the current velocity
                ax.plot(df_filtered['angle_of_attack'], df_filtered['lift_force'],
                        label=f'Lift Force at {velocity} m/s', color=colors[idx % len(colors)], marker='x')
        
        # Customize the plot
        ax.set_xlabel('Angle of Attack (degrees)')
        ax.set_ylabel('Lift Force (N)')
        ax.set_title(f'Lift Force vs. Angle of Attack for {self.data_manager.foil_name}')
        ax.grid(True)
        ax.legend()
        
        # Display the plot
        plt.show(block=False)

    def plot_lift_vs_velocity_comparison(self, angles):
        colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'black']
        
        # Create a figure and an axis
        fig, ax = plt.subplots()
        
        # Plot data for each angle
        for idx, angle in enumerate(angles):
            # Filter data for the current angle
            df_filtered = self.data_manager.filter_data_by_angle(angle)
            
            if not df_filtered.empty:
                # Plot Lift Force vs. velocity for the angle
                ax.plot(df_filtered['inlet_vel'], df_filtered['lift_force'],
                        label=f'Lift Force at {angle} deg', color=colors[idx % len(colors)], marker='x')
        
        # Customize the plot
        ax.set_xlabel('Velocity (m/s)')
        ax.set_ylabel('Lift Force (N)')
        ax.set_title(f'Lift Force vs. Velocity for {self.data_manager.foil_name}')
        ax.grid(True)
        ax.legend()
        
        # Display the plot
        plt.show(block=False)
        
    def plot_3d_lift_vs_velocity_and_angle_scatter(self):
        """
        Create a 3D plot with velocity on x-axis, angle of attack on y-axis, and lift force on z-axis.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        data_corrected =  self.data_manager.data[self.data_manager.data['inlet_vel']>=3.0]

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

        data_corrected =  self.data_manager.data[self.data_manager.data['inlet_vel']>=3.0]

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