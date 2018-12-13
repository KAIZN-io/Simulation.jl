# NOTE: import the standard used packages
exec(open("SYSTEM/py_packages.py").read())

hog_eq_units = {
                'NaCl' : 'mM',
                'V_cell' : 'fL',
                'V_cyt' :  'fL',
                'V_nuc' : 'fL',
                'V_ratio' : 'fL',
                'PI_e' : 'Pa',
                'PI_t' : 'Pa',
                'PI_i' : 'Pa',
                'n_totalHog1' :'amol',
                'totalHog1PP' : 'dimensionless'
                }

combined_models_eq_units = {
                            'V_cell' : 'fL',
                            'G' : '(um)^2',
                            'V_cyt' : 'fL',
                            'V_nuc' : 'fL',
                            'V_os' : 'fL',
                            'V_ref' : 'fL',
                            'V_ratio' : 'fL',
                            'A_Ar' : 'J mol^-1' ,
                            'J_H' : 'mol m^-2 s^-1',
                            'J_K' :'mol m^-2 s^-1' ,
                            'J_Na' : 'mol m^-2 s^-1',
                            'J_Cl' :'mol m^-2 s^-1',
                            'Na_indt' : 'mM s^-1',
                            'Cl_indt' : 'mM s^-1',
                            'K_indt' : 'mM s^-1',
                            'H_indt' : 'mM s^-1',
                            'Na_outdt' : 'mM s^-1',
                            'Cl_outdt' : 'mM s^-1',
                            'K_outdt' : 'mM s^-1',
                            'H_outdt' : 'mM s^-1',
                            'c_e' : 'mM',
                            'pi_e' : 'Pa',
                            'pi_i' : 'Pa',
                            'R_ref' : 'um',
                            'R_refdt' : 'um',
                            'r_osdt' : 'um',
                            'r_bdt' : 'um',
                            'rdt' : 'um',
                            'n_totalHog1' :'amol',
                            'totalHog1PP' : 'dimensionless'
                            }

ion_eq_units = {
                'A_Ar' : 'J mol^-1' ,
                'J_H' : 'mol m^-2 s^-1',
                'J_K' :'mol m^-2 s^-1' ,
                'J_Na' : 'mol m^-2 s^-1',
                'J_Cl' :'mol m^-2 s^-1'
                }

volume_eq_units = {
                    'V' : 'fL',
                    'pi_i' : 'Pa',
                    'V_ref' : 'fL',
                    'G' : '(um)^2',
                    'R_ref' : 'um',
                    'R_refdt' : 'um',
                    'r_osdt' : 'um',
                    'r_bdt' : 'um',
                    'rdt' : 'um',
                    }

cwd = os.getcwd()

TEST_substance = 'Hog1n'
USUBJID = 'Yeast_BSc'

# model_name = 'combined_models'
# NOTE: only for term analysis between ion and combined_models
interested_source = ['ion','combined_models']
# interested_source = [model_name]

"""chose the right data from the databank"""

conn = psycopg2.connect(host='localhost', dbname='simulation_results')
engine = create_engine('postgres://janpiotraschke:@localhost:5432/simulation_results', echo=False)

