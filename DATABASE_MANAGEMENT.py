exec(open("SYSTEM/py_packages.py").read())


time_stamp = datetime.now().strftime("%Y-%m-%dT%H:%M")

# NOTE: creates the db reference_bib
try:
    conn = psycopg2.connect(host='localhost', dbname='postgres',\
                            user='janpiotraschke')
    dbname = "reference_bib"
    cur = conn.cursor()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(dbname)))
    cur.close()
    conn.close()

except:
    pass

dict_to_sql = {
                'DTC' : time_stamp,
                'TESTCD' : 'r',
                'TEST' : 'radius',
                'ORRES' : 5,
                'ORRESU' : 'um',
                'CO' : 'max'
                }

# dict_to_sql = {
#                 'DTC' : time_stamp,
#                 'TESTCD' : 'Hog1n',
#                 'TEST' : 'Hog1n',
#                 'ORRES' : 0.0006,
#                 'ORRESU' : 'mM',
#                 'CO' : 'min'
#                 }
# dict_to_sql = {
#                 'DTC' : time_stamp,
#                 'TESTCD' : 'Hog1n',
#                 'TEST' : 'Hog1n',
#                 'ORRES' : 0.2918 * 1e-1,
#                 'ORRESU' : 'mM',
#                 'CO' : 'max'
#                 }


# dict_to_sql = {
#                 'DTC' : time_stamp,
#                 'TESTCD' : 'r',
#                 'TEST' : 'radius',
#                 'ORRES' : 1.2,
#                 'ORRESU' : 'um',
#                 'CO' : 'min'
#                 }
statistic_data = dict_to_sql

conn = psycopg2.connect(host='localhost', dbname='reference_bib',\
                        user='janpiotraschke')
# open a cursor to perform database operations
cur = conn.cursor()

#create a new schema (=new modelsystem)
schema_name = "yeast_ref"
try:
    #cur.execute("CREATE SCHEMA test;")
    cur.execute(sql.SQL("CREATE SCHEMA {};").format(sql.Identifier(schema_name)))

except:
    pass

conn.commit()

"""try it in SDTM format (CO = comment)"""
try:
    cur.execute(sql.SQL("""
        CREATE TABLE {}.{}(
            "dtc" text,
            "testcd" text,
            "test" text,
            "orres" double precision,
            "orresu" text,
            "co" text,
            PRIMARY KEY ("dtc", "test", "co")
        )
        """).format(sql.Identifier(schema_name),sql.Identifier("bachelor_dummie")))

except:
    pass
conn.commit()

keys_db = tuple(statistic_data.keys())
values_db = tuple(statistic_data.values())

# NOTE: dict to sql database

insert_statement = 'insert into yeast_ref.bachelor_dummie (%s) values %s'
cur.execute(cur.mogrify(insert_statement, (AsIs(','.join(keys_db)), tuple(values_db))))

conn.commit()

"""create tables with the infos above the variables / parameters"""
conn = psycopg2.connect(host='localhost', dbname='postgres',
                        user='janpiotraschke')
cur = conn.cursor()

SystemName = 'ion'

try:
    cur.execute(sql.SQL("""
        CREATE TABLE {}.{}(
            "dtc" text,
            "testcd" text,
            "test" text,
            "orres" double precision,
            "orresu" text,
            "co" text,
            PRIMARY KEY ("dtc", "test", "co")
        )
        """).format(sql.Identifier(schema_name), sql.Identifier("init_values")))
# [0.1231 * 1e-3, 'Pbs2', 'mM', 'original/hog_model']
except:
    pass
conn.commit()

cur.close()
conn.close()
# exec(open('{0}/Single_Models/{1}/{1}.py'.format(cwd,
#                                                 model_name), encoding="utf-8").read())

# """list of the names of the variables in the model"""
# list_of_var_keys = eval('{}_init_values'.format(model_name)).keys()
