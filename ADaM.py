__author__ = 'Jan N. Piotraschke'
__email__ = 'jan.piotraschke@mail.de'
__version__ = 'bachelor_thesis'
__license__ = 'private'


"""the only source for ADaM is SDTM or other ADaM databases"""

"""import the standard used packages"""
exec(open("SYSTEM/py_packages.py").read())
import ADaM_preparation

class VisualisationDesign:
    def plotTimeSeries(TimeSeriesData_df = pd.DataFrame(),
                     SubplotLogic = {},
                     Terms = False):

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

        sns.set_style(style = 'whitegrid')
        # context : dict, None, or one of {paper, notebook, talk, poster}
        sns.set_context(context = 'talk')
        fig = plt.figure(figsize = (10,7.5))

        """fontSize 16 is a good size for the thesis"""
        fontSize = 16

        """create the subplots"""
        iter_num = 1

        """pre define the subplots structures"""
        for ORRESU,j in SubplotLogic.items():
            exec('ax{0} = fig.add_subplot({1}, 1, {0})'.format(iter_num,
                                                        len(SubplotLogic)))
            exec('ax{}.spines["top"].set_visible(False)'.format(iter_num))
            exec('ax{}.spines["right"].set_visible(False)'.format(iter_num))
            exec('ax{}.set_xlabel("time [s]",fontsize=12)'.format(iter_num))

            
            """fix the y-axis lim for pictures for latex / publication"""
            # exec('ax{}.set_ylim(bottom=-20000, top=50000)'.format(iter_num))

            if GeneralizePlot == True:
                exec("ax{}.set_ylabel('no unit',fontsize=fontSize)".format(iter_num))
            else:
                exec('ax{}.set_ylabel(ORRESU,fontsize=fontSize)'.format(iter_num))

            iter_num +=1

        """x axis is shared and the ticks are rotated"""
        fig.autofmt_xdate(bottom = 0.2,
                        rotation = 30)
        fig.suptitle(t='{}_Model'.format(sql_USUBJID.title()),
                     fontsize=fontSize)

        with sns.color_palette('cubehelix',len(TimeSeriesData_df.columns.tolist())):

            """make the fig more fittet"""
            # fig.tight_layout(pad = 3,
            #                 rect = [0,0,0.85,1]
            #                 )

            """show the version of the plot"""
            fig.text(0.99, 0.01,
                     s='{} - {}_Model'.format(current_date,
                                              sql_USUBJID.title()),
                    fontstyle='italic',
                    color='#999999',
                    ha='right',
                    va='bottom',
                    fontsize='x-small'
                    )

            """assign each TESTCD to their right subplot"""
            if GeneralizePlot == False:
                for ORRESU_tuple, axis_index in zip(SubplotLogic.items(),
                                                range(1,len(SubplotLogic)+1)):
                    parameter, substance = ORRESU_tuple

                    for i in substance:

                        if sql_USUBJID == 'combined_models' and i == 'Hog1PPn':
                            exec("ax{}.plot(TimeSeriesData_df[i],label='Hog1PPn (*1E7)')".format(axis_index))

                        else:
                            if Terms==True:
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
            save_fig = dict_system_switch.get('save_figures')

            if save_fig[0] == True:
                
                plt.savefig('/Users/janpiotraschke/Bilder_Simulation/{0}_{1}.{2}'.format(
                    sql_USUBJID, sql_SEQ_list[0], save_fig[1]),
                    dpi=360,
                    format=save_fig[1],
                    bbox_inches='tight'
                )

        fig.tight_layout(pad=3)

        plt.show()
        plt.clf()
        plt.close()

    def plotSingleDoseResponse(colour_plot_dict = {}):


        for values in colour_plot_dict.values():
            plt.plot(values["results"], color = values["colour"])


        """add the threshold line = ORRES_min"""
        plt.axhline(ORRES_min, color='k', linestyle='--', alpha = 0.5)

        """colour the area above ORRES_min"""
        plt.fill_between(x = AUC_all_xaxis,
                        y1 = ORRES_min,
                        y2 = AUC_all_yaxis,
                        where = AUC_all_yaxis > ORRES_min,
                        color = 'green',
                        alpha = 0.2,
                        label = "AUC")
        plt.show()

    def plotDoseResponse(EXDOSE_TESTCD_df = pd.DataFrame(),
                        xscale = 'log'):

        fontSize = 16

        # sns.set_style(style = 'whitegrid')
        # context : dict, None, or one of {paper, notebook, talk, poster}
        # sns.set_context(context = 'talk')

        EXDOSE_TESTCD_df.plot(marker='x')
        
        plt.title(s='Dose-Response-Curve',
                  fontsize=fontSize)

        plt.xscale(value = xscale)
        ax = plt.axes()

        ax.set_xlim()

        ax.set_xlabel("stimulus concentration [mM]")
        ax.set_ylabel("Hog1PPn response (AUC) [s*mM]")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)


        """"save the plot"""
        save_fig = dict_system_switch.get('save_figures')
        if save_fig[0] == True:

                plt.savefig('/Users/janpiotraschke/Bilder_Simulation/{0}_{1}.{2}'.format(
                    sql_USUBJID, sql_SEQ_list[0], save_fig[1]),
                    dpi=360,
                    format=save_fig[1],
                    bbox_inches='tight'
                )

        # plt.tight_layout(pad=3)

        # plt.show()

    def plotHeatMap():
        pass

