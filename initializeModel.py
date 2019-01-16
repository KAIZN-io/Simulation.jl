"""this script initialize a model in the database"""

exec(open("SYSTEM/py_packages.py").read())


def createJsonModel(NameOfModel=''):

    system_comp = ['copa', 'equation', 'ODE']
    dict_system = {}

    system_comp_remove = []


    """pre-check whether the system_comp exists for the specific model"""
    for system in system_comp:
        if os.path.isfile('Single_Models/{0}/{0}_{1}.txt'.format(NameOfModel, system)) == False:
            system_comp_remove.append(system)
    for i in system_comp_remove:
        system_comp.remove(i)

    cur.execute(sql.SQL("""
        SELECT testcd, orresu 
        FROM {0}.orresu_equations;
        """).format(sql.Identifier(NameOfModel)))

    ORRESU_column_names = [desc[0] for desc in cur.description]

    """the values from the sql database in a dict"""
    ORRESU_dict = {}
    for i in cur.fetchall():
        ORRESU_dict[i[ORRESU_column_names.index(
            'testcd')]] = i[ORRESU_column_names.index('orresu')]

    for system in system_comp:
        """opens the .txt file"""
        f = open('Single_Models/{0}/{0}_{1}.txt'.format(NameOfModel, system))

        string_list = [line for line in f]

        dict_spec = {}

        if system == 'copa':
            for string_line in range(len(string_list)):
                key = string_list[string_line][string_list[string_line].find(
                    ""):string_list[string_line].find("=")].strip()
                value = string_list[string_line][string_list[string_line].find(
                    "=")+1:string_list[string_line].find("\n")]
                dict_spec[key] = value

            dict_system[system] = dict_spec

        else:
            dict_system[system] = dict_spec
            for string_line in range(len(string_list)):

                """.strip() removes leading and ending whitespaces"""
                key = string_list[string_line][string_list[string_line].find(
                    ""):string_list[string_line].find("=")].strip()
                value = string_list[string_line][string_list[string_line].find(
                    "=")+1:string_list[string_line].find("\n")]

                """split the value string"""
                dict_spec[key] = {}
                dict_spec[key]['component'] = {}
                splitted = value.split()

                """step 1 : "dont touch that"""
                parenthese_open = 0
                parenthese_close = 0
                join_str_list = []
                join_if = []

                beginning = -1
                ending = -1
                for j, i in enumerate(splitted):
                    if '(' in i:
                        parenthese_open += i.count('(')

                        if beginning < 0:
                            beginning = j

                    if ')' in i:
                        parenthese_close += i.count(')')

                        if (parenthese_open == parenthese_close) and parenthese_open > 0:

                            ending = j
                            join_str_list.append([beginning, ending])

                            beginning = -1
                            ending = -1
                            parenthese_open = 0
                            parenthese_close = 0

                    if ('if' in i) and len(i) == 2:
                        """get the string position of the if condition beginning"""
                        join_if.append(j)

                for k in join_if:
                    # print(splitted[k::])

                    dict_spec[key]['condition'] = ' '.join(splitted[k::])
                    del splitted[k::]

                """invert the list iteration --> then join the pieces together"""
                for i in join_str_list[::-1]:
                    a = ''.join(splitted[i[0]:i[1]+1])

                    del splitted[i[0]:i[1]+1]
                    splitted.insert(i[0], a)

                """step 2 : create the "component" for the variable"""
                join_marker = [0]

                term_separator = ['+', '-']
                for i, j in enumerate(splitted):
                    if j in term_separator:
                        join_marker.append(i)

                join_marker.insert(len(join_marker), len(splitted))

                dict_spec[key]['component'] = {}

                """next step: remove the differential d"""
                if key[0] == 'd':
                    key_surrogate = key[1:]
                else:
                    key_surrogate = key

                for i in range(len(join_marker)-1):
                    a = ''.join(splitted[join_marker[i]:join_marker[i+1]])
                    dict_spec[key]['component']['pat{}{}'.format(
                        key_surrogate, i+1)] = a

                """gibe the unit of the substance the dict"""
                dict_spec[key]['unit'] = ORRESU_dict[key_surrogate]

                """last step: remove keys without values --> remove zombies"""
                keys_to_delete = []
                for remove_key, value in dict_spec[key]['component'].items():
                    if value == "":
                        keys_to_delete.append(remove_key)
                for remove_key in keys_to_delete:
                    dict_spec[key]['component'].pop(remove_key, None)

    if NameOfModel == 'hog':

        hog_stimulus = {}
        hog_stimulus['copa'] = dict_system['copa']
        hog_stimulus['equation'] = {}
        hog_stimulus['equation']['NaCl'] = {'component': {
            'patNaCl1': "(0 if t < t0 else single_impuls_NaCl) if signal_type == 1 else ((single_impuls_NaCl if (t0 <= t and t < (t0 + t1)) else 0) if signal_type == 2 else ((single_impuls_NaCl if ((t - t0 - math.floor((t - t0) / (t1 + t2)) * (t1 + t2)) <= t1) else 0) if signal_type == 3 else ((max_NaCl if (0 if t < t0 else single_impuls_NaCl * math.ceil((t - t0) / t1)) > max_NaCl else (0 if t < t0 else single_impuls_NaCl * math.ceil((t - t0) / t1))) if signal_type == 4 else 0)))"}}
        hog_stimulus['equation']['NaCl']['unit'] = ORRESU_dict['NaCl']
        hog_stimulus['ODE'] = dict_system['ODE']

        for key, value in dict_system['equation'].items():
            hog_stimulus['equation'][key] = value

        dict_system = hog_stimulus

    """create json format.."""
    JsonModel = json.dumps(dict_system, indent=4)

    return JsonModel

