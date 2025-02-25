import duckdb

con = duckdb.connect("chameleon.duckdb", read_only=True)

with open("binning.sql") as f:
    con.execute(f.read())