class DataManagement:
    def sortData():
        pass

"""ISO 8601

get the current date and time in a ISO 8601 conform format
"""
time_stamp = datetime.now().strftime("%Y-%m-%dT%H:%M")
current_date = datetime.now().strftime("%Y-%m-%d")
cwd = os.getcwd()


dict_system_switch = {
                    'export_data_to_sql' : False,
                    'create_ADaM_csv' : False,
                    'df_to_latex' : False,
                    'save_figures': [True, 'png'],
                     }

dict_visualisation = {
                    'graph' : False,
                    # 'subplots' : True,
                    'dose_response' : True,
                    'get_terms' : ['r_os'],
                    'dont_do' : True,

                    'not_to_visualize' : ['Yt','z1','z2','z3','z4','L_ArH','L_HH',
                                            'Na_in','Na_out','K_out','K_in',
                                            'Cl_out','H_in','H_out','ATP','Hog1PPc',
                                            'Hog1c','Hog1n', 'Pbs2' ,'Pbs2PP','R_ref','r_os','r_b', 'c_i','Sorbitol_out'],
                    'exp_rel_var' : ['Hog1PPn','r','Glyc_in','pi_t','Deltaphi','Cl_in'],
                    # type the name of the ODE substance you are interested in
                    # if empty --> normal plots
                    'special_interest' : [],

                    'each_single_model' : False,
                     }


"""choose the model"""
sql_STUDYID = 'Yeast_BSc'
sql_USUBJID = 'combined_models'

# sql_SEQ_list = list(range(31, 44)) #+ list(range(3, 11)) 
sql_SEQ_list = list(range(73,86))
# sql_SEQ_list = list(range(73, 75))

# NOTE : 71 for overview --> combined model
# sql_SEQ_list = [71]

"""tracking substance"""
# NOTE: use Hog1PPn as the output of the dose-response curve
TESTCD = 'Hog1PPn'

""""get the wanted equation terms from SQL"""
get_terms = dict_visualisation.get('get_terms')
EquationTerms_list = []
WantedDataJson_dict = {}

