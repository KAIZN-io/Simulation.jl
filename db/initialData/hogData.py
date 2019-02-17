from values import SimulationTypes
from db.initialData.ModelData import ModelData, ParameterData as P, InitialValueData as I


hogData = ModelData(
    type = SimulationTypes.hog,
    parameters = [
        P('k_phoPbs2', 39.22 /60, 's^-1'),
        P('k_dephoPbs2',  13.44 /60,'s^-1'),
        P('k_phoHog1', 11.2 * 1e3 /60 ,'mM^-1 s^-1'),

        P('k_dephoHog1PPn',  4.144 /60 ,'s^-1'),
        P('k_dephoHog1PPc', 0.09061/60 ,'s^-1'),
        P('k_impHog1PPc', 1.195/60 ,'s^-1'),
        P('k_s0Glyc',  5248 * 1e-3/60,'mM s^-1'),
        P('k_s1Glyc',  56140 * 1e-3/60,'mM s^-1'),
        P('k_s2Glyc', 1139/60 ,'s^-1'),
        P('k_tYt',  0.008934 /60,'s^-1'),
        P('k_impHog1c',  0.7528 /60,'s^-1'),
        P('k_expHog1PPn', 7.076 /60 ,'s^-1'),
        P('k_exp0Glyc', 0.005/60 ,'s^-1'),
        P('k_s0Yt', 0.01211 * 1e-3 /60 ,'mM s^-1'),
        P('k_exp1Glyc', 0.02963 /60 ,'s^-1'),
        P('k_s1Yt', 1.204 /60 ,'s^-1'),
        P('k_expHog1n', 6.36/60 ,'s^-1'),
        P('PI_t0',  0.875 * 1e6,'Pa', 'turgor pressure/unstressed'),
        P('PI_i0',  1.5 * 1e6,'Pa', 'internal osmotic pressure/unstressed'),
        P('PI_e0', 0.625 * 1e6 ,'Pa', 'external osmotic pressure/unstressed'),
        P('Glyc_ex', 0 ,'mM', 'eine Konstante hier'),

        P('G', 72.4607 ,'um^2'),
        P('w',  4.688 * 1e-3 * 1e6,'J m^-3 mM^-1'),
        P('Lp', 0.2497 / 60 * 1e-6 ,'um Pa^-1 s^-1'),
        P('f_V_cyt', 0.5 ,'dimensionless'),
        P('n_Hog1_total', 6780 ,'xxx', 'total number of Hog1'),
        P('V_osPIt', 30.63 ,'fL'),
        P('V_os0', 34.8 ,'fL', 'volume before osmotic change'),
        P('V_b',  23.2,'fL','fixed part of the cell volume'),
        P('alpha', 0.398 * 1e6 ,'Pa'),
        P('beta',  0.2992,'dimensionless'),
        P('gamma', 0.9626 *1e6 ,'Pa'),
        P('tau', 20 * 60 ,'s'),
        P('n_0', 4.176 * 1e3 ,'mmol'),
        P('hill_exponent', 8,'dimensionless'),
        P('hill_exponent_eflux', 12, 'dimensionless'),
        P('max_NaCl', 2 * 1e3, 'mM'),

        P('T', 303.15, 'K'),
        P('R', 8.314, 'J K^-1 mol^-1'),
        P('F', 96485, 'C mol^-1'),
    ],
    initialValues = [
        I('Pbs2' , 0.1231 * 1e-3, 'mM', 'original/hog_model'),              # unphosphorylated Pbs2
        I('Pbs2PP' , 0.000616 * 1e-3, 'mM', 'original/hog_model'),            # phosphorylated Pbs2
        I('Hog1c' , 0.3426 * 1e-3, 'mM', 'original/hog_model'),            # unphosphorylated cytoplasmic Hog1
        I('Hog1PPc' , 0.004443 * 1e-3, 'mM', 'original/hog_model'),        # phosphorylated cytoplasmic Hog1
        I('Hog1n' , 0.2918 * 1e-3, 'mM', 'original/hog_model'),              # unphosphorylated nuclear Hog1
        I('Hog1PPn' , 0.00338 * 1e-3, 'mM', 'original/hog_model'),          # phosphorylated nuclear Hog1
        I('Glyc_in' , 57600 * 1e-3, 'mM', 'original/hog_model'),            # intracellular glycerol

        # Yt is the time delay for the expression of glycerol-producing proteins
        I('Yt' , 1.811 * 1e-3, 'mM', 'original/hog_model'),
        I('V_os' , 34.8, 'fL','original/hog_model'),

        # z = delay of transcriptional feedback on glycerol production
        I('z1' , 0.00338 * 1e-3, 'mM', 'original/hog_model'),
        I('z2' , 0.00338 * 1e-3, 'mM', 'original/hog_model'),
        I('z3' , 0.00338 * 1e-3, 'mM', 'original/hog_model'),
        I('z4' , 0.00338 * 1e-3, 'mM', 'original/hog_model'),
    ]
)

