# # NOTE: update database
# cur.execute("UPDATE yeast_ref.bachelor_dummie SET orres='0.0006' WHERE testcd='Hog1n' AND co='min';")
#
# G = nx.DiGraph()
#
# G.add_node("ROOT")
#
# for i in range(5):
#     G.add_node("Child_%i" % i)
#     G.add_node("Grandchild_%i" % i)
#     G.add_node("Greatgrandchild_%i" % i)
#
#     G.add_edge("ROOT", "Child_%i" % i)
#     G.add_edge("Child_%i" % i, "Grandchild_%i" % i)
#     G.add_edge("Grandchild_%i" % i, "Greatgrandchild_%i" % i)
#
# # write dot file to use with graphviz
# # run "dot -Tpng test.dot >test.png"
# write_dot(G,'test.dot')
#
# # same layout using matplotlib with no labels
# plt.title('draw_networkx')
# pos =graphviz_layout(G, prog='dot')
# nx.draw(G, pos, with_labels=False, arrows=True)
# plt.savefig('nx_test.png')



# with open('csv_datafiles/{0}/PD.csv'.format(name),\
#             'w', newline='') as csvfile:
#
#     # fieldnames gibt die Ordnung an, mit welcher die Header abfolgen
#     # extrasaction: ignore all dict.key which should not be in the headers
#     writer = csv.DictWriter(csvfile, fieldnames=PD_column_names, extrasaction='ignore')
#     writer.writeheader()
#     writer.writerows(toCSV)


# if dict_system_switch.get('create_csv') == True:
#     conn = psycopg2.connect(host='localhost', dbname='simulation_results',\
#                             user='janpiotraschke')
#
#     # open a cursor to perform database operations
#     cur = conn.cursor()
#     cur.execute("Select * FROM combined_models.pd;")
#     PD_column_names = [desc[0] for desc in cur.description]
#
#     print(len(running_chit))
#
#     for dict_running_chit in running_chit:
#
#         # make the dict keys as new variables
#         locals().update(dict_running_chit)
#
#         if name == 'combined_models':
#             pd_to_dict = dict_running_chit['results'].to_dict('index')
#             toCSV=[]
#             for DTC,inner_dict in pd_to_dict.items():
#                 for substance,value in inner_dict.items():
#
#                     dict_test = {}
#                     dict_test['studyid'] = STUDYID
#                     dict_test['domain'] = 'pd'
#                     dict_test['usubjid'] = name
#                     dict_test['pdseq'] = SEQ
#                     dict_test['pdtestcd'] = substance
#                     dict_test['pdtest'] = None
#                     dict_test['pdorres'] = value
#                     dict_test['pdorresu'] = dict_running_chit['units']['{}'.format(substance)]
#                     dict_test['pddtc'] = DTC
#                     dict_test['co'] = "pddtc in Sekunden"
#
#                     keys_db = tuple(dict_test.keys())
#                     values_db = tuple(dict_test.values())
#
#                     """dict to sql database"""
#                     insert_statement = 'insert into combined_models.pd (%s) values %s'
#                     cur.execute(cur.mogrify(insert_statement, (AsIs(','.join(keys_db)), tuple(values_db))))
#
#                     conn.commit()
#
#         else:
#             # TEMP: not finished
#             # TODO: the fusion of the two dicts is not correct yet
#             # to csv file
#             # first: prepare the dataframe to a list of dicts
#             pd_to_dict = dict_running_chit['results'].to_dict('index')
#             toCSV=[]
#
#             index_num = 1
#             for index,inner_dict in pd_to_dict.items():
#                 for substance,value in inner_dict.items():
#                     dict_test = {}
#                     #dict_test['index'] = index_num
#                     dict_test['time_points'] = index
#                     dict_test['value'] = value
#                     dict_test['substance'] = substance
#                     dict_test['units'] = dict_running_chit['units']['{}'.format(substance)]
#                     dict_test['stimulus'] = EXDOSE
#                     dict_test['stimulustype'] = EXTRT
#                     #dict_test.update(dict_running_chit)
#                     index_num += 1
#                     toCSV.append(dict_test)
#
#
#             headers=['time_points','value','substance','units',
#                     'stimulus', 'stimulustype']
#
#             csv_fingerprint = '{}_{}mM_{}s'.format(EXTRT, EXDOSE, \
#                                                 EXSTDTC)
#             # print(toCSV[:2])
#             with open('csv_datafiles/{0}/{0}:{1}.csv'.format(name,csv_fingerprint),\
#                         'w', newline='') as csvfile:
#                 # fieldnames gibt die Ordnung an, mit welcher die Header abfolgen
#                 # restval specifies the value to be written if ...
#                 # the dictionary is missing a key in fieldnames
#                 # extrasaction: ignore all dict.key which should not be in the headers
#                 writer = csv.DictWriter(csvfile, fieldnames=headers, restval='None', \
#                                         extrasaction='ignore')
#                 writer.writeheader()
#                 writer.writerows(toCSV)
#
#         # cur.close()
#         # conn.close()
#
#         """export data to PostgreSQL Database"""
#         if dict_system_switch.get('export_data_to_sql') == True:
#
#             # conn = psycopg2.connect(host='localhost', dbname='simulation_results',\
#             #                         user='janpiotraschke')
#             #
#             # # open a cursor to perform database operations
#             # cur = conn.cursor()
#
#             if name == 'combined_models':
#                 pass
#             #     with open('csv_datafiles/{}/PD.csv'.format(name), 'r') as f:
#             #
#             #         # skip the .csv headers
#             #         next(f)
#             #
#             #         """function of copy_from()
#             #
#             #         Read data from the file-like object file
#             #         >>appending<< them to the table named table.
#             #         """
#             #         cur.copy_from(f,'combined_models.pd', sep=',')
#             #
#             #     conn.commit()
#
#
#             else:
#                 # TEMP: bad way --> better: compare and append if equal
#                 try:
#                     cur.execute(sql.SQL("DROP TABLE {}.{};").format(\
#                                 sql.Identifier(name),sql.Identifier(csv_fingerprint)))
#                 except:
#                     pass
#
#                 conn.commit()
#
#                 cur.execute(sql.SQL("""
#                     CREATE TABLE {}.{}(
#                         time_points double precision,
#                         value double precision,
#                         substance text,
#                         units text,
#                         stimulus integer,
#                         stimulustype text,
#                         PRIMARY KEY (time_points, substance)
#                     )
#                     """).format(sql.Identifier(name),sql.Identifier(csv_fingerprint)))
#
#                 conn.commit()
#
#                 # load the csv file into the database file
#                 with open('csv_datafiles/{0}/{0}:{1}.csv'.format(name,\
#                             csv_fingerprint), 'r') as f:
#                     next(f)
#                     # copy_from(file, table, sep='\t', null='\\N', size=8192, columns=None)
#
#                     # upper case letters must be in double quotes
#                     cur.copy_from(f, '{}."{}"'.format(name, csv_fingerprint), sep=',')
#
#                 # When commit is called, the PostgreSQL engine will run all the queries at once.
#                 conn.commit()
#
#     cur.close()
#     conn.close()

