class AFT_DataProcessingMixin:
    def calculate_lift(self, density):
        """
        Function to calculate the lift in an analytic way.

        Formula:

        Lift = (1/2) * density * (velocity ^ 2) * Area * Lift_Coefficient
        """

        self.data['lift_force'] = (1 / 2) * density * pow(self.data['inlet_vel'], 2) * self.m2_foil_area * self.data['lift_coefficient']

    def calculate_drag(self, density):
        """
        Function to calculate the drag in an analytic way.

        Formula:

        Drag = (1/2) * density * (velocity ^ 2) * Area * Drag_Coefficient
        """

        self.data['drag_force'] = (1 / 2) * density * pow(self.data['inlet_vel'], 2) * self.m2_foil_area * self.data['drag_coefficient']
