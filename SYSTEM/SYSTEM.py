# NOTE: import the standard used packages
exec(open("py_packages.py").read())

# NOTE: creates the db reference_bib
try:
    conn = psycopg2.connect(host='localhost', dbname='postgres')
    dbname = "reference_bib"
    cur = conn.cursor()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(dbname)))
    cur.close()
    conn.close()

except:
    pass
