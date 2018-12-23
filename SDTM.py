__author__ = 'Jan N. Piotraschke'
__email__ = 'jan.piotraschke@mail.de'
__version__ = 'bachelor_thesis'
__license__ = 'private'

"""import the standard used packages"""
exec(open("SYSTEM/py_packages.py").read())
from decimal import Decimal

class netzwerk_daten_gewinnung:
    def __init__(self):
        pass

    def ODE_solver(init, t):

        """get the starting values for the ODEs"""
        for i in range(len(init)):
            exec('{}={}'.format(simulation_frame.columns.tolist()[i],init[i]))

        """get the data for the system from the json file"""
        
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
                        for key2,value2 in value['component'].items():
                            exec('{}={}'.format(key2,value2))
                            t_ODE_comp = t_ODE_comp + (key2,)

                    list_values = list(value['component'].keys())
                    a = '+'.join(list_values)

                    if key == 'ODE':
                        t_ODE = t_ODE + (keys,)

                    exec('{}={}'.format(keys,a))

        """sort the t_ODE

        this must be done because the json file is not sorted!
        """
        t_ODE = sorted(t_ODE)

        """eval the results"""
        t_tuple = ()
        t_tuple_comp = ()

        for i in t_ODE:
            t_tuple = t_tuple + (eval(i),)

        """has the data from the components"""
        for i in t_ODE_comp:
            t_tuple_comp = t_tuple_comp + (eval(i),)


        """export the individuel terms to the database
        """
        if dict_system_switch.get('export_data_to_sql') == True\
        and dict_system_switch.get('export_terms_data_to_sql') == True:

            """sql connection"""
            engine = create_engine('postgres://janpiotraschke:@localhost:5432/simulation_results', echo=False)

            df_dict_term = {}
            for i in t_ODE_comp:
                df_dict_term[i] = eval(i)

            df = pd.DataFrame(df_dict_term, index=[t])

            df.to_sql(csv_fingerprint, con=engine, schema='{}_terms'.format(model_name), if_exists='append')

        return t_tuple

    # # TEMP: new ode solver version
    # def new_ODE_solver(t, init):
    #
    #     # get the starting values for the ODEs
    #     for i in range(len(init)):
    #         exec('{}={}'.format(simulation_frame.columns.tolist()[i],init[i]))
    #
    #     # get the data for the system from the json file
    #     with open('{0}/Single_Models/json_files/{1}_system.json'.format(cwd, model_name)) as json_data:
    #         data_from_json = json.load(json_data)
    #
    #     t_ODE = ()
    #     t_ODE_comp = ()
    #     for key,value_system in data_from_json.items():
    #         if key == 'copa':
    #             for key2, value2 in value_system.items():
    #                 exec('{}={}'.format(key2,value2))
    #
    #         else:
    #             for keys,value in value_system.items():
    #                 if 'condition' in value:
    #                     for key2,value2 in value['component'].items():
    #                         exec('{}={} {}'.format(key2,value2,value['condition']))
    #                         t_ODE_comp = t_ODE_comp + (key2,)
    #                 else:
    #                     # print(value)
    #                     for key2,value2 in value['component'].items():
    #                         exec('{}={}'.format(key2,value2))
    #                         t_ODE_comp = t_ODE_comp + (key2,)
    #
    #                 list_values = list(value['component'].keys())
    #                 a = '+'.join(list_values)
    #
    #                 # print(keys, " = ", a)
    #                 if key == 'ODE':
    #                     t_ODE = t_ODE + (keys,)
    #
    #                 exec('{}={}'.format(keys,a))
    #
    #     # sort the t_ODE:
    #     # NOTE: this must be done because the json file is not sorted!
    #     t_ODE = sorted(t_ODE)
    #
    #     # eval the results
    #     t_tuple = ()
    #     t_tuple_comp = ()
    #
    #     for i in t_ODE:
    #         t_tuple = t_tuple + (eval(i),)
    #
    #     # has the data from the components
    #     for i in t_ODE_comp:
    #         t_tuple_comp = t_tuple_comp + (eval(i),)
    #
    #     # if dict_system_switch.get('export_data_to_sql') == True:
    #     #     # sql connection
    #     #     engine = create_engine('postgres://janpiotraschke:@localhost:5432/simulation_results', echo=False)
    #     #
    #     #     df_dict_term = {}
    #     #     for i in t_ODE_comp:
    #     #         df_dict_term[i] = eval(i)
    #     #
    #     #     df = pd.DataFrame(df_dict_term, index=[t])
    #     #
    #     #     df.to_sql(csv_fingerprint, con=engine, schema='{}_terms'.format(model_name), if_exists='append')
    #     #
    #     return t_tuple


    def simulation(DataForSimulation=pd.DataFrame(), i=[]):
        init_cond_from_frame = DataForSimulation.tail(1).values.tolist()[0]

        """solves the ode and algebraic equations"""
        states = odeint(x.ODE_solver, init_cond_from_frame, i)

        # NOTE: test bereich anfang

        # t_span = [i[0],i[-1]]
        #
        # """ solve_ivp parameter
        #
        # t_span : 2-tuple of floats; Interval of integration (t0, tf)
        # y0 : array_like, shape (n,)
        # """
        # states = solve_ivp(x.new_ODE_solver,
        #                     t_span=t_span,
        #                     y0=init_cond_from_frame,
        #                     method='RK45')
        # matrix = (states.y).transpose()

        # NOTE: test bereich ende

        """ruft die entsprechenden Columns Namen auf"""
        columns_order = DataForSimulation.columns.values.tolist()

        """uebergibt dem working_frame die Ergebnisse der Berechnung"""
        working_frame = pd.DataFrame(states, columns=columns_order, index=i)
        # working_frame = pd.DataFrame(matrix,
        #                             columns=columns_order,
        #                             index=states.t)

        """haengt das working_frame dem simulation_frame an"""
        simulation_frame = pd.concat([DataForSimulation, working_frame])

        return simulation_frame


