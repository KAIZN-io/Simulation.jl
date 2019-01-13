exec(open("SYSTEM/py_packages.py").read())

"""clarification --> data entry staff

the data entry / sorting to sql should be the only humanly touch for the
system
"""


conn = psycopg2.connect(host='localhost', dbname='simulation_results')
cur = conn.cursor()


# allModels_list = ['ion','hog', 'volume', 'combined_models']
allModels_list = ['combined_models']



for model in allModels_list:
    """create initial values table"""
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

    """create parameter table"""
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
            """).format(sql.Identifier(model), sql.Identifier("parameter")))
    except:
        pass

    conn.commit()

    """initial values to database"""
    try:
        exec(open('Single_Models/{0}/{0}.py'.format(model), encoding="utf-8").read())
        ODEVar_dict = eval('{}_init_values'.format(model))
        Parameter_dict = eval('{}_parameter'.format(model))

        """check, how many SEQ number already exists"""
        cur.execute(sql.SQL("SELECT MAX(seq) FROM {}.parameter;").format(
                    sql.Identifier(model)))

        SEQ_old = cur.fetchone()[0]
        if SEQ_old == None:
            SEQ_old = 0

        """SEQ for new simulation"""
        SEQ = SEQ_old + 1

        for i,j in Parameter_dict.items():
            ParameterValues2Sql_dict = {}
            ParameterValues2Sql_dict['seq'] = SEQ
            ParameterValues2Sql_dict['testcd'] = i
            ParameterValues2Sql_dict['orres'] = j[0]
            ParameterValues2Sql_dict['orresu'] = j[1]

            """update database"""
            keys_db = tuple(ParameterValues2Sql_dict.keys())
            values_db = tuple(ParameterValues2Sql_dict.values())

            """dict to sql database"""
            try:
                insert_statement = 'insert into {}.parameter (%s) values %s'.format(
                    model)
                cur.execute(cur.mogrify(insert_statement,
                                        (AsIs(','.join(keys_db)), tuple(values_db))))
            except:
                pass

            conn.commit()

        """check, how many SEQ number already exists"""
        cur.execute(sql.SQL("SELECT MAX(seq) FROM {}.init_values;").format(
                    sql.Identifier(model)))

        SEQ_old = cur.fetchone()[0]
        if SEQ_old == None:
            SEQ_old = 0

        """SEQ for new simulation"""
        SEQ = SEQ_old + 1

        for i in ODEVar_dict.values():
            InitValues2Sql_dict = {}
            InitValues2Sql_dict['seq'] = SEQ
            InitValues2Sql_dict['testcd'] = i[1]
            InitValues2Sql_dict['orres'] = i[0]
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