exec(open("SYSTEM/py_packages.py").read())

"""clarification --> data entry staff

the data entry / sorting to sql should be the only humanly touch for the
system
"""


# time_stamp = datetime.now().strftime("%Y-%m-%dT%H:%M")

# # NOTE: creates the db reference_bib
# try:
#     conn = psycopg2.connect(host='localhost', dbname='postgres')
#     dbname = "reference_bib"
#     cur = conn.cursor()
#     conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#     cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(dbname)))
#     cur.close()
#     conn.close()

# except:
#     pass

# dict_to_sql = {
#                 'DTC' : time_stamp,
#                 'TESTCD' : 'r',
#                 'TEST' : 'radius',
#                 'ORRES' : 5,
#                 'ORRESU' : 'um',
#                 'CO' : 'max'
#                 }

# # dict_to_sql = {
# #                 'DTC' : time_stamp,
# #                 'TESTCD' : 'Hog1n',
# #                 'TEST' : 'Hog1n',
# #                 'ORRES' : 0.0006,
# #                 'ORRESU' : 'mM',
# #                 'CO' : 'min'
# #                 }
# # dict_to_sql = {
# #                 'DTC' : time_stamp,
# #                 'TESTCD' : 'Hog1n',
# #                 'TEST' : 'Hog1n',
# #                 'ORRES' : 0.2918 * 1e-1,
# #                 'ORRESU' : 'mM',
# #                 'CO' : 'max'
# #                 }


# # dict_to_sql = {
# #                 'DTC' : time_stamp,
# #                 'TESTCD' : 'r',
# #                 'TEST' : 'radius',
# #                 'ORRES' : 1.2,
# #                 'ORRESU' : 'um',
# #                 'CO' : 'min'
# #                 }
# statistic_data = dict_to_sql

# conn = psycopg2.connect(host='localhost', dbname='reference_bib')
# # open a cursor to perform database operations
# cur = conn.cursor()

# #create a new schema (=new modelsystem)
# schema_name = "yeast_ref"
# try:
#     #cur.execute("CREATE SCHEMA test;")
#     cur.execute(sql.SQL("CREATE SCHEMA {};").format(sql.Identifier(schema_name)))

# except:
#     pass

# conn.commit()

# """try it in SDTM format (CO = comment)"""
# try:
#     cur.execute(sql.SQL("""
#         CREATE TABLE {}.{}(
#             "dtc" text,
#             "testcd" text,
#             "test" text,
#             "orres" double precision,
#             "orresu" text,
#             "co" text,
#             PRIMARY KEY ("dtc", "test", "co")
#         )
#         """).format(sql.Identifier(schema_name),sql.Identifier("bachelor_dummie")))

# except:
#     pass
# conn.commit()

# keys_db = tuple(statistic_data.keys())
# values_db = tuple(statistic_data.values())

# # NOTE: dict to sql database
# try:
#     insert_statement = 'insert into yeast_ref.bachelor_dummie (%s) values %s'
#     cur.execute(cur.mogrify(insert_statement, (AsIs(','.join(keys_db)), tuple(values_db))))
# except:
#     pass
# conn.commit()

# """create tables with the infos above the variables / parameters"""
# conn = psycopg2.connect(host='localhost', dbname='postgres')
# cur = conn.cursor()

# SystemName = 'ion'

# try:
#     cur.execute(sql.SQL("""
#         CREATE TABLE {}.{}(
#             "dtc" text,
#             "testcd" text,
#             "test" text,
#             "orres" double precision,
#             "orresu" text,
#             "co" text,
#             PRIMARY KEY ("dtc", "test", "co")
#         )
#         """).format(sql.Identifier(schema_name), sql.Identifier("init_values")))
# # [0.1231 * 1e-3, 'Pbs2', 'mM', 'original/hog_model']
# except:
#     pass
# conn.commit()


# # exec(open('{0}/Single_Models/{1}/{1}.py'.format(cwd,
# #                                                 model_name), encoding="utf-8").read())

# # """list of the names of the variables in the model"""
# # list_of_var_keys = eval('{}_init_values'.format(model_name)).keys()

conn = psycopg2.connect(host='localhost', dbname='simulation_results')
cur = conn.cursor()
allModels_list = ['ion', 'dummie', 'hog', 'volume', 'combined_models']

"""create init values sql table"""
for model in allModels_list:
    try:
        cur.execute(sql.SQL("""
            CREATE TABLE {}.{}(
                "seq" integer,
                "testcd" text,
                "test" text,
                "orres" double precision,
                "orresu" text,
                "co" text,
                PRIMARY KEY ("seq", "testcd")
            )
            """).format(sql.Identifier(model), sql.Identifier("init_values")))
    except:
        pass

    conn.commit()

    try:
        exec(open('Single_Models/{0}/{0}.py'.format(model), encoding="utf-8").read())
        ODEVar_dict = eval('{}_init_values'.format(model))

        for i in ODEVar_dict.values():
            InitValues2Sql_dict = {}
            InitValues2Sql_dict['seq'] = str(1)
            InitValues2Sql_dict['testcd'] = i[1]
            InitValues2Sql_dict['orres'] = str(i[0])
            InitValues2Sql_dict['orresu'] = i[2]

            """not always are there comments for the substance given"""
            try:
                InitValues2Sql_dict['co'] = i[3]
            except:
                pass

            """update database"""
            keys_db = tuple(InitValues2Sql_dict.keys())
            values_db = tuple(InitValues2Sql_dict.values())

            """dict to sql database"""
            try:
                insert_statement = 'insert into {}.init_values (%s) values %s'.format(model)
                cur.execute(cur.mogrify(insert_statement, (AsIs(','.join(keys_db)), tuple(values_db))))
            except:
                pass

            conn.commit()
    except:
        pass

"""create units sql table"""
for model in allModels_list:
    try:
        cur.execute(sql.SQL("""
            CREATE TABLE {}.{}(
                "testcd" text,
                "test" text,
                "orresu" text,
                PRIMARY KEY ("testcd")
            )
            """).format(sql.Identifier(model), sql.Identifier("orresu_equations")))
    except:
        pass

    conn.commit()

    try:      
        """get all the units""" 
        exec(open('Single_Models/{0}/{0}_orresu_dict.py'.format(model), encoding="utf-8").read())

        ORRESU_dict = {}
        ORRESU_dict = eval('{}_orresu_dict'.format(model))

        for i in ORRESU_dict.values():
            Orresu2Sql_dict = {}
            Orresu2Sql_dict['testcd'] = i[0]
            Orresu2Sql_dict['orresu'] = i[1]

            """update database"""
            keys_db = tuple(Orresu2Sql_dict.keys())
            values_db = tuple(Orresu2Sql_dict.values())

            """dict to sql database"""
            try:
                insert_statement = 'insert into {}.orresu_equations (%s) values %s'.format(
                    model)
                cur.execute(cur.mogrify(insert_statement, (AsIs(','.join(keys_db)), tuple(values_db))))
            except:
                pass

            conn.commit()
    except:
        pass

cur.close()
conn.close()

