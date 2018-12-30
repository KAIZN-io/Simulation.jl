exec(open("SYSTEM/py_packages.py").read())


def findDiff(d1, d2):
    DifferenceDict = {}

    for i,substance in d1.items():

        if i == 'copa':
            pass
        else:

            # DifferenceDict[i] = {}
            for SubstanceName,k in substance.items():

                if SubstanceName not in d2[i].keys():
                    print("Substance", SubstanceName, "not in second dict")
                else:
                    # DifferenceDict[i][SubstanceName] = {}

                    for m,n in k.items():

                        if type(n) == dict:
                            # DifferenceDict[i][SubstanceName][m] = {}
                            for patSubstance, Term in n.items():
                                if patSubstance not in d2[i][SubstanceName][m].keys():
                                    DifferenceDict[i] = {}
                                    DifferenceDict[i][SubstanceName] = {}
                                    DifferenceDict[i][SubstanceName][m] = {}
                                    DifferenceDict[i][SubstanceName][m][patSubstance] = Term

    return DifferenceDict

TargetModel = 'combined_models'

conn = psycopg2.connect(host='localhost', dbname='simulation_results')
cur = conn.cursor()

"""get the max seq for the iteration process"""
cur.execute(sql.SQL("""
    select max(seq)
    from {}.json
    """).format(sql.Identifier(TargetModel)))
MaxSeq = cur.fetchone()[0]

for i in range(1, MaxSeq):

    cur.execute(sql.SQL("""
        select model_version
        from {}.json
        where seq = %s;
        """).format(sql.Identifier(TargetModel)), [i])

    first_dict = cur.fetchone()[0]

    cur.execute(sql.SQL("""
        select model_version
        from {}.json
        where seq = %s;
        """).format(sql.Identifier(TargetModel)), [i+1])

    second_dict = cur.fetchone()[0]

    Adding_Changes = findDiff(second_dict, first_dict)
    Deleting_Changes = findDiff(first_dict,second_dict)

    AddingChanges_json = json.dumps(Adding_Changes, indent=4)
    DeletingChanges_json = json.dumps(Deleting_Changes, indent=4)


    cur.execute(sql.SQL("""
        UPDATE {}.json
        SET adding_changes = %s, deleting_changes = %s
        WHERE seq = %s;
        """).format(sql.Identifier(TargetModel)), [AddingChanges_json, DeletingChanges_json, i+1])
    conn.commit()

# cur.close()
# conn.close()