if len(get_terms) > 0:

    TermsOrresuGrouped = {}
    

    with open('Single_Models/json_files/{0}_system.json'.format(sql_USUBJID)) as json_data:
        data_from_json = json.load(json_data)

    """all ODEs of the System"""
    ODESystem_list = []
    for i in data_from_json['ODE'].keys():
        ODESystem_list.append(i[1:])

    """iterate over the model equations
    
    note: equations are saved with a 'dt' at the end, if the must be just in 
    multiple ODEs in the same ODE solver step
    """    

    # NOTE : get the terms units!
    RenameTerms_dict = {}
    for i,j in data_from_json['equation'].items():
       
        """ignore 'dt' at the end of the dict keys"""
        a = i[::-1]
        if (a[:2] == 'td' and a[2:][::-1] in get_terms)\
        or i in get_terms:
            WantedDataJson_dict[i] = j
            EquationTerms_list.append(j['component'])

    """iterate over the models ODEs
    
    note: ODE are saved with a 'd' as a prefix
    """

    for i,j in data_from_json['ODE'].items():
        if i[1:] in get_terms:
            """check whether the ODE has only its equation as an input"""
            ComponentJson_list = list(j['component'].values())

            if i[1:] != ComponentJson_list[0][::-1][2:][::-1]:
                EquationTerms_list.append(j['component'])
                WantedDataJson_dict[i[1:]] = j
            else:
                """for renaming of the algebraic equation"""
                RenameTerms_dict[ComponentJson_list[0]] = i[1:]
                
    """merge the ODE and the equation dict into one dict"""
    EquationTerms_dict = {k: v for d in EquationTerms_list for k, v in d.items()}

    """the list for the query"""
    SqlQueryTerms_list = list(EquationTerms_dict.keys())

    """correct the name of the TESTCD"""
    for old_key, new_key in RenameTerms_dict.items():
        WantedDataJson_dict[new_key] = WantedDataJson_dict.pop(old_key)

    # todo : i now leave it like this but it should be changed in json file
    for i in WantedDataJson_dict.keys():
        if i in ODESystem_list:
            old_unit = WantedDataJson_dict[i]['unit']

            """rename the unit for the ODEs"""
            WantedDataJson_dict[i]['unit']=old_unit+' *s^-1'

    TermsPlotLogic = {}
    for i,j in WantedDataJson_dict.items():
        TermsPlotLogic[j['unit']]=list(j['component'].keys())


    if dict_visualisation.get('dont_do') == False:

        QueryTermsData_df = ADaM_preparation.getEquationTermsformSQL(sql_USUBJID=sql_USUBJID,
                                                SqlQueryTerms_list=SqlQueryTerms_list)

        """remove multiple rows"""
        QueryTermsData_df = QueryTermsData_df[~QueryTermsData_df.index.duplicated(keep='first')]

        VisualisationDesign.plotTimeSeries(TimeSeriesData_df=QueryTermsData_df,
                                        SubplotLogic=TermsPlotLogic,
                                        Terms=True)

"""compare models"""
TestSubstance_dict = {
    'ion': 'Deltaphi',
    'hog': 'Hog1PPn',
    'volume': 'r'
    }

TestSubstanceUnit_dict = {
    'ion': 'V',
    'hog':'mM',
    'volume':'um'
} 
# NOTE: models must have the same simulation lenght
# NOTE: combined_models = 71 for ion model, 72 for the rest
CompareSeq_dict = {
    'combined_models': 72,
    'ion': 53,
    'hog': 12,
    'volume': 18
}

SingleModels = ['volume']
for i in SingleModels:
    CompareSeq = {}
    CompareSeq['combined_models'] = CompareSeq_dict['combined_models']
    CompareSeq[i] = CompareSeq_dict[i]
    x = ADaM_preparation.compareModels(ModelsToCompare_list=['combined_models', i],
                                       TestSubstance=TestSubstance_dict[i],
                                       ModelSeq=CompareSeq
                                       )

    if i == 'volume':
        """radius to volume"""
        x['volume'] = (4/3) * np.pi * x['volume']**3
        x['combined_models'] = (4/3) * np.pi * x['combined_models']**3

    # sql_USUBJID = TestSubstance_dict[i]

    # VisualisationDesign.plotTimeSeries(TimeSeriesData_df=x,
    #                                    SubplotLogic={TestSubstanceUnit_dict[i]: [i, 'combined_models']})


"""try to get the data from the database"""
ADaM_dict = ADaM_preparation.getDatafromSQL(sql_STUDYID = sql_STUDYID,
                                            sql_USUBJID = sql_USUBJID,
                                            sql_SEQ_list = sql_SEQ_list)

EXDOSE_TESTCD_list = []
used_EXTRT_list = []

