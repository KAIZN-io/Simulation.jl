from values import SimulationTypes
from db.initialData.ModelData import ModelData, ParameterData as P, InitialValueData as I


volumeData = ModelData(
    type = SimulationTypes.volume,
    parameters = [
        P('d', 0.115,'um','cell wall thickness'),
        P('phi', 1e-4,'Pa^{-1} s^{-1}', 'cell wall extensibility; fitted Altenburg 2018'),
        P('pi_c', 2e5, 'Pa', 'critical turgor pressure'),
        P('Lp', 1.19e-6, 'um s^{-1} Pa^{-1}', 'hydraulic conductivity'),
        P('nu', 0.5, 'dimensionless', 'Poissons ratio'),
        P('k_uptake', 2e-16, 'mmol s^{-1} um^{-2}'),
        P('k_consumption', 2.5e-16, 'mmol s^{-1} um^{-3}'),
        P('E_3D', 2.58e6, 'Pa', 'measured Youngs modulus; Goldenbogen & Giese et al. 2016'),
        P('c_e', 240, 'mM'),
        P('pi_e', 604594.08, 'mM'),
        P('modulus_adjustment', '(1 - nu ** 2) ** (-1)', 'dimensionless'),
        # P('E', 3440000.0,'Pa'),
        P('E', 'modulus_adjustment * E_3D', '', 'adjusted to 2D Young\'s modulus (surface)'),

        P('T', 303.15, 'K'),
        P('R', 8.314, 'J K^-1 mol^-1'),
        P('F', 96485, 'C mol^-1'),

    ],
    initialValues = [
        I('r_os' , 1.18773900649, 'um'),
        I('r_b' , 0.496161324363, 'um'),
        I('r' , 1.68390033085, 'um'),
        I('pi_t' , 2e5, 'Pa','turgor pressure'),
        I('R_ref' , 1.36108685239, 'um'),
        I('c_i' , 6.38904517734e-12, 'mmol','internal concentration of osmolytes'),
    ]
)

