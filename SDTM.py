__author__ = 'Jan N. Piotraschke'
__email__ = 'jan.piotraschke@mail.de'
__version__ = 'bachelor_thesis'
__license__ = 'private'

"""import the standard used packages"""
exec(open("SYSTEM/py_packages.py").read())
from decimal import Decimal
import uuid
import sys

class netzwerk_daten_gewinnung:
    def __init__(self):
        pass


    def plotTimeSeries(TimeSeriesData_df=pd.DataFrame(),
                    SubplotLogic={},
                    Terms=False):
            """ def description

            this function only needs the ODE results and the ORRESU_dict to
            visualise the time-series

            SubplotLogic = {ylabel_str : correspondingSubstance_list}
            """
            
            if len(SubplotLogic.keys()) == 0:
                SubplotLogic[1] = 'a'
                GeneralizePlot = True
            else:
                GeneralizePlot = False

            sns.set_style(style='whitegrid')
            # context : dict, None, or one of {paper, notebook, talk, poster}
            sns.set_context(context='talk')
            fig = plt.figure(figsize=(10, 7.5))

            """fontSize 16 is a good size for the thesis"""
            fontSize = 16

            """create the subplots"""
            iter_num = 1

            """pre define the subplots structures"""
            for ORRESU, j in SubplotLogic.items():
                exec('ax{0} = fig.add_subplot({1}, 1, {0})'.format(iter_num,
                                                                len(SubplotLogic)))
                exec('ax{}.spines["top"].set_visible(False)'.format(iter_num))
                exec('ax{}.spines["right"].set_visible(False)'.format(iter_num))
                exec(
                    'ax{}.set_xlabel("time [s]",fontsize=fontSize)'.format(iter_num))

                """fix the y-axis lim for pictures for latex / publication"""
                # exec('ax{}.set_ylim(bottom=-20000, top=50000)'.format(iter_num))

                if GeneralizePlot == True:
                    exec("ax{}.set_ylabel('no unit',fontsize=fontSize)".format(iter_num))
                else:
                    exec('ax{}.set_ylabel(ORRESU,fontsize=fontSize)'.format(iter_num))

                iter_num += 1

            """x axis is shared and the ticks are rotated"""
            fig.autofmt_xdate(bottom=0.2,
                            rotation=30)
            fig.suptitle(t='{}_Model'.format(model_name.title()),
                         fontsize=fontSize)

            # fig.suptitle(t='Volume',
            #             fontsize=fontSize)

            with sns.color_palette('cubehelix', len(TimeSeriesData_df.columns.tolist())):

                """make the fig more fittet"""
                # fig.tight_layout(pad = 3,
                #                 rect = [0,0,0.85,1]
                #                 )

                # """show the version of the plot"""
                # fig.text(0.99, 0.01,
                #          s='{} - {}'.format(current_date,
                #                             sql_USUBJID.title()),
                #          fontstyle='italic',
                #          color='#999999',
                #          ha='right',
                #          va='bottom',
                #          fontsize='x-small'
                #         )

                """assign each TESTCD to their right subplot"""
                if GeneralizePlot == False:
                    for ORRESU_tuple, axis_index in zip(SubplotLogic.items(),
                                                        range(1, len(SubplotLogic)+1)):
                        parameter, substance = ORRESU_tuple

                        for i in substance:

                            if model_name == 'combined_models' and i == 'Hog1PPn':
                                exec(
                                    "ax{}.plot(TimeSeriesData_df[i],label='Hog1PPn (*1E7)')".format(axis_index))

                            else:
                                if Terms == True:
                                    exec("ax{0}.plot(TimeSeriesData_df[i],label=EquationTerms_dict[i])".format(
                                        axis_index))

                                else:
                                    exec('ax{0}.plot(TimeSeriesData_df[i],label=i)'.format(
                                        axis_index))

                            exec('ax{0}.legend(ncol=1,borderaxespad = 0,bbox_to_anchor=(1.01, 0.5), \
                                frameon = True,loc={1!r},fontsize=fontSize)'.format(axis_index, 'center left'))

                else:
                    PlotLabels = TimeSeriesData_df.columns.tolist()
                    for i in PlotLabels:
                        exec('ax1.plot(TimeSeriesData_df[i],label=i)')
                        exec("ax1.legend(ncol=1,borderaxespad = 0,bbox_to_anchor=(1.01, 0.5), \
                                    frameon = True,loc='center left',fontsize=fontSize)")

                """"save the plot"""
                
                PictureName = '{0}_{1}.png'.format(model_name, SEQ)
                plt.savefig('SimulationPictures/{0}'.format(PictureName),
                    dpi=360,
                    format='png',
                    bbox_inches='tight'
                )

                # """pre check if picture is already saved in database"""
                # cur.execute(sql.SQL("""
                #         Select max(seq) from {0}.analysis 
                #         """).format(sql.Identifier(model_name)))
                
                # if cur.fetchone()[0] != SEQ:
                #     cur.execute(sql.SQL("""
                #             INSERT INTO {0}.analysis(
                #                 seq, namepicture)
                #                 VALUES(%s, %s);
                #             """).format(sql.Identifier(model_name)), [SEQ, PictureName])

                #     conn.commit()
                
                return PictureName
                   
                
    def prepareVisualization(sql_USUBJID='', ODE_RESULTS = pd.DataFrame(), PDORRESU_x = {}):
        """conversion r to V

        convert the radius to the volume unit for better understandung of the
        cell system
        """

        # TEMP: temporary solution; PDORRESU = PDORRESU_x because otherwise it 
        # overwrites the ijj['units'] dict --> local/global variable problem?
        if sql_USUBJID == 'combined_models':
            NotToVisualize = dict_visualisation.get('not_to_visualize')
            ColumnsOfDataframe = ODE_RESULTS.columns.tolist()

            ColumnsToVisualize = list(
                set(ColumnsOfDataframe) - set(NotToVisualize))

            for i in NotToVisualize:
                ODE_RESULTS = ODE_RESULTS.drop(columns=[i])

            PDORRESU = {
                i: PDORRESU_x[i] for i in ColumnsToVisualize if i in PDORRESU_x}

            try:
                ODE_RESULTS['Hog1PPn'] = ODE_RESULTS['Hog1PPn'] * 1E7
                # ODE_RESULTS['Cl_in'] = ODE_RESULTS['Cl_in'] / 10
            except:
                pass
        else: 
            PDORRESU = PDORRESU_x

        convert_r_to_V = ['r', 'r_os', 'r_b', 'R_ref']
        ODE_RESULTS_columns = ODE_RESULTS.columns.tolist()
        for column_name in ODE_RESULTS_columns:

            if column_name in convert_r_to_V:
                ODE_RESULTS[column_name] = (
                    4/3) * np.pi * ODE_RESULTS[column_name]**3

                """"rename the column name

                change the first letter to 'V' and append then the rest of the
                old word string to this
                """
                new_column_name = 'V' + column_name[1:]
                ODE_RESULTS.rename(columns={column_name: new_column_name},
                                    inplace=True
                                    )
                """adapt the PDORRESU dict to the new units"""
                if column_name in PDORRESU:
                    PDORRESU[new_column_name] = PDORRESU.pop(column_name)
                    PDORRESU[new_column_name] = 'fL'

     
        """group the keys by their units"""
        PDORRESU_grouped = {}
        for key, value in sorted(PDORRESU.items()):
            PDORRESU_grouped.setdefault(value, []).append(key)

        """some design condition for the bachelor plots"""
        if sql_USUBJID == 'volume':
            ODE_RESULTS = pd.DataFrame(ODE_RESULTS['V'])
            PDORRESU_grouped = {'total volume [fL]': ['V']}

        return ODE_RESULTS, PDORRESU_grouped


    def ODE_solver(InitialValues, t):

        ResultsDict = {}
        TermResultsDict = {}
        OdeResultsForSolver = []
        t_ODE_comp = ()
        
        """get the Names of the ODEs"""
        ColumnNames = simulation_frame.columns.tolist()

        """assing the initial values to their ODEs"""
        for i in range(len(InitialValues)):
            try:               
                exec('{}={}'.format(ColumnNames[i], InitialValues[i]))

            except:
                print(ColumnNames[i], InitialValues[i], 'time:', t)

        """get the model system from the json file"""
        with open('Single_Models/json_files/{0}_system.json'.format(
            model_name)) as json_data:
            data_from_json = json.load(json_data)

        """activate the model system"""
        for EquationType, ModelSpecies in data_from_json.items():
            if EquationType == 'copa':
                for CopaName, CopaTerm in ModelSpecies.items():

                    exec('{}={}'.format(CopaName,CopaTerm))

            else:
                """iterate over the content for the species"""
                for SpeciesName,SpeciesContent in ModelSpecies.items():
                    if 'condition' in SpeciesContent:
                    
                        for TermPat,Term in SpeciesContent['component'].items():
                  
                            """activate the term under its condition"""
                            exec('{}={} {}'.format(TermPat, Term,
                                                   SpeciesContent['condition']))

                            """add TermPat to a set / list for database"""
                            t_ODE_comp = t_ODE_comp + (TermPat,)

                    else:
                        for TermPat,Term in SpeciesContent['component'].items():

                            exec('{}={}'.format(TermPat,Term))
                            t_ODE_comp = t_ODE_comp + (TermPat,)

                    """rejoin the terms to their equation"""
                    list_values = list(SpeciesContent['component'].keys())

                    """
                    prepare to calculate the sum of the terms of a substance
                    """
                    EquationTerms = '+'.join(list_values)

                    KeysPlaceholder = SpeciesName
                    exec('{}={}'.format(KeysPlaceholder,EquationTerms))

                    if EquationType == 'ODE':
                        ResultsDict[SpeciesName] = eval(SpeciesName)

        """sort the OdeResultsForSolverPlaceholder

        this must be done because the json file is not sorted!
        """
        ResultsDict = OrderedDict(sorted(ResultsDict.items()))

        """ODE results for the next simulation step of the ODE solver"""
        OdeResultsForSolver = [j for i, j in ResultsDict.items()]

        """export the individuel terms to the database"""
        if dict_system_switch.get('export_data_to_sql') == True\
        and dict_system_switch.get('export_terms_data_to_sql') == True:

            """sql connection"""
            engine = create_engine(
                'postgres://postgres:@db_postgres:5432/simulation_results')

            df_dict_term = {}
            for i in t_ODE_comp:
                df_dict_term[i] = eval(i)

            df = pd.DataFrame(df_dict_term, index=[t])

            df.to_sql(csv_fingerprint, con=engine, schema='{}_terms'.format(model_name), if_exists='append')

        return OdeResultsForSolver


    def simulation(DataForSimulation=pd.DataFrame(), i=[]):
        init_cond_from_frame = DataForSimulation.tail(1).values.tolist()[0]

        """solves the ode and algebraic equations"""
        states = odeint(x.ODE_solver, init_cond_from_frame, i)



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

    exec(open("createDatabaseStructure.py").read())
    exec(open("initializeModel.py").read())

    dict_visualisation = {

        'not_to_visualize': ['Yt', 'z1', 'z2', 'z3', 'z4', 'L_ArH', 'L_HH',
                             'Na_in', 'Na_out', 'K_out', 'K_in',
                             'Cl_out', 'H_in', 'H_out', 'ATP', 'Hog1PPc',
                             'Hog1c', 'Hog1n', 'Pbs2', 'Pbs2PP', 'R_ref', 'r_os', 'r_b', 'c_i', 'Sorbitol_out'],
        # 'exp_rel_var': ['Hog1PPn', 'r', 'Glyc_in', 'pi_t', 'Deltaphi', 'Cl_in'],
        # # type the name of the ODE substance you are interested in
        # # if empty --> normal plots
        # 'special_interest': [],

        # 'each_single_model': False,
        }
    """momentanes arbeitsverzeichnis = cwd"""
    cwd = os.getcwd()

    x = netzwerk_daten_gewinnung

    STUDYID = 'Yeast_BSc'
    EXCAT = 'Salz'

    json_args = sys.argv[1]
    args = json.loads(json_args)

    dict_time = {
            'start': float(args['dict_time']['start']),
            'stop': float(args['dict_time']['stop']),
            'time_steps': float(args['dict_time']['time_steps']),
            'Glucose_impuls_start': float(args['dict_time']['Glucose_impuls_start']),
            'Glucose_impuls_end': float(args['dict_time']['Glucose_impuls_end']),
            'NaCl_impuls_start': float(args['dict_time']['NaCl_impuls_start']),
            'NaCl_impuls_firststop': float(args['dict_time']['NaCl_impuls_firststop']),
        }
    

    dict_model_switch = args['dict_model_switch']
    dict_unique_EXSTDTC = args['dict_unique_EXSTDTC']
    dict_stimulus = args['dict_stimulus']
    dict_system_switch = args['dict_system_switch']

    """only one model each time as True"""
    # dict_model_switch = {
    #                     'combined_models': False,
    #                     # 'dummie': False,
    #                     'hog': False,
    #                     'ion': True,
    #                     'volume': False,
    #                      }

    # dict_time = {
    #             'start' : 0,
    #             'stop' : 80,  
    #             'time_steps' : 0.1,
    #             'NaCl_impuls_start': 30,
    #             'NaCl_impuls_firststop' : 10,
    #             'Glucose_impuls_start' : 1,
    #             'Glucose_impuls_end' : 13,
    #             }

    """make the dict keys as new variables"""
    locals().update(dict_time)

    """Stimulus = [time] in s"""
    # dict_unique_EXSTDTC = {                                
    #                             'KCl' : [30],
    #                             'NaCl' : [30],
    #                             'Sorbitol' : [30],
    #                         }

    """implementation rules

    Stimulus = [[value(s)], unit, [target(s)], boolean]
    """
    """only for the hog model

    signal_type :
        1: one steady impulse
        2: single pulse of NaCl
        3: square pulses of NaCl
        4: up-staircase change of NaCl
    """
    # dict_stimulus = {
    #                 'KCl' : [[200], 'mM', ['K_out','Cl_out'], True],
    #                 'NaCl': [[800], 'mM', ['Na_out', 'Cl_out'], False],
    #                 'Sorbitol': [[1600], 'mM', ['Sorbitol_out'], False],

    #                 'NaCl_impuls' : [200, 'mM'],
    #                 'signal_type' : [2],
    #                 }

    signal_type = dict_stimulus.get('signal_type')[0]
    NaCl_impuls = dict_stimulus.get('NaCl_impuls')[0]

    """database management system"""
    # NOTE : SpecificInitValuesVersionSEQ = 2 for combined_models (4 ist alte Version)
    # NOTE : SpecificModelVersionSEQ = 6 for combined_models (oder 14 (mit Glucose * - V_ratio))
    # NOTE : Ion Model --> Model Version 3 hat eine vebesserte ATP Berechnung --> macht aber keine Auswirkung
    # NOTE : Hog Model --> Model Version 4 ist besser
    # NOTE: SpecificParameterVersionSEQ muss die 1 behalten, da die Parameter nicht veraendert wurden
    # dict_system_switch = {
    #                     'export_data_to_sql' : True,
    #                     'export_terms_data_to_sql' : False,
    #                     'SpecificInitValuesVersionSEQ' : [1],
    #                     'SpecificModelVersionSEQ' : [1],
    #                     'SpecificParameterVersionSEQ' : [1]
    #                      }


    """host name taken from docker-compose.yml"""
    conn = psycopg2.connect(
        host='db_postgres',
        user='postgres',
        dbname='simulation_results'
    )

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

            # TODO: notloesung: definiere folgendes als funktion um
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
            
            """gets the wanted ParameterValuesVersion"""
            if len(dict_system_switch.get('SpecificParameterVersionSEQ')) > 0:
                SpecificParameterVersionSEQ = dict_system_switch.get(
                    'SpecificParameterVersionSEQ')[0]

            else:
                """get the MAX(seq) value from the database"""
                cur.execute(sql.SQL("""
                    SELECT MAX(seq)
                    FROM {}.parameter;
                    """).format(sql.Identifier(NameOfModel)))

                SpecificParameterVersionSEQ = cur.fetchone()[0]

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
       
            """list of the names of the ODE in the model"""
            cur.execute(sql.SQL("""
                    SELECT testcd
                    FROM {}.init_values
                    WHERE seq = %s
                    """).format(sql.Identifier(NameOfModel)), [SpecificInitValuesVersionSEQ])

            ModelOdeVariable = cur.fetchall()
            ModelOdeVariable = [x[0] for x in ModelOdeVariable]


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

        # SEQ = str(uuid.uuid4())

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
                    "parameterversion": SpecificParameterVersionSEQ
                    }


        csv_fingerprint = str(SEQ)

        init_cond = []
        init_cond_string = []
        init_cond_unit = []

        """get the parameter from the database"""
        cur.execute(sql.SQL("""
            SELECT testcd, orres
            FROM {}.parameter 
            WHERE seq=%s;
            """).format(sql.Identifier(model_name)), [SpecificParameterVersionSEQ])

        TESTCD_ORRESU_tuple = cur.fetchall()

        """init_dict creation"""
        parameter_dict = {}
        for i in TESTCD_ORRESU_tuple:
            parameter_dict[i[0]] = i[1]
        
        """make the dict keys as new variables"""
        locals().update(parameter_dict)


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
                glucose_switch= [True]
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


        """create a copy for the design of the plot"""
        ODE_RESULTS_raw = ijj['results']

        ODE_RESULTS, PDORRESU_grouped = x.prepareVisualization(
            sql_USUBJID=model_name, ODE_RESULTS=ODE_RESULTS_raw, PDORRESU_x=ijj['units'])

        """plot the results, save the plot and return the PictureName"""
        PictureName = x.plotTimeSeries(TimeSeriesData_df=ODE_RESULTS,
                                           SubplotLogic=PDORRESU_grouped)

        EX_dict['namepicture'] = PictureName

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
        
        if list_of_model_names[0] != 'volume':
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

            print("Daten hochgeladen")

    print("simulation finished")

    cur.close()
    conn.close()

