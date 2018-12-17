exec(open("SYSTEM/py_packages.py").read())

"""

cur.execute("INSERT INTO product(store_id, url, price, charecteristics, color, dimensions) VALUES (%s, %s, %s, %s, %s, %s)",
            (1,  'http://www.google.com', '$20', json.dumps(thedictionary), 'red', '8.5x11'))
That will solve your problem. However, you really should be storing keys and values in their own separate columns. To retrieve the dictionary, do:

cur.execute('select charecteristics from product where store_id = 1')
dictionary = json.loads(cur.fetchone()[0])
Hope it helps.
"""




model_name = 'ion'

"""get the data for the system from the json file"""
with open('Single_Models/json_files/{0}_system.json'.format(model_name)) as json_data:
    data_from_json = json.load(json_data)


conn = psycopg2.connect(host='localhost', dbname='simulation_results')
cur = conn.cursor()

test= str({"customer": "John Doe", "items": {"product": "Beer", "qty": 6}})

try:
    cur.execute(sql.SQL("""
        CREATE TABLE {}.json(
            SEQ serial NOT NULL PRIMARY KEY,
            info json NOT NULL
        );
        """).format(sql.Identifier(model_name)))
except:
    pass
conn.commit()

DataFromJson_str = str(data_from_json).replace("'", '"')

insert_statement = "insert into ion.json(info) (%s);"
# insert_statement = 'insert into {}.init_values (%s) values %s'.format(model)
cur.execute(insert_statement, [DataFromJson_str])
# print(insert_statement) 
# cur.execute(insert_statement)
conn.commit()
# cur.execute(sql.SQL("""
#     INSERT INTO ion.json(info)
#     VALUES ({});
#     """).format(sql.Identifier(test)))
# conn.commit()

# cur.execute("""INSERT INTO ion.json(info)
# VALUES
# (
#     '{ "customer": "John Doe", "items": {"product": "Beer","qty": 6}}'
# );""")
# conn.commit()

cur.execute("""
    SELECT
    info -> 'items' -> 'qty' AS qty
    FROM
    ion.json;
    """)
print(cur.fetchall())

cur.close()
conn.close()