"""iterate over the specific simulation / experimental runs"""
for RUN_SEQ in ADaM_dict.values():

    """for data exchange
    
    .csv file it the choice for data exchange between systems
    """
    if dict_system_switch.get('create_ADaM_csv') == True:
        ADaM_preparation.create_ADaM_csv(RUN_SEQ = RUN_SEQ)

    """exclude some ODEs from the visualisation"""
    if dict_visualisation.get('dont_do') == True\
    and dict_visualisation.get('graph') == True\
    and sql_USUBJID == 'combined_models':
        for i in dict_visualisation.get('not_to_visualize'):
            RUN_SEQ['ODE_RESULTS'] = RUN_SEQ['ODE_RESULTS'].drop(columns=[i])
            RUN_SEQ['PDORRESU'].pop(i,None)


    """make the dict keys as new variables"""
    locals().update(RUN_SEQ)

    Tmax = ODE_RESULTS[TESTCD].idxmax()

    Cmax = ODE_RESULTS[TESTCD].max()
    CTmax_series = ODE_RESULTS.loc[[Tmax]][TESTCD]

    if sql_USUBJID == 'combined_models'\
    and dict_visualisation.get('dose_response') == True:

        conn = psycopg2.connect(host='localhost',
                                dbname='reference_bib')

        cur = conn.cursor()

        """get the max values"""
        cur.execute("SELECT * FROM yeast_ref.bachelor_dummie WHERE co = 'max'")

        test_info = cur.fetchall()
        col_names = [desc[0] for desc in cur.description]
        max_from_db = pd.DataFrame(test_info, columns = col_names)

        """get the min values"""
        cur.execute("SELECT * FROM yeast_ref.bachelor_dummie WHERE co = 'min'")

        test_info = cur.fetchall()
        col_names = [desc[0] for desc in cur.description]
        min_from_db = pd.DataFrame(test_info, columns = col_names)

        cur.close()
        conn.close()

        values_df = min_from_db.loc[(min_from_db['testcd'] == TESTCD)
                                    & (min_from_db['co'] == 'min')]

        ORRES_min = values_df['orres'].values.tolist()[0]

        """Get a list of unique used EXTRT"""
        if EXTRT not in used_EXTRT_list:
            used_EXTRT_list.append(EXTRT)

        conc_time_curve = ODE_RESULTS[TESTCD]

        start_end = []
        for index in range(len(conc_time_curve)):

            """get the values for the index"""
            val_dict = dict(conc_time_curve.iloc[[index]])
            time = list(val_dict.keys())[0]
            conc = val_dict[time]

            if conc >= ORRES_min\
            and len(start_end)%2 == 0 :
                start_end.append(time)

            if conc < ORRES_min\
            and len(start_end)%2 == 1 :
                start_end.append(time)

            if index == range(len(conc_time_curve))[-1]\
            and len(start_end)%2 == 1:
                start_end.append(time)

        """split the list in start and end pairs"""
        start_end_list = [start_end[x:x+2] for x in range(0, len(start_end), 2)]

        conc_time_curve_end = conc_time_curve.tail(1).keys()[0]

        start_end.append(0)
        start_end.append(conc_time_curve_end)
        start_end = list(set(start_end))
        start_end.sort()

        """get the different section for the colour plot"""
        colour_plot_dict = {}
        dict_index = 0
        for i in range(len(start_end)-1):
            colour_plot_dict[dict_index] = {}

            colour_plot_dict[dict_index]["results"] = conc_time_curve[
                                                    start_end[i]:start_end[i+1]
                                                    ]

            # TEMP: error in correct colour allocation--> works for the bachelor
            if conc_time_curve[start_end[i]] >= ORRES_min:
                colour_plot_dict[dict_index]["colour"] = 'red'

            else:
                colour_plot_dict[dict_index]["colour"] = 'black'

            dict_index += 1

        """calculate the time over the min threshold

        ==> effective dose time
        """
        TC_over_min = 0
        for i in start_end_list:
            TC_over_min += (i[1])-(i[0])

        """calculate AUC with the trapezoidal rule"""
        simulation_values = conc_time_curve.values.tolist()
        simulation_times = conc_time_curve.index.tolist()

        AUC_all_yaxis = np.array(simulation_values)
        AUC_all_xaxis = np.array(simulation_times)
        AUC_all = np.trapz(y=AUC_all_yaxis, x=AUC_all_xaxis)

        AUC_eff = 0
        for i in start_end_list:
            test_xaxis = conc_time_curve.index.tolist()
            test_yaxis = conc_time_curve.values.tolist()

            start_index = test_xaxis.index(i[0])
            stop_index = test_xaxis.index(i[1])

            AUC_eff_xaxis = test_xaxis[start_index:stop_index+1]
            AUC_eff_yaxis = test_yaxis[start_index:stop_index+1]

            AUC_eff_without_threshold = np.trapz(y=AUC_eff_yaxis,
                                                x=AUC_eff_xaxis
                                                )
            AUC_eff_under_threshold = np.trapz(y=[ORRES_min]*len(AUC_eff_yaxis),
                                                x=AUC_eff_xaxis
                                                )

            AUC_eff += (AUC_eff_without_threshold - AUC_eff_under_threshold)

        placeholder_dict = {}
        placeholder_dict[EXTRT] = {}
        placeholder_dict[EXTRT]['EXDOSE'] = EXDOSE
        placeholder_dict[EXTRT][TESTCD] = AUC_all
        EXDOSE_TESTCD_list.append(placeholder_dict)

        """plot the single Dose-Response curve"""
        # VisualisationDesign.plotSingleDoseResponse(colour_plot_dict)



    if dict_visualisation.get('graph') == True:
        """conversion r to V

        convert the radius to the volume unit for better understandung of the
        cell system
        """
        convert_r_to_V = ['r','r_os','r_b','R_ref']
        ODE_RESULTS_columns = ODE_RESULTS.columns.tolist()
        for column_name in ODE_RESULTS_columns:
            if column_name in convert_r_to_V:
                ODE_RESULTS[column_name] = (4/3) * np.pi * ODE_RESULTS[column_name]**3

                """"rename the column name

                change the first letter to 'V' and append then the rest of the
                old word string to this
                """
                new_column_name = 'V' + column_name[1:]
                ODE_RESULTS.rename(columns={column_name:new_column_name},
                                    inplace=True
                                    )
                """adapt the PDORRESU dict to the new units"""
                PDORRESU[new_column_name] = PDORRESU.pop(column_name)
                PDORRESU[new_column_name] = 'fL'


        if USUBJID == 'combined_models':
            try:
                ODE_RESULTS['Hog1PPn'] = ODE_RESULTS['Hog1PPn'] * 1E7
                # ODE_RESULTS['Cl_in'] = ODE_RESULTS['Cl_in'] / 10
            except:
                pass

        """group the keys by their units"""
        PDORRESU_grouped = {}
        for key, value in sorted(PDORRESU.items()):
            PDORRESU_grouped.setdefault(value, []).append(key)

        """some design condition for the bachelor plots"""
        if sql_USUBJID == 'volume':
            ODE_RESULTS = pd.DataFrame(ODE_RESULTS['V']) 
            PDORRESU_grouped = {'total volume [fL]':['V']}
    
        """plot the time series"""
        VisualisationDesign.plotTimeSeries(TimeSeriesData_df=ODE_RESULTS,
                                            SubplotLogic=PDORRESU_grouped)



    """visualize each single model"""
    if dict_visualisation.get('each_single_model') is True\
    and sql_USUBJID == 'combined_models':

        """list of model subsets

        create a list of each subsets models of the combined_models
        """
        str_single_models = ['ion','volume','hog']

        for model_name in str_single_models:
            """open the file which contains the name of the ODE variables"""
            exec(open('Single_Models/{0}/{0}.py'.format(model_name),
                                                    encoding="utf-8").read())

            """list of the names of the variables in the model"""
            list_of_var_keys = list(eval('{}_init_values'.format(
                                                            model_name)).keys())

            """we must remove V_os,
            because in the combined model it is not an ODE
            """
            if model_name == 'hog':
                list_of_var_keys.remove('V_os')

            plotting_part_of_dataframe = ODE_RESULTS[list_of_var_keys]

            # TEMP: Arbeitsloesung; noch kein Code um Plots nach Groessenordnungen
            #       aufzuteilen
            if model_name == 'volume':
                plotting_part_of_dataframe=plotting_part_of_dataframe.drop(columns=['pi_t', 'c_i'])

            if model_name == 'hog':
                plotting_part_of_dataframe=plotting_part_of_dataframe.drop(columns=['Glyc_in'])

            # TODO:
            """visualize process

            ==> generalize it as a def function
            give the function either a dataframe or a list of dataframe
            """
            sns.set_style(style = 'whitegrid')
            sns.set_context(context = 'notebook')

            plt.figure(figsize=(11.69, 8.27))
            plt.plot(plotting_part_of_dataframe)

            ax = plt.axes()
            ax.set_xlim()

            ax.set_xlabel("time [s]")
            ax.set_ylabel("Model")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.yaxis.grid(
                linewidth=0.5,
                color="black",
                alpha=0.3)

            plt.tick_params(
                which='both',
                right='off',
                top='off')

            plt.legend(
                labels=plotting_part_of_dataframe.columns.tolist(),
                loc='best',
                fontsize=11)

            """saving subset plot
            
            saves the each plot in a file.
            """
            save_fig = dict_system_switch.get('save_figures')

            if save_fig[0] == True:
                
                plt.savefig('/Users/janpiotraschke/Bilder_Simulation/combined_{0}_SEQ{1}_{2}.png'.format(
                    model_name, sql_SEQ_list[0], current_date),
                    dpi=360,
                    format=save_fig[1],
                    bbox_inches='tight')


