from values import SimulationTypes
from db.initialData.ModelData import ModelData, ParameterData as P, InitialValueData as I


ionData = ModelData(
    type = SimulationTypes.ion,
    parameters = [
        P('ATP_stimulus', 2.5, 'mM'),

        # NOTE: original ion parameter values
        P('V_out', 2.85e-6,'m^3'),
        P('V_in', 1.8 * 1e-11,'m^3'),
        P('Surf', 2.29e-5, 'm^2'),

        P('pbc', 200,'mM pH^-1'),
        P('C_m', 1e-2, 'xxxxxxx'),
        P('c_strich_ATP', 0.316, 'mM'),
        P('K_eq', 1e-6, 'dimensionless'),

        P('L_HHaG', 0.0019 , 'mol^2 J^-1 m^-2 s^-1'),
        P('L_ArHaG', -0.00195, 'mol^2 J^-1 m^-2 s^-1'),
        P('L_HNa', -6.31 * 1e-15, 'mol^2 J^-1 m^-2 s^-1'),
        P('L_NaH', -6.31 * 1e-15, 'mol^2 J^-1 m^-2 s^-1'),
        P('L_KK', 6.37 * 1e-11, 'mol^2 J^-1 m^-2 s^-1'),
        P('L_HCl', 1.298 * 1e-9, 'mol^2 J^-1 m^-2 s^-1'),
        P('L_ClH', 1.298 * 1e-9, 'mol^2 J^-1 m^-2 s^-1'),
        P('L_NaNa', 3.03 * 1e-15, 'mol^2 J^-1 m^-2 s^-1'),
        P('L_ClCl', 1.04 * 1e-9, 'mol^2 J^-1 m^-2 s^-1'),
        P('L_HK', -2.072097044 * 1e-16, 'mol^2 J^-1 m^-2 s^-1'),
        P('L_KH', -2.072097044 * 1e-16, 'mol^2 J^-1 m^-2 s^-1'),

        P('k_incrHH', 3.54 * 1e-9, 'mol^2 J^-1 m^-2 s^-2'),
        P('k_incrArH', -3.64 * 1e-9, 'mol^2 J^-1 m^-2 s^-2'),
        P('k_ATPincr', 10, 'mol m^-3 s^-1'),
        P('k_ATPdecr', 4.0, ''),
        P('k_decrArH', 1.8666666666666669e-06, ''),
        P('k_decrHH', 1.8631578947368422e-06, ''),

        P('T', 303.15, 'K'),
        P('R', 8.314, 'J K^-1 mol^-1'),
        P('F', 96485, 'C mol^-1'),
    ],
    initialValues = [
        I('H_in' , 3.063e-3  , 'mM','original/ion_model'),
        I('K_in' , 75.54 , 'mM','original/ion_model'),
        I('Cl_in' , 0.545 , 'mM','original/ion_model'),
        I('Na_in' , 29.98 , 'mM','original/ion_model'),

        # NOTE: Werte vom originalen Ion-Modell
        I('H_out' , 3.162e-3, 'mM'),
        I('K_out' , 0.1, 'mM'),
        I('Cl_out' , 0.1, 'mM'),
        I('Na_out' , 0.01, 'mM'),

        ######
        I('ATP' , 2.477, 'mM'),
        I('Deltaphi' , -0.168, 'V'),

        # changeable coefficients, init for time = 0 min
        I('L_ArH', 0, '... s^-1'),
        I('L_HH', 1.62 * 1e-9, '... s^-1')
    ]
)

