"""this script creates the database storage structure"""

exec(open("SYSTEM/py_packages.py").read())

conn = psycopg2.connect(
    host='db_postgres',
    user='postgres',
    dbname='simulation_results'
)

cur = conn.cursor()

allModels_list = ['ion', 'hog', 'volume', 'combined_models']


NameOfModel_list = ['test5']

for NameOfModel in NameOfModel_list:

    """check if the model structure is already created"""
    cur.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name = %s;
            """, [NameOfModel])

    if (len(cur.fetchall())>0) == False:

        """create model terms schema"""
        cur.execute(sql.SQL("""
                CREATE SCHEMA {0}
                    AUTHORIZATION postgres;
                """).format(sql.Identifier(NameOfModel+'_terms')))

        conn.commit()

        """create schema"""
        cur.execute(sql.SQL("""
                CREATE SCHEMA {0}
                    AUTHORIZATION postgres;
                """).format(sql.Identifier(NameOfModel)))

        conn.commit()




        """create json table"""
        cur.execute(sql.SQL("""
                CREATE TABLE {0}.json
                (
                    seq serial,
                    model_version json,
                    adding_changes json,
                    deleting_changes json,
                    CONSTRAINT json_pkey PRIMARY KEY(seq)
                )
                WITH(
                    OIDS=FALSE
                )
                TABLESPACE pg_default;
                """).format(sql.Identifier(NameOfModel)))

        conn.commit()

        """create ex table"""
        cur.execute(sql.SQL("""
                CREATE TABLE {0}.ex
                (
                    studyid text COLLATE pg_catalog."default",
                    domain text COLLATE pg_catalog."default",
                    usubjid text COLLATE pg_catalog."default" NOT NULL,
                    exseq integer NOT NULL,
                    excat text COLLATE pg_catalog."default",
                    extrt text COLLATE pg_catalog."default" NOT NULL,
                    exdose real,
                    exdosu text COLLATE pg_catalog."default",
                    exstdtc_array double precision[],
                    simulation_start double precision,
                    simulation_stop double precision,
                    co text COLLATE pg_catalog."default",
                    modelversion integer,
                    initvaluesversion integer,
                    CONSTRAINT ex_pkey PRIMARY KEY(usubjid, exseq, extrt)
                )
                WITH(
                    OIDS=FALSE
                )
                TABLESPACE pg_default;
                """).format(sql.Identifier(NameOfModel)))

        conn.commit()

        """create pd table"""
        cur.execute(sql.SQL("""
                CREATE TABLE {0}.pd
                (
                    studyid text COLLATE pg_catalog."default",
                    domain text COLLATE pg_catalog."default",
                    usubjid text COLLATE pg_catalog."default" NOT NULL,
                    pdseq integer NOT NULL,
                    pdtestcd text COLLATE pg_catalog."default" NOT NULL,
                    pdtest text COLLATE pg_catalog."default",
                    pdorres double precision,
                    pdorresu text COLLATE pg_catalog."default",
                    pddtc double precision NOT NULL,
                    co text COLLATE pg_catalog."default",
                    CONSTRAINT pd_pkey PRIMARY KEY(usubjid, pdseq, pdtestcd, pddtc)
                )
                WITH(
                    OIDS=FALSE
                )
                TABLESPACE pg_default;
                """).format(sql.Identifier(NameOfModel)))

        conn.commit()


        cur.execute(sql.SQL("""
                CREATE TABLE {0}.init_values
                (
                    seq integer NOT NULL,
                    testcd text COLLATE pg_catalog."default" NOT NULL,
                    test text COLLATE pg_catalog."default",
                    orres double precision,
                    orresu text COLLATE pg_catalog."default",
                    co text COLLATE pg_catalog."default",
                    CONSTRAINT init_values_pkey PRIMARY KEY (seq, testcd)
                )
                WITH (
                    OIDS = FALSE
                )
                TABLESPACE pg_default;
                """).format(sql.Identifier(NameOfModel)))

        conn.commit()


        cur.execute(sql.SQL("""
                CREATE TABLE {0}.parameter
                (
                    seq integer NOT NULL,
                    testcd text COLLATE pg_catalog."default" NOT NULL,
                    test text COLLATE pg_catalog."default",
                    orres double precision,
                    orresu text COLLATE pg_catalog."default",
                    co text COLLATE pg_catalog."default",
                    CONSTRAINT parameter_pkey PRIMARY KEY (seq, testcd)
                )
                WITH (
                    OIDS = FALSE
                )
                TABLESPACE pg_default;
                """).format(sql.Identifier(NameOfModel)))

        conn.commit()

        cur.execute(sql.SQL("""
                CREATE TABLE {0}.orresu_equations
                (
                    testcd text COLLATE pg_catalog."default" NOT NULL,
                    test text COLLATE pg_catalog."default",
                    orresu text COLLATE pg_catalog."default",
                    CONSTRAINT orresu_equations_pkey PRIMARY KEY (testcd)
                )
                WITH (
                    OIDS = FALSE
                )
                TABLESPACE pg_default;
                """).format(sql.Identifier(NameOfModel)))

        conn.commit()



cur.close()
conn.close()



