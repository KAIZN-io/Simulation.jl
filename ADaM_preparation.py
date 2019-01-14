__author__ = 'Jan N. Piotraschke'
__email__ = 'jan.piotraschke@mail.de'
__version__ = 'bachelor_thesis'
__license__ = 'private'

# import the standard used packages
exec(open("SYSTEM/py_packages.py").read())

from argparse import Namespace

def compareModels(ModelsToCompare_list = [], TestSubstance = '', ModelSeq={}):
    """get the data"""
    conn = psycopg2.connect(host='localhost', dbname='simulation_results')
    """host name taken from docker-compose.yml"""
    # conn = psycopg2.connect(
    #     host='db_postgres',
    #     user='postgres',
    #     dbname='simulation_results'
    # )
    """open a cursor to perform database operations"""
    cur = conn.cursor()
    
    PD_df_dict = {}
    for i in ModelsToCompare_list:

        cur.execute(sql.SQL("""
            SELECT pdorres, pddtc 
            FROM {}.pd 
            WHERE pdseq=%s AND pdtestcd=%s
            ORDER BY pddtc;
            """).format(sql.Identifier(i)), [ModelSeq[i], TestSubstance])
    
        values_list = []
        PD_df_index = []
        for j in cur.fetchall():
            values_list.append(j[0])
            PD_df_index.append(j[1])
        PD_df_dict[i] = values_list

    """create the ODE_RESULTS DataFrame"""
    ODE_RESULTS = pd.DataFrame(PD_df_dict, index=PD_df_index)

    return ODE_RESULTS

    
    

def getDatafromSQL(sql_STUDYID = '', sql_USUBJID = '', sql_SEQ_list = []):
    conn = psycopg2.connect(host='localhost', dbname='simulation_results')
    """host name taken from docker-compose.yml"""
    # conn = psycopg2.connect(
    #     host='db_postgres',
    #     user='postgres',
    #     dbname='simulation_results'
    # )
    """open a cursor to perform database operations"""
    cur = conn.cursor()

    dict_running_chit = {}

    """iterate over a list which contains the wanted SEQ keys"""
    for SEQ in sql_SEQ_list:

        """get the used TRT row"""
        cur.execute(sql.SQL("""
            SELECT * 
            FROM {}.ex 
            WHERE exseq=%s;
            """).format(sql.Identifier(sql_USUBJID)),[SEQ])

        EX_column_names = [desc[0] for desc in cur.description]
        EX_data = cur.fetchall()[0]

        EX_dict = {EX_column_names[index]:EX_data[index] for index in range(len(EX_data))}

        """get all TESTCD names from the database"""
        cur.execute(sql.SQL("""
            SELECT DISTINCT(pdtestcd) 
            FROM {}.pd 
            WHERE pdseq=%s;
            """).format(sql.Identifier(sql_USUBJID)),[SEQ])

        TESTCD_list = [x[0] for x in cur.fetchall()]

        PD_df_dict = {}

        """iterate with each TESTCD"""
        for TESTCD_iterator in TESTCD_list:
            cur.execute(sql.SQL("""
                SELECT pdorres, pddtc 
                FROM {}.pd 
                WHERE pdseq=%s AND pdtestcd=%s
                ORDER BY pddtc;
                """).format(sql.Identifier(sql_USUBJID)),[SEQ,TESTCD_iterator])

            PD_column_names = [desc[0] for desc in cur.description]

            """the values from the sql database"""
            ORRES_list = []
            PD_df_index = []
            for i in cur.fetchall():
                ORRES_list.append(i[PD_column_names.index('pdorres')])
                PD_df_index.append(i[PD_column_names.index('pddtc')])

            PD_df_dict[TESTCD_iterator] = ORRES_list

        """create the ODE_RESULTS DataFrame"""
        ODE_RESULTS = pd.DataFrame(PD_df_dict,index=PD_df_index)

        dict_running_chit[SEQ] = {}

        """get the ORRESU for each TESTCD"""
        cur.execute(sql.SQL("""
            SELECT DISTINCT pdtestcd, pdorresu 
            FROM {}.pd 
            WHERE pdseq=%s;
            """).format(sql.Identifier(sql_USUBJID)),[SEQ])

        TESTCD_ORRESU_tuple = cur.fetchall()

        PDORRESU_dict = {}
        for i in TESTCD_ORRESU_tuple:
            PDORRESU_dict[i[0]] = i[1]

        dict_running_chit[SEQ]['USUBJID'] = sql_USUBJID
        dict_running_chit[SEQ]['SEQ'] = SEQ
        dict_running_chit[SEQ]['EXCAT'] = EX_dict['excat']
        dict_running_chit[SEQ]['EXTRT'] = EX_dict['extrt']
        dict_running_chit[SEQ]['EXDOSE'] = EX_dict['exdose']
        dict_running_chit[SEQ]['EXDOSU'] = EX_dict['exdosu']
        dict_running_chit[SEQ]['EXSTDTC'] = EX_dict['exstdtc_array']
        dict_running_chit[SEQ]['ODE_RESULTS'] = ODE_RESULTS
        dict_running_chit[SEQ]['PDORRESU'] = PDORRESU_dict

    cur.close()
    conn.close()

    return dict_running_chit