conn = psycopg2.connect(
    host='db_postgres',
    user='postgres',
    dbname='simulation_results'
)

cur = conn.cursor()

allModels_list = ['ion', 'hog', 'volume', 'combined_models']

for NameOfModel in allModels_list:

    """check if the model is already initialize"""
    cur.execute("Select max(seq) From {0}.init_values".format(NameOfModel))

    if cur.fetchone()[0] == None:
        """read the model file"""
        exec(open('Single_Models/{0}/{0}.py'.format(NameOfModel), encoding="utf-8").read())
        ODEVar_dict = eval('{}_init_values'.format(NameOfModel))
        Parameter_dict = eval('{}_parameter'.format(NameOfModel))

        """initialize seq"""
        SEQ = 1

        """parameter to database"""
        for i,j in Parameter_dict.items():

            cur.execute(sql.SQL("""
                    INSERT INTO {0}.parameter(
            	        seq, testcd, orres, orresu)
                        VALUES(%s, %s, %s, %s);
                    """).format(sql.Identifier(NameOfModel)),[SEQ, i, j[0], j[1]])

            conn.commit()

        """initial values to database"""
        for i in ODEVar_dict.values():

            cur.execute(sql.SQL("""
                    INSERT INTO {0}.init_values(
            	        seq, testcd, orres, orresu)
                        VALUES(%s, %s, %s, %s);
                    """).format(sql.Identifier(NameOfModel)),[SEQ, i[1], i[0], i[2]])
     
            conn.commit()

        """get the units of the equations"""
        exec(open('Single_Models/{0}/{0}_orresu_dict.py'.format(NameOfModel), encoding="utf-8").read())
        ORRESU_dict = eval('{}_orresu_dict'.format(NameOfModel))

        for i in ORRESU_dict.values():

            cur.execute(sql.SQL("""
                    INSERT INTO {}.orresu_equations(
                        testcd, orresu)
                        VALUES (%s, %s);
                    """).format(sql.Identifier(NameOfModel)),[i[0], i[1]])
     
            conn.commit()

        """create the JSON model and push it into the database"""
        ModelInJsonFormat = createJsonModel(NameOfModel=NameOfModel)

        cur.execute(sql.SQL("""
                INSERT INTO {}.json(
                    seq, model_version)
	                VALUES(%s, %s);
                """).format(sql.Identifier(NameOfModel)), [SEQ, ModelInJsonFormat])

        conn.commit()


cur.close()
conn.close()