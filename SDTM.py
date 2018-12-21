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
                'stop' : 100,  
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
                    'KCl' : [[200], 'mM', ['K_out','Cl_out'], True],
                    'NaCl' : [[0.3,3,30,300,600], 'mM', ['Na_out','Cl_out'], False],
                    'Sorbitol': [[300], 'mM', ['Sorbitol_out'], False],

                    'NaCl_impuls' : [200, 'mM'],
                    'signal_type' : [3],
                    }


    """database management system"""
    dict_system_switch = {
                        'export_data_to_sql' : True,
                        'export_terms_data_to_sql' : False,
                        'SpecificInitValuesVersionSEQ' : [],
                        'SpecificModelVersionSEQ' : []
                         }

    """activated stimuli

    find out which stimulus pipeline is opened for the experiment series
    """
    activated_stimuli = [stimulus_name for stimulus_name, boolean
                        in dict_stimulus.items() if boolean[-1] == True]


    """ affected models

    find out the from stimuli affected models
    """
    models_ext_stimulus = []
    for model_name, boolean in dict_model_switch.items():
        if boolean == True:
            exec(open('{0}/Single_Models/{1}/{1}.py'.format(cwd, model_name),encoding="utf-8").read())

            """list of the names of the variables in the model"""
            list_of_var_keys = eval('{}_init_values'.format(model_name)).keys()

            """iterating over all activated stimuli"""
            for i in activated_stimuli:

                """get me the target of the specific stimuli"""
                target = dict_stimulus.get(i)[2]

                """if the targets are in the specific model"""
                if set(target).issubset(list_of_var_keys) == True:
                    models_ext_stimulus.append('{}'.format(model_name))

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

            """find the right stimuli-simulation-time-list for this impuls"""
            if key in dict_unique_EXSTDTC.keys():

                dict_of_EXSTDTC[key] = dict_unique_EXSTDTC[key]

    dict_stimuli = dict(zip(list_of_stimuli_name, list_of_stimuli_conc))

    list_of_model_names = []
    for key,value in dict_model_switch.items():
        if value == True:
            list_of_model_names.append(key)

    """simulation

    the actual simulation begins
    """

    """time points for not external stimulated models"""
    t = np.linspace(start, stop, (stop-start)/time_steps)
    time_of_simulations = [start, t]

    """the 'universal' time list"""
    time_points = [start, stop, Glucose_impuls_start]

    model_test = [k for k,l in dict_model_switch.items() if l == True]

    running_chit = []
    for choosen_model in model_test:
        if choosen_model != 'hog':
            """update the local safed ModelVersion"""
            conn = psycopg2.connect(host='localhost', dbname='simulation_results')
            cur = conn.cursor()

            """gets the wanted ModelVersion"""
            if len(dict_system_switch.get('SpecificModelVersionSEQ')) > 0:
                SpecificModelVersionSEQ = dict_system_switch.get(
                    'SpecificModelVersionSEQ')[0]
            else:
                """get the MAX(seq) value from the database"""
                cur.execute(sql.SQL("""
                    SELECT MAX(seq)
                    FROM {}.json;
                    """).format(sql.Identifier(choosen_model)))

                SpecificModelVersionSEQ = cur.fetchone()[0]

            cur.execute(sql.SQL("""
                SELECT model_version
                FROM {}.json
                WHERE seq = %s;
                """).format(sql.Identifier(choosen_model)), [SpecificModelVersionSEQ])

            ModelVersionFromDatabase = cur.fetchone()[0]

            cur.close()
            conn.close()

            """create json format"""

            s = json.dumps(ModelVersionFromDatabase, indent=4)
            with open('Single_Models/json_files/{0}_system.json'.format(choosen_model), "w") as f:
                f.write(s)

        conn = psycopg2.connect(host='localhost', dbname='simulation_results')
        """open a cursor to perform database operations"""
        cur = conn.cursor()

        """create a new schema (=new model)"""
        try:
            cur.execute(sql.SQL("CREATE SCHEMA {};").format(\
                            sql.Identifier(choosen_model)))
        except:
            pass

        conn.commit()

        """intervention (EX) domain table creaton"""
        try:
            cur.execute(sql.SQL("""
                CREATE TABLE {}.{}(
                    STUDYID text,
                    DOMAIN text,
                    USUBJID text,
                    EXSEQ integer,
                    EXCAT text,
                    EXTRT text,
                    EXDOSE real,
                    EXDOSU text,
                    EXSTDTC double precision,
                    CO text,
                    MODELVERSION integer,
                    INITVALUESVERSION integer, 
                    PRIMARY KEY (USUBJID, EXSEQ, EXTRT)
                )
                """).format(sql.Identifier(choosen_model),sql.Identifier('ex')))

        except:
            pass
        conn.commit()

        """findings (PD) domain table creaton"""
        try:
            cur.execute(sql.SQL("""
                CREATE TABLE {}.{}(
                    STUDYID text,
                    DOMAIN text,
                    USUBJID text,
                    PDSEQ integer,
                    PDTESTCD text,
                    PDTEST text,
                    PDORRES double precision,
                    PDORRESU text,
                    PDDTC double precision,
                    CO text,
                    PRIMARY KEY (USUBJID, PDSEQ, PDTESTCD, PDDTC)
                )
                """).format(sql.Identifier(choosen_model),sql.Identifier('pd')))

        except:
            pass

        conn.commit()
        cur.close()
        conn.close()

        for yy,kl in dict_stimuli.items():
            for xkl in kl:
                for zy in dict_of_EXSTDTC[yy]:
                    if choosen_model in models_ext_stimulus:
                        switchboard = [1,1,1,1,1]

                        time_of_simulations_test = []

                        time_points.append(zy)
                        time_points.sort()

                        simulation_test = [np.linspace(i,j,(j-i)/time_steps)
                                            for i,j in zip(time_points[0::],time_points[1::])
                                            ]

                        """remove that you can add for a new simulation"""
                        time_points.remove(zy)

                        for i in simulation_test:
                            time_of_simulations_test.append(i)
                    else:
                        switchboard = [1,0,0,0,1]
                        time_of_simulations_test = [np.linspace(start, stop, (stop-start)/time_steps)]

                    dict_running_chit = {'name' : choosen_model,
                                        'EXTRT' : yy,
                                        'EXDOSE' : xkl,
                                        'EXSTDTC' : zy,
                                        'results' : time_of_simulations_test,
                                        }

                    liste_compress = list(itertools.compress(dict_running_chit,switchboard))

                    dict_running_chit = {i : dict_running_chit[i] for i in liste_compress}

                    """append to the rest of the toodo simulation"""
                    running_chit.append(dict_running_chit)

                    if choosen_model not in models_ext_stimulus:
                        break
                if choosen_model not in models_ext_stimulus:
                    break
            if choosen_model not in models_ext_stimulus:
                break



        # # TODO:
        # """scenario if all stimuli are False"""
        # if len(dict_stimuli.keys()) == 0:
        #     time_of_simulations_test = [np.linspace(start, stop, (stop-start)/time_steps)]
        #     for choosen_model in model_test:
        #         dict_running_chit = {'name' : choosen_model,
        #                             'EXTRT' : 0,
        #                             'EXDOSE' : 0,
        #                             'EXSTDTC' : 0,
        #                             'results' : time_of_simulations,
        #                             }
        #         running_chit.append(dict_running_chit)



    """create list for simulaiton results"""
    simulation_results = []
    for ijj in running_chit:

        """initialize an empty DataFrame for each time value"""
        simulation_frame = pd.DataFrame()
        model_name = ijj['name']

        conn = psycopg2.connect(host='localhost', dbname='simulation_results')

        cur = conn.cursor()

        """check, how many SEQ number already exists"""
        cur.execute(sql.SQL("SELECT MAX(EXSEQ) FROM {}.ex;").format(\
                    sql.Identifier(model_name)))

        SEQ_old = cur.fetchone()[0]
        if SEQ_old == None:
            SEQ_old = 0

        """SEQ for new simulation"""
        SEQ = SEQ_old + 1

        """create the term schema"""
        try:
            cur.execute(("CREATE SCHEMA {}_terms;").format(model_name))
        except:
            pass

        conn.commit()
        cur.close()
        conn.close()

        if model_name not in models_ext_stimulus:
            EXTRT = 0
            EXDOSE = 0
            EXSTDTC = 0

        else:
            EXTRT = ijj['EXTRT']
            EXDOSE = ijj['EXDOSE']
            EXSTDTC = ijj['EXSTDTC']

        conn = psycopg2.connect(host='localhost', dbname='simulation_results')

        """open a cursor to perform database operations"""
        cur = conn.cursor()
        """gets the wanted InitValuesVersion"""
        if len(dict_system_switch.get('SpecificInitValuesVersionSEQ')) > 0:
            SpecificInitValuesVersionSEQ = dict_system_switch.get(
                'SpecificInitValuesVersionSEQ')[0]

        else:
            """get the MAX(seq) value from the database"""
            cur.execute(sql.SQL("""
                SELECT MAX(seq)
                FROM {}.init_values;
                """).format(sql.Identifier(model_name)))

            SpecificInitValuesVersionSEQ = cur.fetchone()[0]

        cur.close()
        conn.close()

        EX_dict = {
                    "studyid" : STUDYID,
                    "domain" : "ex",
                    "usubjid" : model_name,
                    "exseq" : SEQ,
                    "excat" : EXCAT,
                    "extrt" : EXTRT,
                    "exdose" : EXDOSE,
                    "exdosu" : "mM",
                    "exstdtc" : EXSTDTC,
                    "co" : "exstdtc in Sekunden",
                    "modelversion": SpecificModelVersionSEQ,
                    "initvaluesversion": SpecificInitValuesVersionSEQ,
                    }

        """export the EX dict to the database"""
        if dict_system_switch.get('export_data_to_sql') == True:
            conn = psycopg2.connect(host='localhost', dbname='simulation_results')

            """open a cursor to perform database operations"""
            cur = conn.cursor()

            """update database"""
            keys_db = tuple(EX_dict.keys())
            values_db = tuple(EX_dict.values())

            """dict to sql database"""
            try:
                insert_statement = 'insert into {}.ex (%s) values %s'.format(model_name)
                cur.execute(cur.mogrify(insert_statement, (AsIs(','.join(keys_db)), tuple(values_db))))
            except:
                pass

            conn.commit()

            cur.close()
            conn.close()

      
        csv_fingerprint = str(SEQ)

        init_cond = []
        init_cond_string = []
        init_cond_unit = []

        """get the parameter and initial values"""
        exec(open('{0}/Single_Models/{1}/{1}.py'.format(cwd, model_name)\
                    ,encoding="utf-8").read())

        if model_name != 'dummie':

            # NOTE: test area

            conn = psycopg2.connect(
                host='localhost', dbname='simulation_results')

            cur = conn.cursor()

            # """gets the wanted InitValuesVersion"""
            # if len(dict_system_switch.get('SpecificInitValuesVersionSEQ')) > 0:
            #     SpecificInitValuesVersionSEQ = dict_system_switch.get(
            #         'SpecificInitValuesVersionSEQ')[0]

            # else:
            #     """get the MAX(seq) value from the database"""
            #     cur.execute(sql.SQL("""
            #         SELECT MAX(seq)
            #         FROM {}.init_values;
            #         """).format(sql.Identifier(model_name)))

            #     SpecificInitValuesVersionSEQ = cur.fetchone()[0]

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

            cur.close()          
            conn.close()

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
            if i[0] == EXSTDTC\
            and model_name in models_ext_stimulus:

                for stimulus_name_adding in dict_stimulus.get(EXTRT)[2]:

                    """adds the right value to the right ODE"""
                    simulation_frame.loc[EXSTDTC,stimulus_name_adding] += EXDOSE

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

            simulation_results.append(simulation_frame)

        ijj['results'] = simulation_results[-1]

        print(SEQ, "model_name", model_name)

        conn = psycopg2.connect(host='localhost', dbname='simulation_results')

        """open a cursor to perform database operations"""

        cur = conn.cursor()
        cur.execute(sql.SQL("Select * FROM {}.pd;").format(sql.Identifier(model_name)))
        PD_column_names = [desc[0] for desc in cur.description]

        """round the time points"""
        RoundByUsedTimeSteps = abs(Decimal(str(time_steps)).as_tuple().exponent)

        OldTimeIndex = list(ijj['results'].index)
        NewTimeIndex = np.round(OldTimeIndex, decimals = RoundByUsedTimeSteps)

        DfAsMatrix = ijj['results'].values
        ColumnsOfDataframe = ijj['results'].columns.tolist()
        
        """get the size of the matrix"""
        # print(DfAsMatrix.shape)

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