if __name__ == "__main__":

    """momentanes arbeitsverzeichnis = cwd"""
    cwd = os.getcwd()
    #erschafft einen Ordner namens "Pictures"
    #os.mkdir('csv_datafiles/volume')

    #os.mkdir('Simulation_Data')

    x = netzwerk_daten_gewinnung

    STUDYID = 'Yeast_BSc'
    EXCAT = 'Salz'

    """only one model each time as True"""
    dict_model_switch = {
                        'combined_models': True,
                        'dummie': False,
                        'hog': False,
                        'ion': False,
                        'volume': False,
                         }

    dict_time = {
                'start' : 0,
                'stop' : 600,  
                'time_steps' : 0.1,
                'NaCl_impuls_start' : 10,
                'Glucose_impuls_start' : 60,
                'Glucose_impuls_end' : 72,
                'KCL_unique_impuls_start' : 30,
                }

    """make the dict keys as new variables"""
    locals().update(dict_time)

    """Stimulus = [time] in s"""
    dict_unique_EXSTDTC = {                                
                                'KCl' : [30],
                                'NaCl' : [30],
                                'Sorbitol' : [30],
                            }

    """implementation rules

    Stimulus = [[value(s)], unit, [target(s)], boolean]
    """
    """only for the hog model

    signal_type :
        2: single pulse of NaCl
        3: square pulses of NaCl
        4: up-staircase change of NaCl
    """
    dict_stimulus = {
                    'KCl' : [[100], 'mM', ['K_out','Cl_out'], True],
                    'NaCl': [[100, 200], 'mM', ['Na_out', 'Cl_out'], False],
                    'Sorbitol': [[100, 200, 400, 800, 1600], 'mM', ['Sorbitol_out'], False],

                    'NaCl_impuls' : [200, 'mM'],
                    'signal_type' : [3],
                    }


    """database management system"""
    # NOTE : SpecificInitValuesVersionSEQ = 4 for combined_models
    dict_system_switch = {
                        'export_data_to_sql' : False,
                        'export_terms_data_to_sql' : False,
                        'SpecificInitValuesVersionSEQ' : [4],
                        'SpecificModelVersionSEQ' : []
                         }

    """get the right pipelines for the choosen model simulation"""
    conn = psycopg2.connect(host='localhost', dbname='simulation_results')
    
    """open a cursor to perform database operations"""
    cur = conn.cursor()


    """activated stimuli

    find out which stimulus pipeline is opened for the experiment series
    """
    activated_stimuli = [stimulus_name for stimulus_name, items
                        in dict_stimulus.items() if items[-1] == True]


    """ affected models

    find out the from stimuli affected models
    """
    models_ext_stimulus = []
    list_of_model_names = []

    for NameOfModel, boolean in dict_model_switch.items():
        if boolean == True:
            list_of_model_names.append(NameOfModel)

            """gets the wanted ModelVersion"""
            if len(dict_system_switch.get('SpecificModelVersionSEQ')) > 0:
                SpecificModelVersionSEQ = dict_system_switch.get(
                    'SpecificModelVersionSEQ')[0]
            else:
                """get the MAX(seq) value from the database"""
                cur.execute(sql.SQL("""
                    SELECT MAX(seq)
                    FROM {}.json;
                    """).format(sql.Identifier(NameOfModel)))

                SpecificModelVersionSEQ = cur.fetchone()[0]

            """gets the wanted InitValuesVersion"""
            if len(dict_system_switch.get('SpecificInitValuesVersionSEQ')) > 0:
                SpecificInitValuesVersionSEQ = dict_system_switch.get(
                    'SpecificInitValuesVersionSEQ')[0]

            else:
                """get the MAX(seq) value from the database"""
                cur.execute(sql.SQL("""
                    SELECT MAX(seq)
                    FROM {}.init_values;
                    """).format(sql.Identifier(NameOfModel)))

                SpecificInitValuesVersionSEQ = cur.fetchone()[0]
            

            if NameOfModel != 'hog':
                """update the local safed json file for the model"""
                cur.execute(sql.SQL("""
                    SELECT model_version
                    FROM {}.json
                    WHERE seq = %s;
                    """).format(sql.Identifier(NameOfModel)), [SpecificModelVersionSEQ])

                ModelVersionFromDatabase = cur.fetchone()[0]

                """create json format"""

                s = json.dumps(ModelVersionFromDatabase, indent=4)
                with open('Single_Models/json_files/{0}_system.json'.format(NameOfModel), "w") as f:
                    f.write(s)

                """query the available ODE components"""
                cur.execute(sql.SQL("""
                    SELECT testcd
                    FROM {}.init_values
                    WHERE seq = %s
                    """).format(sql.Identifier(NameOfModel)), [SpecificInitValuesVersionSEQ])

                ModelOdeVariable = cur.fetchall()
                ModelOdeVariable = [x[0] for x in ModelOdeVariable]

            else:
                exec(open('Single_Models/{0}/{0}.py'.format(NameOfModel),encoding="utf-8").read())

                """list of the names of the variables in the model"""
                ModelOdeVariable = eval(
                    '{}_init_values'.format(NameOfModel)).keys()

            """iterating over all activated stimuli"""
            for i in activated_stimuli:

                """get me the target of the specific stimuli"""
                target = dict_stimulus.get(i)[2]

                """if the targets are in the specific model"""
                if set(target).issubset(ModelOdeVariable) == True:
                    models_ext_stimulus.append('{}'.format(NameOfModel))

    """deletes multiple listings"""

    models_ext_stimulus = list(set(models_ext_stimulus))

    """preparation for simulation"""
    list_of_stimuli_conc = []
    list_of_stimuli_name = []
    dict_of_EXSTDTC = {}

    for key,values in dict_stimulus.items():
        if values[-1] == True:
            list_of_stimuli_conc.append(values[0])
            list_of_stimuli_name.append(key)

            """find the right stimuli-simulation-time-list for this impuls
            
            creates a sub dict of the possible stimilus
            """
            if key in dict_unique_EXSTDTC.keys():

                dict_of_EXSTDTC[key] = dict_unique_EXSTDTC[key]

    dict_stimuli = dict(zip(list_of_stimuli_name, list_of_stimuli_conc))
   
    """simulation

    the actual simulation begins
    """

    """time points for not external stimulated models"""
    t = np.linspace(start, stop, (stop-start)/time_steps)

    """the 'universal' time list"""
    time_points = [start, stop, Glucose_impuls_start]

    list_of_model_names = [k for k,l in dict_model_switch.items() if l == True]

    running_chit = []
    for NameOfModel in list_of_model_names:

        for TRT,DOSE_list in dict_stimuli.items():
            for SingleDose in DOSE_list:
                """for every dose volume a new Simulation"""

                if NameOfModel in models_ext_stimulus:

                    """all the time points for the simulation"""
                    time_points.extend(dict_of_EXSTDTC[TRT])

                    """if there are multiple stimuli events at one time point"""
                    time_points = list(set(time_points))
                    time_points.sort()

                    switchboard = [1,1,1,1,1]

                    time_of_simulations_test = [np.linspace(i, j, (j-i)/time_steps)
                                        for i,j in zip(time_points[0::],time_points[1::])
                                        ]

                else:
                    switchboard = [1,0,0,0,1]
                    time_of_simulations_test = [t]
                
                dict_running_chit = {'name' : NameOfModel,
                                    'EXTRT': TRT,
                                    'EXDOSE': SingleDose,
                                    'EXSTDTC_list': dict_of_EXSTDTC[TRT],
                                    'results': time_of_simulations_test,
                                    }
                                    
                liste_compress = list(itertools.compress(dict_running_chit,switchboard))

                dict_running_chit = {i : dict_running_chit[i] for i in liste_compress}

                """append to the rest of the toodo simulation"""
                running_chit.append(dict_running_chit)

               
                if NameOfModel not in models_ext_stimulus:
                    break
            if NameOfModel not in models_ext_stimulus:
                break


    for ijj in running_chit:

        """initialize an empty DataFrame for each time value"""
        simulation_frame = pd.DataFrame()
        model_name = ijj['name']


        """check, how many SEQ number already exists"""
        cur.execute(sql.SQL("SELECT MAX(EXSEQ) FROM {}.ex;").format(\
                    sql.Identifier(model_name)))

        SEQ_old = cur.fetchone()[0]
        if SEQ_old == None:
            SEQ_old = 0

        """SEQ for new simulation"""
        SEQ = SEQ_old + 1


        if model_name not in models_ext_stimulus:
            EXTRT = 0
            EXDOSE = 0
            EXSTDTC_list = [0]

        else:
            EXTRT = ijj['EXTRT']
            EXDOSE = ijj['EXDOSE']
            EXSTDTC_list = ijj['EXSTDTC_list']

        EX_dict = {
                    "studyid" : STUDYID,
                    "domain" : "ex",
                    "usubjid" : model_name,
                    "exseq" : SEQ,
                    "excat" : EXCAT,
                    "extrt" : EXTRT,
                    "exdose" : EXDOSE,
                    "exdosu" : "mM",
                    "exstdtc_array" : EXSTDTC_list,
                    "simulation_start": start,
                    "simulation_stop": stop,
                    "co" : "exstdtc in Sekunden",
                    "modelversion": SpecificModelVersionSEQ,
                    "initvaluesversion": SpecificInitValuesVersionSEQ,
                    }


        csv_fingerprint = str(SEQ)

        init_cond = []
        init_cond_string = []
        init_cond_unit = []

        """get the parameter and initial values"""
        exec(open('{0}/Single_Models/{1}/{1}.py'.format(cwd, model_name)\
                    ,encoding="utf-8").read())

        if model_name != 'dummie':

            cur.execute(sql.SQL("""
                SELECT testcd, orres, orresu
                FROM {}.init_values 
                WHERE seq=%s;
                """).format(sql.Identifier(model_name)), [SpecificInitValuesVersionSEQ])

            TESTCD_ORRESU_tuple = cur.fetchall()

            """init_dict creation"""
            init_dict = {}
            unit_dict = {}
            for i in TESTCD_ORRESU_tuple:
                init_dict[i[0]] = i[1]
                unit_dict[i[0]] = i[2]

        else:
            dict_of_init_values = eval('{}_init_values'.format(model_name))
            items_from_dict = dict_of_init_values.items()
            for key, value in items_from_dict:
                init_cond.append(value[0])
                init_cond_string.append(value[1])
                init_cond_unit.append(value[2])

            init_dict = dict(zip(init_cond_string, init_cond))
            unit_dict = dict(zip(init_cond_string, init_cond_unit))
        
        """DataFrame initialisieren"""
               
        ijj['units'] = unit_dict

        simulation_frame = pd.DataFrame([init_dict])


        for i in ijj['results']:
            
            working_frame = []

            """ logic behind the simulation

            if the time has come ... and a stimulus is activated ...
            and a compartible model is choosen ...
            """
          
            if i[0] in EXSTDTC_list\
            and model_name in models_ext_stimulus:

                for TESTCDAffectedByStimulus in dict_stimulus.get(EXTRT)[2]:

                    """adds the right value to the right ODE"""
                    simulation_frame.loc[i[0],
                                         TESTCDAffectedByStimulus] += EXDOSE

                """switch for glucose adding"""
                glucose_switch= [False]

                simulation_frame = x.simulation(DataForSimulation=simulation_frame,
                                                i=i
                                                )

            elif i[0] == Glucose_impuls_start\
            and model_name in models_ext_stimulus:

                # glucose_switch= [True]
                # note: i exclueded the glucose stimulus 
                glucose_switch= [False]
                simulation_frame = x.simulation(DataForSimulation=simulation_frame,
                                                i=i
                                                )

            else:

                glucose_switch= [False]
                simulation_frame = x.simulation(DataForSimulation=simulation_frame,
                                                i=i
                                                )

            
        """replace the time array with the simulation results"""
        ijj['results'] = simulation_frame

        print(SEQ, "model_name", model_name)

        """last step before pushing results to database
        
        beautify the results
        """

        """round the time points"""
        RoundByUsedTimeSteps = abs(Decimal(str(time_steps)).as_tuple().exponent)

        OldTimeIndex = list(ijj['results'].index)
        NewTimeIndex = np.round(OldTimeIndex, decimals = RoundByUsedTimeSteps)

        DfAsMatrix = ijj['results'].values
        ColumnsOfDataframe = ijj['results'].columns.tolist()
        

        def truncate(n, decimals=0):
            multiplier = 10 ** decimals
            return int(n * multiplier) / multiplier

        RoundAfterDigitsCound = 5
        NumbersWithoutZero = list(range(1, 10))
        NumbersWithoutZero = [str(x) for x in NumbersWithoutZero]

        for (x, y), UnroundedValue in np.ndenumerate(DfAsMatrix):

            GetDecimalPointPosition = str(UnroundedValue).find('.')
            for index, i in enumerate(str(UnroundedValue)):
                if i in NumbersWithoutZero:
                    FirstOccurenceNaturalNumber = index
                    if index > GetDecimalPointPosition:
                        FirstOccurenceNaturalNumber -= 1
                    break

            TruncateIndex = FirstOccurenceNaturalNumber + RoundAfterDigitsCound - GetDecimalPointPosition

            RoundedValue = truncate(UnroundedValue, decimals=TruncateIndex)

            DfAsMatrix[x, y] = RoundedValue


        ijj['results'] = pd.DataFrame(DfAsMatrix, 
            columns=ColumnsOfDataframe,
            index=NewTimeIndex)

        """get less data 
        
        only get each (1/time_steps) simulation results
        """
        ijj['results'] = ijj['results'].loc[::int(1/time_steps)]


        """export the EX dict to the database"""
        if dict_system_switch.get('export_data_to_sql') == True:
            keys_db = tuple(EX_dict.keys())
            values_db = tuple(EX_dict.values())

            """dict to sql database"""
            insert_statement = 'insert into {}.ex (%s) values %s'.format(
                model_name)
            cur.execute(cur.mogrify(insert_statement,
                                    (AsIs(','.join(keys_db)), tuple(values_db))))

            conn.commit()

            """make the dict keys as new variables"""
            locals().update(ijj)

            pd_to_dict = ijj['results'].to_dict('index')

            for DTC,inner_dict in pd_to_dict.items():
                for substance,value in inner_dict.items():

                    dict_test = {}
                    dict_test['studyid'] = STUDYID
                    dict_test['domain'] = 'pd'
                    dict_test['usubjid'] = model_name
                    dict_test['pdseq'] = SEQ
                    dict_test['pdtestcd'] = substance
                    dict_test['pdtest'] = None
                    dict_test['pdorres'] = value
                    dict_test['pdorresu'] = ijj['units']['{}'.format(substance)]
                    dict_test['pddtc'] = DTC
                    dict_test['co'] = "pddtc in Sekunden"

                    keys_db = tuple(dict_test.keys())
                    values_db = tuple(dict_test.values())

                    """dict to sql database"""

                    insert_statement = 'insert into {}.pd (%s) values %s'.format(model_name)
                    cur.execute(cur.mogrify(insert_statement, (AsIs(','.join(keys_db)), tuple(values_db))))

                    conn.commit()

    cur.close()
    conn.close()