# models_to_analyse = {}
# for model in interested_source:
#     models_to_analyse[model] = {}
#
#     # open a cursor to perform database operations
#     source_option = [model, '{}_terms'.format(model)]
#
#     available_fingerprint = []
#     for i in source_option:
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = %s;",[i])
#
#         # get a list of column names from the psycopg2 cursor :
#         col_names = [desc[0] for desc in cur.description]
#
#         query_info = cur.fetchall()
#         query_info = [list(element) for element in query_info]
#
#         cur.close()
#
#         info_dataframe = pd.DataFrame(query_info, columns = col_names)
#         table_names = list(set(info_dataframe['table_name']))
#
#         available_fingerprint.append(table_names)
#
#     table_name_list = list(set(available_fingerprint[0]) & set(available_fingerprint[1]))
#
#     for choosen_table in table_name_list:
#
#         df = pd.read_sql_table(table_name=choosen_table, con=engine, schema=model)
#
#         df = df.sort_index()
#         columns_from_sql = df.columns.tolist()
#         test_query = df.values.tolist()
#
#         units = {}
#         for i in test_query:
#             units[i[2]] = i[3]
#
#         # sort it in a dict
#         all_dict = {}
#         for i in test_query:
#             if i[2] in all_dict:
#                 all_dict[i[2]].append(i)
#             else:
#                 all_dict[i[2]] = [i]
#
#         dataframe_dict = {}
#
#         for key, values in all_dict.items():
#             dataframe_column_list = [x[1] for x in values]
#
#             dataframe_index_list = [x[0] for x in values]
#             dataframe_dict[values[0][2]] = dataframe_column_list
#
#         df_from_db = pd.DataFrame(dataframe_dict,index=dataframe_index_list)
#
#         dict_running_chit = {}
#         dict_running_chit['name'] = list(all_dict.values())[0][0][-1]
#         dict_running_chit['results'] = df_from_db
#         dict_running_chit['units'] = units
#
#
#         # get the patial terms from the database
#         cur = conn.cursor()
#
#         cur.execute(sql.SQL("SELECT * FROM {}.{};").format(\
#                     sql.Identifier('{}_terms'.format(model)),sql.Identifier(choosen_table)))
#
#         col_names_pat = [desc[0] for desc in cur.description]
#         test_info = cur.fetchall()
#         cur.close()
#
#         test_info = [list(element) for element in test_info]
#
#         pat_dataframe = pd.DataFrame(test_info, columns = col_names_pat)
#
#         pat_dataframe = pat_dataframe.set_index('index')
#         pat_dataframe = pat_dataframe.sort_index()
#         pat_dataframe = pat_dataframe[~pat_dataframe.index.duplicated(keep='first')]
#
#         models_to_analyse[model]['all_terms'] = pat_dataframe
#
#         df = pat_dataframe
#
#         # get reference data from json file:
#         with open('{0}/Single_Models/json_files/{1}_system.json'.format(cwd, model)) as json_data:
#             data_from_json = json.load(json_data)
#
#         add_up_dict = {}
#         eq_pat_list = []
#         for i,k in data_from_json['equation'].items():
#             for j in k.values():
#                 eq_pat_list.append(j.keys())
#
#                 # how to add up the multiple columns from the dataframe
#                 add_up_dict[i] = list(j.keys())
#
#         eq_pat_list = [j for i in eq_pat_list for j in i]
#
#         # pandas dataframe with the equations parts
#         df_eq_pat = df[eq_pat_list]
#
#         df_eq = pd.DataFrame()
#         for i,j in add_up_dict.items():
#             for k in j:
#                 if i not in df_eq:
#                     df_eq[i] = df_eq_pat[k]
#                 else:
#                     df_eq[i] += df_eq_pat[k]
#
#
#         # pandas dataframe with the odes term parts
#         df_ode_terms = df.drop(columns = eq_pat_list)
#
#         # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#         # create .csv file with equation simulation_results for data exchange
#         eq_toCSV = []
#         for time_points,row in df_eq.iterrows():
#
#             for substance,value in row.iteritems():
#                 dict_toCSV = {}
#
#                 dict_toCSV['time_points'] = time_points
#                 dict_toCSV['value'] = value
#                 dict_toCSV['substance'] = substance
#                 dict_toCSV['units'] = eval(("{}_eq_units").format(model))[substance]
#
#                 eq_toCSV.append(dict_toCSV)
#
#         headers=['time_points','value','substance','units']
#
#         time_length = int(df_eq.index[-1])
#
#         csv_eq_fingerprint = '{}_{}s'.format('equation', time_length)
#
#         with open('csv_datafiles/{0}/{0}:{1}.csv'.format(model,csv_eq_fingerprint),\
#                     'w', newline='') as csvfile:
#             """
#             fieldnames gibt die Ordnung an, mit welcher die Header abfolgen
#             restval specifies the value to be written if ...
#             the dictionary is missing a key in fieldnames
#             extrasaction: ignore all dict.key which should not be in the headers
#             """
#
#             writer = csv.DictWriter(csvfile, fieldnames=headers, restval='None', \
#                                     extrasaction='ignore')
#             writer.writeheader()
#             writer.writerows(eq_toCSV)
#
#         # TODO: create network from .json file
#         equation_dict = {}
#         for key,value_system in data_from_json.items():
#             if key == 'copa':
#                 pass
#             else:
#                 for nodes,value in value_system.items():
#                     for key2,components in value['component'].items():
#                         if nodes not in equation_dict:
#                             equation_dict[nodes] = components
#                         else:
#                             equation_dict[nodes] += components
#
#         # get all the variables of the system
#         var_elements_raw = list(equation_dict.keys())
#         var_elements = []
#         for i in var_elements_raw:
#             if i[0] == 'd':
#                 var_elements.append(i[1:])
#             else:
#                 var_elements.append(i)
#
#         # drop the event equation NaCl from the hog model
#         equation_dict.pop('NaCl', None)
#
#         # TODO: funktioniert noch nicht richtig
#         # Grund: PI_t0 wird als Element von PI_t angesehen
#         # IDEA: Abstand zwischen den Variablenseparatoren +,-,*,/ einbauen
#
#         edges_list = []
#         for variable in var_elements:
#             for substance, substance_equation in equation_dict.items():
#                 if variable in substance_equation:
#                     edges_list.append((variable,substance))
#             # print(variable, '-->', substance_equation, '-->', substance)
#
#     models_to_analyse[model]['ODE_results'] = dict_running_chit['results']
#     models_to_analyse[model]['ODE_terms_results'] = df_ode_terms
#     models_to_analyse[model]['algebraic_equation_results'] = df_eq
#     models_to_analyse[model]['algebraic_equation_terms_results'] = df_eq_pat
#
# conn.close()


