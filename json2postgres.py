exec(open("SYSTEM/py_packages.py").read())

def pushJsonToPostgresql(json_file = {}):
    conn = psycopg2.connect(host='localhost', dbname='simulation_results')
    cur = conn.cursor()

    """create the table for the model versions"""
    try:
        cur.execute(sql.SQL("""
            CREATE TABLE {}.json(
                seq serial PRIMARY KEY,
                model_version json 
            );
            """).format(sql.Identifier(model_name)))
    except:
        pass
    conn.commit()

    """prepare the json file for the upload"""
    test = str(json_file)
    test = test.replace("'", '"')

    """upload the json file"""
    insert_statement = 'insert into '+model_name+'.json(model_version) values (%s)'
    cur.execute(insert_statement, [test])

    conn.commit()

    cur.close()
    conn.close()

model_name = 'combined_models'

"""get the data for the system from the json file"""
with open('Single_Models/json_files/{0}_system.json'.format(model_name)) as json_data:
    data_from_json = json.load(json_data)

pushJsonToPostgresql(json_file=data_from_json)

# conn = psycopg2.connect(host='localhost', dbname='simulation_results')
# cur = conn.cursor()

# cur.execute(sql.SQL("""
#     SELECT model_version 
#     FROM {}.json
#     WHERE seq = 1;
#     """).format(sql.Identifier(model_name)))

# print("\n",type(cur.fetchone()[0]))

# cur.close()
# conn.close()


