exec(open("SYSTEM/py_packages.py").read())


def new_ODE_solver(t, init):

    # get the starting values for the ODEs
    for i in range(len(init)):
        exec('{}={}'.format(simulation_frame.columns.tolist()[i],init[i]))

    # get the data for the system from the json file
    with open('{0}/Single_Models/json_files/{1}_system.json'.format(cwd, model_name)) as json_data:
        data_from_json = json.load(json_data)

    t_ODE = ()
    t_ODE_comp = ()
    for key,value_system in data_from_json.items():
        if key == 'copa':
            for key2, value2 in value_system.items():
                exec('{}={}'.format(key2,value2))

        else:
            for keys,value in value_system.items():
                if 'condition' in value:
                    for key2,value2 in value['component'].items():
                        exec('{}={} {}'.format(key2,value2,value['condition']))
                        t_ODE_comp = t_ODE_comp + (key2,)
                else:
                    # print(value)
                    for key2,value2 in value['component'].items():
                        exec('{}={}'.format(key2,value2))
                        t_ODE_comp = t_ODE_comp + (key2,)

                list_values = list(value['component'].keys())
                a = '+'.join(list_values)

                # print(keys, " = ", a)
                if key == 'ODE':
                    t_ODE = t_ODE + (keys,)

                exec('{}={}'.format(keys,a))

    # sort the t_ODE:
    # NOTE: this must be done because the json file is not sorted!
    t_ODE = sorted(t_ODE)

    # eval the results
    t_tuple = ()
    t_tuple_comp = ()

    for i in t_ODE:
        t_tuple = t_tuple + (eval(i),)

    # has the data from the components
    for i in t_ODE_comp:
        t_tuple_comp = t_tuple_comp + (eval(i),)

    if dict_system_switch.get('export_data_to_sql') == True:
        # sql connection
        engine = create_engine('postgres://janpiotraschke:@localhost:5432/simulation_results', echo=False)

        df_dict_term = {}
        for i in t_ODE_comp:
            df_dict_term[i] = eval(i)

        df = pd.DataFrame(df_dict_term, index=[t])

        df.to_sql(csv_fingerprint, con=engine, schema='{}_terms'.format(model_name), if_exists='append')
    print(t)
    return t_tuple


cwd = os.getcwd()
model_name = 'combined_models'

dict_system_switch = {
                    # TEMP: only works for model with stimuli !!!
                    # IDEA: fuers datenbankmanagmentsystem (DBMS)
                    'fetch_data_from_sql' : False,
                    'export_data_to_sql' : False,
                    'create_csv' : False,
                    # show_DataFrame = [boolen, head, tail]
                    'show_DataFrame' : [False, 2, 0],
                     }

dict_time = {
            'start' : 0,
            'stop' : 100,  # 7200 = 2 h (mehr braucht Yeast nicht)
            'time_steps' : 0.1,
            'NaCl_impuls_start' : 10,
            'Glucose_impuls_start' : 60,
            'Glucose_impuls_end' : 72,
            'KCL_unique_impuls_start' : 30,
            'Sorbitol_stimulus_start' : 30,
            }

for key,value in dict_time.items():
    exec(key + '=value')

