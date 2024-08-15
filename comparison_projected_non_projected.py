from matplotlib import pyplot as plt
from src.foils_data.FoilManager import FoilManager
from src.foils_data.FoilPlotter import FoilPlotter, compare_foils_lift, compare_foils_drag
from src.utilities.Constants import *

NACA6409_CFD_path_bad = 'data_CFD/CFD_3D_skrzydla_przednie2023_batmanowe_NACA6409_Wyniki.csv'
NACA6409_CFD_path_good = 'data_CFD/CFD_3D_skrzydla_przednie2023_batmanowe_NACA6409_Wyniki_p.csv'
NACA6409_AFT_path = 'data_AFT/xf-n6409-il-1000000-n5.csv'

data_manager_NACA6409_CFD_bad = FoilManager('CFD', 'NACA 6409 BAD', NACA6409_CFD_path_bad, NACA6409_TOTAL_LENGTH,
                                            NACA6409_CHORD_LENGTH, NACA6409_AREA)
data_manager_NACA6409_CFD_bad.load_data()
data_manager_NACA6409_CFD_bad.clean_data()
data_manager_NACA6409_CFD_bad.multiply_forces_by_2_CFD()
data_manager_NACA6409_CFD_bad.calculate_lift_coefficient(WATER_DENSITY)
data_manager_NACA6409_CFD_bad.calculate_drag_coefficient(WATER_DENSITY)
data_manager_NACA6409_CFD_bad.calculate_cl_cd()

data_manager_NACA6409_CFD_good = FoilManager('CFD', 'NACA 6409 GOOD', NACA6409_CFD_path_good, NACA6409_TOTAL_LENGTH,
                                             NACA6409_CHORD_LENGTH, NACA6409_AREA)
data_manager_NACA6409_CFD_good.load_data()
data_manager_NACA6409_CFD_good.clean_data()
data_manager_NACA6409_CFD_good.multiply_forces_by_2_CFD()
data_manager_NACA6409_CFD_good.calculate_lift_coefficient(WATER_DENSITY)
data_manager_NACA6409_CFD_good.calculate_drag_coefficient(WATER_DENSITY)
data_manager_NACA6409_CFD_good.calculate_cl_cd()


plotter_NACA6409_CFD_bad = FoilPlotter(data_manager_NACA6409_CFD_bad)
plotter_NACA6409_CFD_good = FoilPlotter(data_manager_NACA6409_CFD_good)

compare_foils_lift(plotter_NACA6409_CFD_bad, plotter_NACA6409_CFD_good)
compare_foils_drag(plotter_NACA6409_CFD_bad, plotter_NACA6409_CFD_good)