# if len(dict_visualisation.get('special_interest')) > 0:
#     examine_subst = dict_visualisation.get('special_interest')[0]
#     # if examine_subst == 'r':
#     convert_r_to_V = ['r','r_os','r_b','R_ref']
#     # examine_behaviour_df = pd.DataFrame()
#     examine_dict = {}
#     for dict_running_chit in running_chit:
#         results, name, unit, EXTRT, EXDOSE, EXSTDTC \
#         = x.prepare_analysis_running_chit(dict_running_chit=dict_running_chit)
#
#         if EXSTDTC not in examine_dict:
#             examine_dict[EXSTDTC] = pd.DataFrame()
#
#         if examine_subst in convert_r_to_V:
#             examine_dict[EXSTDTC]['{}/{}mM'.format(EXTRT,\
#                                 EXDOSE)] = (4/3) * np.pi * results[examine_subst]**3
#         elif examine_subst == 'Hog1PPn':
#             examine_dict[EXSTDTC]['{}/{}mM'.format(EXTRT,\
#                                 EXDOSE)] = results[examine_subst]*1000
#         else:
#             examine_dict[EXSTDTC]['{}/{}mM'.format(EXTRT,\
#                                 EXDOSE)] = results[examine_subst]
#
#     # TEMP: not good but it works
#     for key,values in examine_dict.items():
#         sns.set_style('whitegrid')
#         sns.set_context('notebook')
#         fig = plt.figure(figsize=(10,7.5))
#         ax1 = fig.add_subplot(1, 1, 1)
#         ax1.spines["top"].set_visible(False)
#         ax1.spines["right"].set_visible(False)
#         ax1.set_xlabel("time [s]",fontsize=12)
#         # ax1.set_ylabel('membrane potential [V]')
#         ax1.set_ylabel('Total volume [fL]',fontsize=12)
#         # ax1.set_ylabel('concentration [uM]')
#
#
#         fig.autofmt_xdate(bottom=0.2, rotation=30)
#         fig.suptitle(t='{}_Model - cell volume'.format(name.title()),fontsize = 12)
#         # make the fig more fittet
#         fig.tight_layout(pad=3,rect=[0,0,0.85,1])
#
#         # to show the version of the plot
#         fig.text(0.99, 0.01,
#                 s='{} - {}_Model'.format(current_date, name.title()),
#                 fontstyle='italic',
#                 color='#999999',
#                 ha='right',
#                 va='bottom',
#                 fontsize='x-small'
#                 )
#         # TEMP: notloesung --> manuel --> schrecklich
#         labels_names = ['NaCl-100mM','NaCl-200mM','NaCl-300mM','NaCl-500mM']
#
#         plt.plot(values)
#         ax1.legend(labels_names,ncol=1,borderaxespad = 0,bbox_to_anchor=(1.01, 0.5), \
#                     frameon = True,loc='center left',fontsize=12)
#         # exec('ax{0}.plot(results[i],label=i)'.format(axis_index))
#         # exec('ax{0}.legend(ncol=1,borderaxespad = 0,bbox_to_anchor=(1.01, 0.5), \
#         #     frameon = True,loc={1!r})'.format(axis_index,'center left'))
#
#         save_fig = dict_visualisation.get('save_figures')
#         plt.savefig('Pictures/{0}_examine.{1}'.format(name, save_fig[1]),
#                     dpi = 1200,
#                     format = save_fig[1],
#                     bbox_inches='tight'
#                     )
#         plt.show()
#         plt.clf()
#         plt.close()

#     """
#     Visualisiert nach den Methoden, die True geschaltet sind. Benoetigt eine
#     Liste mit Panda DataFrame als Input.
#     """
#     # TEMP: does not work
#     # IDEA: heatmap für verhaeltnisberechnung zw. substanzen berechnen
#     #       --> fuer visualiserung fuer menschen
#     if dict_visualisation.get('heat_map') is True:
#
#         plt.style.use('ggplot')
#         cmap = sns.diverging_palette(220, 10, as_cmap=True)
#         sns.heatmap(data, cmap=cmap,vmax=1,
#                     square=True, linewidths=.5, cbar_kws={"shrink": .5})
#         plt.savefig('heat_map.png', dpi = 1200, format = 'png')
#         plt.figure(figsize=(12,9))
#         result = plt.show()
