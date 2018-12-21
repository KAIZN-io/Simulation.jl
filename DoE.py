exec(open("SYSTEM/py_packages.py").read())

TargetModel = 'combined_models'
InvestigateModel = 'hog'

conn = psycopg2.connect(host='localhost', dbname='simulation_results')
cur = conn.cursor()

"""get the MAX(seq) value from the database"""
cur.execute(sql.SQL("""
                SELECT MAX(seq)
                FROM {}.init_values;
                """).format(sql.Identifier(TargetModel)))

SeqToWorkWith = cur.fetchone()[0]

"""find out what the specific model is made of"""
cur.execute(sql.SQL("""
    SELECT DISTINCT(testcd)
    FROM {}.init_values;
    """).format(sql.Identifier(InvestigateModel)))

ReferenceModelSubstances = []
for i in cur.fetchall():
    ReferenceModelSubstances.append(i[0])

"""
get the simulation results of the 
ODE Simulation No. 65 at the specific time point
"""

ThresholdTime = 40
cur.execute("""
    SELECT pdtestcd, pdorres
    FROM combined_models.pd
    WHERE pddtc = %s AND pdseq = 65;
    """, [ThresholdTime])

"""create the corresponding dict for this query"""
OdeSolutionAtTimepoint_dict = {}
for i in cur.fetchall():
    OdeSolutionAtTimepoint_dict[i[0]] = i[1]

# TODO : round up the numbers of i[1] 

# NOTE : i can also update the whole series of values at 40 s the db

"""
we must remove V_os, because in the combined model it is not an ODE
"""
if InvestigateModel == 'hog':
    ReferenceModelSubstances.remove('V_os')

# TODO: create 4 new possible ODE states --> now i only make number 2
"""
1. all values at timepoint 40s
2. only all values from the substance of the hog model
3. only all values from the substance of the volume model
4. only all values from the substance of the ion model
"""

Comment = 'changed from orginal' 
for TESTCD,ORRES in OdeSolutionAtTimepoint_dict.items():
    if TESTCD in ReferenceModelSubstances:

        cur.execute(sql.SQL("""
            UPDATE {}.init_values
            SET orres = %s, co = %s
            WHERE testcd = %s AND seq = %s;
            """).format(sql.Identifier(TargetModel)), [ORRES, Comment,TESTCD, SeqToWorkWith])
        conn.commit()

cur.close()
conn.close()