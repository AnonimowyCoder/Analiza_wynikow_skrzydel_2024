from shapely import LineString
from shapely.geometry import Point
import pandas as pd


def read_boat_data(csv_path, row_index=0):
    """
    Function to read the boat data from csv file.
    :param csv_path:
    :param row_index:
    :return: Boat
    """
    df = pd.read_csv(csv_path)

    # Check if the row_index is within the range of the DataFrame
    if row_index >= len(df):
        raise IndexError("The specified row index is out of range.")

    boat_data = df.iloc[row_index]
    boat = Boat(
        length=boat_data['length'],
        width=boat_data['width'],
        mass=boat_data['mass'],
        mass_center_y_position=boat_data['mass_center_y_position'],
        front_pylons_y_position=boat_data['front_pylons_y_position'],
        front_pylons_x_width=boat_data['front_pylons_x_width'],
        rear_pylon_y_position=boat_data['rear_pylon_y_position'],
        rear_pylon_mass=boat_data['rear_pylon_mass'],
        front_pylon_right_mass=boat_data['front_pylon_right_mass'],
        front_pylon_left_mass=boat_data['front_pylon_left_mass']
    )
    return boat


class Boat:
    def __init__(self, length, width, mass, front_pylons_y_position=0,
                 front_pylons_x_width=0, rear_pylon_y_position=0, mass_center_y_position=0, rear_pylon_mass=0.0,
                 front_pylon_right_mass=0.0,
                 front_pylon_left_mass=0.0):
        """
        Class representing the Boat Blueprint

        The center of coordinate system is in the middle of the back of the boat.
        Hence there are no negative 'y' coordinates.
        The center of mass is considered to be on 'y' axis.
        The rear pylon is considered to be on 'y' axis.

        :param length: length of the Boat [m]
        :param width: width of the Boat [m]
        :param mass: mass of the Boat [kg]
        :param front_pylons_y_position: position of front pylons in 'y' axis [m]
        :param front_pylons_x_width: width of front pylons in 'y' axis [m]
        :param rear_pylon_y_position: position of rear pylons in 'y' axis [m]
        :param mass_center_y_position: centre of mass in 'y' axis [m]
        """
        self.length = length
        self.width = width
        self.mass = mass
        self.mass_center_y_position = mass_center_y_position
        self.front_pylons_y_position = front_pylons_y_position
        self.front_pylons_x_width = front_pylons_x_width
        self.rear_pylon_y_position = rear_pylon_y_position
        self.rear_pylon_mass = rear_pylon_mass
        self.front_pylon_right_mass = front_pylon_right_mass
        self.front_pylon_left_mass = front_pylon_left_mass

    def center_of_mass_based_on_front_rear_mass_ratio(self, front_pylons_mass_ratio, front_pylons_y_position,
                                                      front_pylons_x_width, rear_pylon_y_position):
        """
        Function that calculates the position of center of mass based on mass distribution ration on pylons. Requires the
        positions of pylons.

        Uses simple geometric relationship:
        mass_center_y_position = front_pylons_y_position - (front_pylons_y_position - rear_pylon_y_position) * (rear_pylon_mass / mass)

        :param front_pylons_mass_ratio: the ratio (0 - 1) of the mass carried by front pylons
        :param front_pylons_y_position:
        :param front_pylons_x_width:
        :param rear_pylon_y_position:
        """
        self.front_pylons_y_position = front_pylons_y_position
        self.front_pylons_x_width = front_pylons_x_width
        self.rear_pylon_y_position = rear_pylon_y_position

        # Calculation of pylons masses
        front_pylon_mass = (self.mass * front_pylons_mass_ratio) / 2
        self.front_pylon_left_mass = front_pylon_mass
        self.front_pylon_right_mass = front_pylon_mass
        self.rear_pylon_mass = self.mass - 2 * front_pylon_mass

        # Calculation of position of mass center
        self.mass_center_y_position = front_pylons_y_position - (front_pylons_y_position - rear_pylon_y_position) * (
                    self.rear_pylon_mass / self.mass)
        print('the calculated mass center based of distribution:\nfront', front_pylons_mass_ratio, '\nrear: ',
              1 - front_pylons_mass_ratio)

        print(self.mass_center_y_position)

    def distribution_of_masses(self, mass_center_y_position, front_pylons_y_position, front_pylons_x_width,
                               rear_pylon_y_position):
        """
        Function that calculates the distribution of masses on pylons that are on given positions. The function
        Uses a simple geometric relationship:
        R3 = P * d12 / h3

        where:

        P is the load

        d12 is the distance of the load to the side 1-2

        h3 is the height of the triangle with respect to side 1-2.

        :param mass_center_y_position: position of mass center in 'y' axis [m]
        :param front_pylons_y_position: position of front pylons in 'y' axis
        :param front_pylons_x_width: distance between 'y' axis and front pylon
        :param rear_pylon_y_position: position of rear pylon in 'y' axis
        """

        self.mass_center_y_position = mass_center_y_position
        self.front_pylons_y_position = front_pylons_y_position
        self.front_pylons_x_width = front_pylons_x_width
        self.rear_pylon_y_position = rear_pylon_y_position

        # assert points
        rear_pylon_pos = Point(0.0, rear_pylon_y_position)
        front_pylon_right_pos = Point(front_pylons_x_width, front_pylons_y_position)
        front_pylon_left_pos = Point(-front_pylons_x_width, front_pylons_y_position)
        mass_center_pos = Point(0.0, self.mass_center_y_position)

        # calculate for rear pylon
        line_2_3 = LineString([front_pylon_right_pos, front_pylon_left_pos])
        d_2_3 = mass_center_pos.distance(line_2_3)
        h_2_3 = rear_pylon_pos.distance(line_2_3)
        self.rear_pylon_mass = self.mass * (d_2_3 / h_2_3)

        # calculate for front right pylon
        line_3_1 = LineString([front_pylon_left_pos, rear_pylon_pos])
        d_3_1 = mass_center_pos.distance(line_3_1)
        h_3_1 = front_pylon_right_pos.distance(line_3_1)
        self.front_pylon_right_mass = self.mass * (d_3_1 / h_3_1)

        # calculate for front left pylon
        line_1_2 = LineString([rear_pylon_pos, front_pylon_right_pos])
        d_1_2 = mass_center_pos.distance(line_1_2)
        h_1_2 = front_pylon_left_pos.distance(line_1_2)
        self.front_pylon_left_mass = self.mass * (d_1_2 / h_1_2)

        # Create and return the dictionary of mass distribution
        mass_distribution = {
            "rear_pylon_mass": self.rear_pylon_mass,
            "front_pylon_right_mass": self.front_pylon_right_mass,
            "front_pylon_left_mass": self.front_pylon_left_mass
        }
        print(mass_distribution)
