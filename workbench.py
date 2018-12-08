"""import the standard used packages"""
exec(open("SYSTEM/py_packages.py").read())

conn = psycopg2.connect(host='localhost', dbname='simulation_results',\
                        user='janpiotraschke')

# open a cursor to perform database operations
cur = conn.cursor()

# name = 'combined_models'
# with open('csv_datafiles/{}/PD.csv'.format(name), 'r') as f:
#     next(f)
#     # copy_from(file, table, sep='\t', null='\\N', size=8192, columns=None)
#
#     # upper case letters must be in double quotes
#     cur.copy_from(f,'combined_models.pd', sep=',')
#
# # When commit is called, the PostgreSQL engine will run all the queries at once.
# conn.commit()

"""delete a unique row(s) from the table"""
# cur.execute("DELETE FROM combined_models.pd WHERE pdseq=3;")

seq_list = [[x] for x in list(range(23,30))]
# cur.execute("SELECT DISTINCT pdseq FROM combined_models.pd;")
# cur_fet = cur.fetchall()
# cur_fet.sort()
# print(cur_fet)
cur.executemany("DELETE FROM combined_models.pd WHERE pdseq=%s", seq_list)
conn.commit()

cur.executemany("DELETE FROM combined_models.ex WHERE exseq=%s", seq_list)
conn.commit()


cur.close()
conn.close()