def getEquationTermsformSQL(sql_USUBJID='', SqlQueryTerms_list=[]):
    
    conn = psycopg2.connect(host='localhost', dbname='simulation_results')
    """host name taken from docker-compose.yml"""
    # conn = psycopg2.connect(
    #     host='db_postgres',
    #     user='postgres',
    #     dbname='simulation_results'
    # )

    sql_USUBJID = sql_USUBJID+'_terms'
    Query = 'SELECT index, ' + ','.join(SqlQueryTerms_list) +' FROM {}."51";'

    cur = conn.cursor()
    cur.execute(sql.SQL(Query).format(sql.Identifier(sql_USUBJID)))
    TermsColumnName_list = [desc[0] for desc in cur.description]

    QueryTermsData_df = pd.DataFrame(cur.fetchall(), 
                                    columns=TermsColumnName_list)

    """Set the DataFrame index using one existing column"""
    QueryTermsData_df.set_index('index', inplace=True)
    
    cur.close()
    conn.close()

    # todo: overgive the ADaM.py a Pandas DataFrame with the results

    return QueryTermsData_df

def create_ADaM_csv(RUN_SEQ = {}):
    """turn the dict keys to variables in the def area"""
    n = Namespace(**RUN_SEQ)

    ADaM_column_names = ['USUBJID', 'SEQ', 'EXCAT', 'EXTRT', 'EXDOSE',
                        'EXDOSU', 'EXSTDTC', 'PDTESTCD', 'PDORRES',
                        'PDORRESU', 'PDDTC']
    pd_to_dict = RUN_SEQ['ODE_RESULTS'].to_dict('index')


    toCSV=[]
    for DTC,inner_dict in pd_to_dict.items():
        for PDTESTCD,PDORRES in inner_dict.items():

            dict_test = {}
            dict_test['USUBJID'] = n.USUBJID
            dict_test['SEQ'] = n.SEQ
            dict_test['EXCAT'] = n.EXCAT
            dict_test['EXTRT'] = n.EXTRT
            dict_test['EXDOSE'] = n.EXDOSE
            dict_test['EXDOSU'] = n.EXDOSU
            dict_test['EXSTDTC'] = n.EXSTDTC
            dict_test['PDTESTCD'] = PDTESTCD
            dict_test['PDORRES'] = PDORRES
            dict_test['PDORRESU'] = RUN_SEQ['PDORRESU'][PDTESTCD]
            dict_test['PDDTC'] = DTC
            toCSV.append(dict_test)

    with open('csv_datafiles/{0}/ADaM.csv'.format(n.USUBJID),\
                'w', newline='') as csvfile:

        # fieldnames gibt die Ordnung an, mit welcher die Header abfolgen
        # extrasaction: ignore all dict.key which should not be in the headers
        writer = csv.DictWriter(csvfile, fieldnames=ADaM_column_names, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(toCSV)

