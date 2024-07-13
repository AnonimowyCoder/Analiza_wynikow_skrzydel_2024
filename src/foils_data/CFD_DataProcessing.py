class CFD_DataProcessingMixin:
    def calculate_lift_coefficient(self, density):
        """
        Calculate the lift coefficient using lift force.

        Formula:

        lift_coefficient = (2 * lift_force) / (density * velocity^2 * area)
        """
        self.data['lift_coefficient'] = (2 * self.data['lift_force']) / (
                density * pow(self.data['inlet_vel'], 2) * self.m2_foil_area)

    def calculate_drag_coefficient(self, density):
        """
        Calculate the drag coefficient using drag force.

        Formula:

        drag_coefficient = (2 * drag_force) / (density * velocity^2 * area)
        """
        self.data['drag_coefficient'] = (2 * self.data['drag_force']) / (
                density * pow(self.data['inlet_vel'], 2) * self.m2_foil_area)

    def calculate_cl_cd(self):
        """
        Calculate lift coefficient vs drag coefficient (effectivness of foil).

        Formula:

        cl_cd = cl / cd
        """
        self.data['cl_cd'] = self.data['lift_coefficient'] / self.data['drag_coefficient']
