from pathlib import Path

from src.foils_data.FoilPlotter import FoilPlotter
from src.utilities.Constants import *

from src.foils_data.FoilManager import FoilManager


def foil_manager_procedure(data_type, name, path, area):
    data_manager = FoilManager(data_type, name, path, 0, 0, area)

    data_manager.load_data()
    data_manager.clean_data()
    data_manager.multiply_forces_by_2_CFD()
    data_manager.calculate_lift_coefficient(WATER_DENSITY)
    data_manager.calculate_drag_coefficient(WATER_DENSITY)
    data_manager.calculate_cl_cd()

    return data_manager


script_dir = Path(__file__).resolve().parent
WINGLET_2_HMIN_FIMAX_path = script_dir / '..' / '..' / 'data_winglets' / 'SKRYPT_Winglet_2_hmin_fimax.csv'
WINGLET_3_HMIN_FIMIN_path = script_dir / '..' / '..' / 'data_winglets' / 'SKRYPT_Winglet_3_hmin_fimin.csv'
WINGLET_4_HMAX_FIMIN_path = script_dir / '..' / '..' / 'data_winglets' / 'SKRYPT_Winglet_4_hmax_fimin.csv'
WINGLET_5_HSR_FISR_path = script_dir / '..' / '..' / 'data_winglets' / 'SKRYPT_winglet_5_hsr_fisr.csv'
NACA6409_PROSTOKATNE_path = script_dir / '..' / '..' / 'data_winglets' / 'SKRYPT_naca6409_prostokatne.csv'
NACA6409_WINGLET_path = script_dir / '..' / '..' / 'data_winglets' / 'SKRYPT_naca6409_winglet.csv'
NACA6409_CFD_path = script_dir / '..' / '..' / 'data_CFD' / 'CFD_3D_skrzydla_przednie2023_batmanowe_NACA6409_Wyniki.csv'

data_WINGLET_2 = foil_manager_procedure('CFD', 'WINGLET 2', WINGLET_2_HMIN_FIMAX_path, WINGLET_2_AREA)

data_WINGLET_3 = foil_manager_procedure('CFD', 'WINGLET 3', WINGLET_3_HMIN_FIMIN_path, WINGLET_3_AREA)

data_WINGLET_4 = foil_manager_procedure('CFD', 'WINGLET 4', WINGLET_4_HMAX_FIMIN_path, WINGLET_4_AREA)

data_WINGLET_5 = foil_manager_procedure('CFD', 'WINGLET 5', WINGLET_5_HSR_FISR_path, WINGLET_5_AREA)

data_NACA6409_PROST = foil_manager_procedure('CFD', 'NACA6409 PROST', NACA6409_PROSTOKATNE_path, NACA6409_PROST_AREA)

data_NACA6409_WING = foil_manager_procedure('CFD', 'NACA6409 WING', NACA6409_WINGLET_path, NACA6409_WING_AREA)

data_NACA6409_BAT = foil_manager_procedure('CFD', 'NACA6409 BAT', NACA6409_CFD_path, NACA6409_AREA)

plotter_WINGLET_2 = FoilPlotter(data_WINGLET_2)
plotter_WINGLET_3 = FoilPlotter(data_WINGLET_3)
plotter_WINGLET_4 = FoilPlotter(data_WINGLET_4)
plotter_WINGLET_5 = FoilPlotter(data_WINGLET_5)
plotter_NACA6409_PROST = FoilPlotter(data_NACA6409_PROST)
plotter_NACA6409_WING = FoilPlotter(data_NACA6409_WING)
plotter_NACA6409_BAT = FoilPlotter(data_NACA6409_BAT)

#plotter_WINGLET_2.plot_cl_cd_at_target_velocities({6, 7, 8})
#plotter_WINGLET_2.plot_lift_coefficient_at_target_velocity_compare_foils(8, data_WINGLET_3)
# plotter_WINGLET_2.plot_cl_cd_at_target_velocity_compare_foils(8, data_WINGLET_3, data_WINGLET_4, data_WINGLET_5,data_NACA6409_WING,data_NACA6409_PROST,data_NACA6409_BAT)
#plotter_WINGLET_2.plot_drag_coefficient_at_target_velocity_compare_foils(8, data_WINGLET_3)
#plotter_NACA6409_PROST.plot_cl_cd_at_target_velocity_compare_foils(8, data_NACA6409_WING)
#plotter_NACA6409_PROST.plot_drag_force_target_velocity_compare_foils(8,data_NACA6409_WING)
#plotter_NACA6409_PROST.plot_lift_vs_angle_compare_foils(8,data_NACA6409_WING)

plotter_NACA6409_WING.plot_lift_coefficient_at_target_velocity_compare_foils(8, data_NACA6409_PROST)
plotter_NACA6409_WING.plot_drag_coefficient_at_target_velocity_compare_foils(8, data_NACA6409_PROST)
