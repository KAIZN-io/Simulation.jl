exec(open("SYSTEM/py_packages.py").read())

conn = psycopg2.connect(host='localhost', dbname='simulation_results')
cur = conn.cursor()

cur.execute("""
    Select * 
    From combined_models.init_values
    Where seq = 4;
    """)

dataFromQuery = cur.fetchall()
ColumnNames = [i[0] for i in cur.description]

knockOutTerm = 'c_i'
dataFromQuery = [i for i in dataFromQuery if i[1] != knockOutTerm]

"""find out the max represented seq in the database"""
cur.execute("""Select Max(seq) From combined_models.init_values""")
MaxSeq = cur.fetchone()[0]

NewSeq = MaxSeq + 1

"""tuple to list"""
dataFromQuery = [list(i) for i in dataFromQuery]

"""update seq number"""
for n, i in enumerate(dataFromQuery):
    dataFromQuery[n][0] = NewSeq

for i in dataFromQuery:

    insert_statement = 'insert into combined_models.init_values(%s) values %s'
    cur.execute(cur.mogrify(insert_statement,
                            (AsIs(','.join(ColumnNames)), tuple(i))))

    conn.commit()