# TODO: find the terms which are not correlating
# NOTE: get the json _terms of the ion model
# get the data for the system from the json file
with open('{0}/Single_Models/json_files/ion_system.json'.format(cwd)) as json_data:
    data_from_json_ion = json.load(json_data)

# the terms in the ion model
model_terms_ion = []
term_overview_dict = {}
for key,value_system in data_from_json_ion.items():
    if key == 'copa':
        for key2, value2 in value_system.items():
            pass
    else:
        for keys,value in value_system.items():
            for key2,value2 in value['component'].items():
                term_overview_dict[key2] = value2
                model_terms_ion.append(key2)

if interested_source == ['ion','combined_models']:

    ion_df = models_to_analyse['ion']['all_terms']

    combined_term_names = ['patA_Ar1', 'patJ_H1', 'patJ_H2', 'patJ_H3', 'patJ_H4', 'patJ_H5', 'patJ_H6', 'patJ_K1', \
                            'patJ_K2', 'patJ_K3', 'patJ_Na1', 'patJ_Na2', 'patJ_Na3', 'patJ_Cl1', 'patJ_Cl2', 'patJ_Cl3', \
                            'patL_ArH1', 'patL_ArH2', 'patL_HH1', 'patL_HH2', 'patATP1', 'patATP2', 'patDeltaphi2', \
                            'patH_in1', 'patCl_in1', 'patCl_out1', 'patH_out1', 'patK_in1', 'patK_out1', 'patNa_in1', 'patNa_out1']
    combined_df = models_to_analyse['combined_models']['all_terms'][combined_term_names]

    rename_combined_df = {'patH_in1':'patH_in2',
                        'patK_in1':'patK_in2',
                        'patNa_in1':'patNa_in2',
                        'patCl_in1':'patCl_in2'
                            }

    combined_df = combined_df.rename(columns=rename_combined_df)

    placeholder_for_test = ion_df.columns.tolist()

    term_corr_dict = {}
    for term in ion_df.columns.tolist():
        term_corr_dict[term] = ion_df[term].corr(combined_df[term], method='pearson')

    for i,j in term_corr_dict.items():
        if j <= 0.8:
            pass
            # print('Korrelation von', i ,' = ',term_overview_dict[i] ,' =>', j)



conn = psycopg2.connect(host='localhost', dbname='simulation_results')
# open a cursor to perform database operations
cur = conn.cursor()

#create a new schema (=new model)
schema_name = "pp_combined_models"
try:
    #cur.execute("CREATE SCHEMA test;")
    cur.execute(sql.SQL("CREATE SCHEMA {};").format(sql.Identifier(schema_name)))

except:
    pass

conn.commit()

# alter a existing sql table
new_column_name = 'SEQ'
try:
    cur.execute(sql.SQL("ALTER TABLE pp_combined_models.parameter ADD {} integer;").format(sql.Identifier(new_column_name)))
except:
    pass

conn.commit()
# # TEMP: bad way --> better: compare and append if equal
# try:
#     cur.execute(sql.SQL("DROP TABLE {}.{};").format(\
#                 sql.Identifier(schema_name),sql.Identifier(csv_fingerprint)))
# except:
#     pass
#
# conn.commit()
#

# NOTE: try it in SDTM format (CO = comment)
# try:
#     cur.execute(sql.SQL("""
#         CREATE TABLE {}.{}(
#             "DTC" double precision,
#             "TEST" text,
#             "ORRES" double precision,
#             "ORRESU" text,
#             "CO" text,
#             PRIMARY KEY ("DTC", "TEST")
#         )
#         """).format(sql.Identifier(schema_name),sql.Identifier("bachelor_dummie")))
#
# except:
#     pass

# NOTE: create finding tables
try:
    cur.execute(sql.SQL("""
        CREATE TABLE {}.{}(
            "DOMAIN" text,
            "USUBJID" text,
            "SEQ" text,
            "GRPID" text,
            "TESTCD" text,
            "TEST" text,
            "CAT" text,
            "ORRES" double precision,
            "ORRESU" text,
            PRIMARY KEY ("USUBJID", "SEQ", "TESTCD")
        )
        """).format(sql.Identifier(schema_name),sql.Identifier("parameter")))