if dict_visualisation.get('dose_response') == True:

    """split the results by the used EXTRT"""
    split_ET_list = [[] for x in range(len(used_EXTRT_list))]

    for i in range(len(used_EXTRT_list)):
        for j in EXDOSE_TESTCD_list:
            if used_EXTRT_list[i] in j.keys():
                j[used_EXTRT_list[i]]["{} stimulus".format(used_EXTRT_list[i])] \
                                            = j[used_EXTRT_list[i]].pop(TESTCD)
                # j[used_EXTRT_list[i]]["{}-{}".format(used_EXTRT_list[i], TESTCD)] \
                #     = j[used_EXTRT_list[i]].pop(TESTCD)
                split_ET_list[i].append(j[used_EXTRT_list[i]])

    """final version of dose-response

    the two paragraphs above are suboptimal. the next paragraph sorts the
    response of TESTCD under the different stimulus types and saves that in a
    list. alternative to list, you can also choose the dict data structure.
    ==> EXTRT_sorted
    """
    EXTRT_sorted = []
    for dicts in split_ET_list:
        super_dict = defaultdict(list)
        for d in dicts:
            for k, v in d.items():
                super_dict[k].append(v)
        EXTRT_sorted.append(super_dict)


    """create each Dataframe and than merge them together

    advantage: the initial simulation stimulus time must not be th
    e same
    if N.A. --> values are None in the final DataFrame
    """
    df_list = []
    for i in EXTRT_sorted:
        index = i['EXDOSE']
        i.pop('EXDOSE',None)
        df_list.append(pd.DataFrame(i, index=index))

    EXDOSE_TESTCD_df = df_list[0]
    for i in range(len(df_list)-1):
        EXDOSE_TESTCD_df = pd.concat(objs = [EXDOSE_TESTCD_df,df_list[i+1]],
                                    axis = 1,
                                    sort = True
                                    )
    """df to latex

    df.to_latex()
    copy the printed text to latex to visualize the dataframe there
    """
    if dict_system_switch.get('df_to_latex') == True:
        print(EXDOSE_TESTCD_df.to_latex())

    """plot the whole Dose-Response curve"""
    VisualisationDesign.plotDoseResponse(EXDOSE_TESTCD_df=EXDOSE_TESTCD_df,
                                        xscale='log')
