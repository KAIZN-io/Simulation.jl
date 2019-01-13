exec(open("SYSTEM/py_packages.py").read())


TargetModel = 'hog'
vonWoherIchdieDatenhole = 'combined_models'

conn = psycopg2.connect(host='localhost', dbname='simulation_results')
cur = conn.cursor()

"""get the MAX(seq) value from the database"""
# cur.execute(sql.SQL("""
#                 SELECT MAX(seq)
#                 FROM {}.init_values;
#                 """).format(sql.Identifier(TargetModel)))

# SeqToWorkWith = cur.fetchone()[0]
SeqToWorkWith = 5
"""find out what the target model is made of"""
cur.execute(sql.SQL("""
    SELECT DISTINCT(testcd)
    FROM {}.init_values;
    """).format(sql.Identifier(TargetModel)))

TargetModelSubstance = []
for i in cur.fetchall():
    TargetModelSubstance.append(i[0])

"""
get the simulation results of the 
ODE Simulation No. 53 at the specific time point
"""

ThresholdTime = 20
cur.execute("""
    SELECT pdtestcd, pdorres
    FROM combined_models.pd
    WHERE pddtc = %s AND pdseq = 53;
    """, [ThresholdTime])

"""create the corresponding dict for this query"""
OdeSolutionAtTimepoint_dict = {}
for i in cur.fetchall():
    OdeSolutionAtTimepoint_dict[i[0]] = i[1]


if TargetModel == 'hog':
    OdeSolutionAtTimepoint_dict['V_os'] = 4/3 * \
        np.pi * OdeSolutionAtTimepoint_dict['r_os'] ** 3


# TODO: create 4 new possible ODE states --> now i only make number 2
"""
1. all values at timepoint 20s
2. only all values from the substance of the hog model
3. only all values from the substance of the volume model
4. only all values from the substance of the ion model
"""
# print(OdeSolutionAtTimepoint_dict)
Comment = 'changed again again' 
for TESTCD,ORRES in OdeSolutionAtTimepoint_dict.items():
    if TESTCD in TargetModelSubstance:
        cur.execute(sql.SQL("""
            UPDATE {}.init_values
            SET orres = %s, co = %s
            WHERE testcd = %s AND seq = %s;
            """).format(sql.Identifier(TargetModel)), [ORRES, Comment,TESTCD, SeqToWorkWith])
        conn.commit()

cur.close()
conn.close()
