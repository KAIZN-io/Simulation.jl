exec(open("SYSTEM/py_packages.py").read())

conn = psycopg2.connect(host='localhost', dbname='simulation_results')
cur = conn.cursor()

ThresholdTime = 40

cur.execute("""
    SELECT pdtestcd, pdorres
    FROM combined_models.pd
    WHERE pddtc = %s AND pdseq = 65;
    """, [ThresholdTime])

# print(cur.fetchall())

"""find out what the specific model is made of"""
InvestigateModel = 'hog'
cur.execute(sql.SQL("""
    SELECT DISTINCT(testcd)
    FROM {}.init_values;
    """).format(sql.Identifier(InvestigateModel)))

ReferenceModelSubstances = [] 
for i in cur.fetchall():
    ReferenceModelSubstances.append(i[0])

"""
we must remove V_os, because in the combined model it is not an ODE
"""
if InvestigateModel == 'hog':
    ReferenceModelSubstances.remove('V_os')

# TODO : get the values at the time 40 s a design with that the new models init values with a new seq

cur.close()
conn.close()