except:
    pass
# try:
#     cur.execute(sql.SQL("""
#         CREATE TABLE {}.{}(
#             DOMAIN text,
#             USUBJID text,
#             SEQ text,
#             GRPID text,
#             TESTCD text,
#             TEST text,
#             CAT text,
#             ORRES numeric,
#             ORRESU text,
#             PRIMARY KEY (USUBJID, SEQ)
#         )
#         """).format(sql.Identifier(schema_name),sql.Identifier("parameter")))
#
# except:
#     pass
conn.commit()

SEQ = 1

# EX_dict = {
#             "DOMAIN" : "EX",
#             "USUBJID" : USUBJID,
#             "EXSEQ" : SEQ,
#             "EXCAT" : "Salz",
#             "EXTRT" : ,
#             "EXDOSE" : ,
#             "EXDOSU" : "mM",
#             "EXSTDTC" : ,
#             "CO" : "EXSTDTC in Sekunden",
#             }

PP_dict = {
            "DOMAIN" : ["PP"]*4,
            "USUBJID" : [USUBJID]*4,
            "SEQ" : [SEQ]*4,
            "GRPID" : [None]*4,
            "TESTCD" : ["TMAX", "CMAX", "AUCEFF", "AUCALL"],
            "TEST" : ["Time of CMAX", "Max Conc", "AUC effective", "AUC all"],
            "CAT" : [TEST_substance]*4,
            "ORRES" : ['%.5f'%(Tmax), '%.5f'%(Cmax), '%.5f'%(AUC_eff), '%.5f'%(AUC_all)],
            "ORRESU" : ["s", "mM", "s*mM", "s*mM"],
            }

PP_df = pd.DataFrame(PP_dict, index=range(len(PP_dict["DOMAIN"])))
engine = create_engine('postgres://janpiotraschke:@localhost:5432/simulation_results', echo=False)

# TODO: dont delete the existing values but dont simply append all into the database
PP_df.to_sql(name='parameter', index=False, con=engine, schema='pp_combined_models', if_exists='replace')

# NOTE: update database

# keys_db = tuple(PP_dict.keys())
# values_db = tuple(PP_dict.values())

# NOTE: dict to sql database
# try:
# insert_statement = 'insert into pp_combined_models.parameter (%s) values %s'
# cur.execute(cur.mogrify(insert_statement, (AsIs(','.join(keys_db)), tuple(values_db))))
# except:
#     pass

# conn.commit()

cur.close()
conn.close()






row = 10
ion_schablone = ion_df.columns.tolist()
# for test_substance in ion_schablone:
#     print(test_substance)
#     print(combined_df[test_substance].iloc[row])
#     print(ion_df[test_substance].iloc[row])

# T = 303.15,
# R = 8.314
# L_HCl = 1.298 * 1e-9
# Cl_in = 0.545
# Cl_out = 0.1 * 1126
# a_log = np.log(Cl_in/Cl_out)
# # a_test = R*T*(L_HCl*np.log(Cl_in/Cl_out))

# xyz = 'patJ_H3'
# plt.plot(ion_df[xyz])
# plt.plot(combined_df[xyz])
# plt.plot(ion_df)
# # plt.plot(combined_df)
# plt.show()

# NOTE: for calculation of correlation, the values must have the same timestamps!
# new scale
x_axis = models_to_analyse[model]['ODE_results'].index.tolist()

interp_dict = {
                'ODE_terms_results' : models_to_analyse[model]['ODE_terms_results'],
                'algebraic_equation_results' : models_to_analyse[model]['algebraic_equation_results']
                }

# old scale
change_this_time_skala = interp_dict['ODE_terms_results'].index.tolist()

preprocessed_dict = {}
for results_type,df_results in interp_dict.items():

    pre_placeholder_dict = {}
    for column_name in df_results:
        # old scale
        old_species_value = df_results[column_name].tolist()
        new_species_value = interp1d(change_this_time_skala,old_species_value)(x_axis)
        pre_placeholder_dict[column_name] = new_species_value

    preprocessed_dict[results_type] = pre_placeholder_dict

algeb_preprocessed_df = pd.DataFrame(preprocessed_dict['algebraic_equation_results'], index=x_axis)
ODE_term_preprocessed_df = pd.DataFrame(preprocessed_dict['ODE_terms_results'], index=x_axis)


# TODO: calculate the correlation between the effected substance and his affector

ergebnislist = []
corr_matrix_df = []
for x in algeb_preprocessed_df:
    probelist = []
    for y in ODE_term_preprocessed_df:
        probelist.append(algeb_preprocessed_df[x].corr(ODE_term_preprocessed_df[y],method='pearson'))

    ergebnislist.append(probelist)