combined_models_parameter = {
                'T' : [303.15, 'K'],
                'R' : [8.314, 'J K^-1 mol^-1'],
                'F' : [96485, 'C mol^-1'],

                'k_phoPbs2' : [39.22 /60, 's^-1'],
                'k_dephoPbs2' : [ 13.44 /60,'s^-1'],
                'k_phoHog1' : [11.2 * 1e3 /60 ,'mM^-1 s^-1'],

                'k_dephoHog1PPn' : [ 4.144 /60 ,'s^-1'],
                'k_dephoHog1PPc' : [0.09061/60 ,'s^-1'],
                'k_impHog1PPc' : [1.195/60 ,'s^-1'],
                'k_s0Glyc' : [ 5248 * 1e-3/60,'mM s^-1'],
                'k_s1Glyc' : [ 56140 * 1e-3/60,'mM s^-1'],
                'k_s2Glyc' : [1139/60 ,'s^-1'],
                'k_tYt' : [ 0.008934 /60,'s^-1'],
                'k_impHog1c' : [ 0.7528 /60,'s^-1'],
                'k_expHog1PPn' : [7.076 /60 ,'s^-1'],
                'k_exp0Glyc' : [0.005/60 ,'s^-1'],
                'k_s0Yt' : [0.01211 * 1e-3 /60 ,'mM s^-1'],
                'k_exp1Glyc' : [0.02963 /60 ,'s^-1'],
                'k_s1Yt' : [1.204 /60 ,'s^-1'],
                'k_expHog1n' : [6.36/60 ,'s^-1'],
                'PI_t0' : [ 0.875 * 1e6,'Pa', 'turgor pressure/unstressed'],
                'PI_i0' : [ 1.5 * 1e6,'Pa', 'internal osmotic pressure/unstressed'],
                'PI_e0' : [0.625 * 1e6 ,'Pa', 'external osmotic pressure/unstressed'],
                'Glyc_ex' : [0 ,'mM', 'eine Konstante hier'],

                # NOTE: G is now an algebraic equation
                #'G' : [72.4607 ,'um^2'],
                'w' : [ 4688,'J m^-3 mM^-1'],
                'Lp' : [0.2497 / 60 * 1e-6 ,'um Pa^-1 s^-1'],
                'f_V_cyt' : [0.5 ,'dimensionless'],
                'n_Hog1_total' : [6780 ,'xxx', 'total number of Hog1'],
                'V_osPIt' : [30.63 ,'fL'],
                'V_os0' : [34.8 ,'fL', 'volume before osmotic change'],
                'V_b' : [ 23.2,'fL','fixed part of the cell volume'],
                'alpha' : [0.18 * 1e6 ,'Pa'],   #orginal: [0.398 * 1e6 ,'Pa']
                'beta' : [ 0.6,'dimensionless'],  #original: [ 0.2992,'dimensionless']
                'gamma' : [0.18 *1e6 ,'Pa'], #original: [0.9626 *1e6 ,'Pa']
                'tau' : [20 * 60 ,'s'],
                'n_0' : [4.176 * 1e3 ,'mmol'],
                'hill_exponent' : [8,'dimensionless'],
                'hill_exponent_eflux' : [12,'dimensionless'],

                # from volume model
                'd' : [0.115,'um','cell wall thickness'],
                'phi' : [1e-4,'Pa^{-1} s^{-1}', 'cell wall extensibility', 'fitted Altenburg 2018'],
                'pi_c' : [2e5, 'Pa', 'critical turgor pressure'],
                # 'Lp' : [1.19e-6, 'um^{-1} s^{-1} Pa^{-1}', 'hydraulic conductivity'],   # NOTE: Lp schon oben notiert
                'nu' : [0.5, 'dimensionless', 'Poissons ratio'],
                'k_uptake' : [2e-16, 'mmol s^{-1} um^{-2}'],
                'k_consumption' : [2.5e-16, 'mmol s^{-1} um^{-3}'],
                'E_3D' : [2.58e6, 'Pa', 'measured Youngs modulus', 'Goldenbogen & Giese et al. 2016'],

                # from ion model
                'ATP_stimulus' : [2.5, 'mM'],

                #'V_out' : [2.85e-6,'m^3'],

                # umgerechnetes Volumen für kombiniertes Hog Model
                #'V_out' : [2.85 * 1e12,'fL'],
                # neu definierte externe Umgebung--> Experiment naeher
                'V_out' : [28.95 * 1e3, 'fL'],

                #'Surf' : [2.29e-5, 'm^2'],
                'pbc' : [200,'mM pH^-1'],
                'C_m' : [1e-2, 'xxxxxxx'],
                'c_strich_ATP' : [0.316, 'mM'],
                'K_eq' : [1e-6, 'dimensionless'],

                # TODO: change the unit of L_XX
                'L_HHaG' : [0.0019  , 'mol^2 J^-1 m^-2 s^-1'],
                'L_ArHaG' : [-0.00195 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_HNa' : [-6.31 * 1e-15 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_NaH' : [-6.31 * 1e-15 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_KK' : [6.37 * 1e-11 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_HCl' : [1.298 * 1e-9 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_ClH' : [1.298 * 1e-9 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_NaNa' : [3.03 * 1e-15 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_ClCl' : [1.04 * 1e-9 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_HK' : [-2.072097044 * 1e-16 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_KH' : [-2.072097044 * 1e-16 , 'mol^2 J^-1 m^-2 s^-1'],

                #'L_HHaG' : [0.0019, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_ArHaG' : [-0.00195, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_HNa' : [-6.31 * 1e-15, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_NaH' : [-6.31 * 1e-15, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_KK' : [6.37 * 1e-11, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_HCl' : [1.298 * 1e-9, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_ClH' : [1.298 * 1e-9, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_NaNa' : [3.03 * 1e-15, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_ClCl' : [1.04 * 1e-9, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_HK' : [-2.072097044 * 1e-16, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_KH' : [-2.072097044 * 1e-16, 'mol^2 J^-1 m^-2 s^-1'],
                #####
                'k_incrHH' : [3.54 * 1e-9, 'mol^2 J^-1 m^-2 s^-2'],
                'k_incrArH' : [-3.64 * 1e-9, 'mol^2 J^-1 m^-2 s^-2'],
                'k_ATPincr' : [10, 'mol m^-3 s^-1'],

                'c_ext_extra' : [0,'mM']
                }

for key,value in combined_models_parameter.items():
    exec(key + '=value[0]')

modulus_adjustment = (1 - nu ** 2) ** (-1)  # dimensionless
E = modulus_adjustment * E_3D  # adjusted to 2D Young's modulus (surface)

k_ATPdecr = k_ATPincr / ATP_stimulus
k_decrArH =  k_incrArH / L_ArHaG
k_decrHH = k_incrHH / L_HHaG

# NOTE: es war ein Parameter zu viel definiert --> Lp

t_span = [0,100]
y = [2.477, 0.545, 112.60000000000001, -0.168, 57.6, 0.003063, 3.560412, 4.443e-06, 3.3800000000000002e-06, 0.00034260000000000003, 0.0002918, 75.54, 112.60000000000001, 0.0, 1.6200000000000002e-09, 29.98, 11.26, 0.0001231, 6.16e-07, 1.783877, 0.001811, 163.66806300000002, 200000.0, 2.4, 0.580719, 1.819281, 3.3800000000000002e-06, 3.3800000000000002e-06, 3.3800000000000002e-06, 3.3800000000000002e-06]
columns_order = ['ATP', 'Cl_in', 'Cl_out', 'Deltaphi', 'Glyc_in', 'H_in', 'H_out', 'Hog1PPc', 'Hog1PPn', 'Hog1c', 'Hog1n', 'K_in', 'K_out', 'L_ArH', 'L_HH', 'Na_in', 'Na_out', 'Pbs2', 'Pbs2PP', 'R_ref', 'Yt', 'c_i', 'pi_t', 'r', 'r_b', 'r_os', 'z1', 'z2', 'z3', 'z4']

df_dict = {}
for i in range(len(columns_order)):
    df_dict[columns_order[i]] = y[i]
simulation_frame = pd.DataFrame(df_dict, index=[1])
init = y

# NOTE: im dataframe sind die richtigen Variablen - init. Werte Zuweisungen!
# NOTE: kontrolliert am 25 Oktober 2018
# for i in range(len(init)):
#     print('{}={}'.format(simulation_frame.columns.tolist()[i],init[i]))

# t_span : 2-tuple of floats; Interval of integration (t0, tf)
# y0 : array_like, shape (n,)
switch = [False]
# NOTE: egal ob RK45 oder LSODA --> das Ergebnis ist das selbe ....
states = solve_ivp(new_ODE_solver, t_span=t_span, y0=y, method='RK45')
matrix = (states.y).transpose()
working_frame = pd.DataFrame(matrix, columns=columns_order, index=states.t)
# plt.plot(working_frame['Deltaphi'])
# plt.show()
