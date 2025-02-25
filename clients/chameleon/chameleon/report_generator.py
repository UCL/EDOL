import duckdb

db = duckdb.connect("chameleon.duckdb", read_only=True)

with open("binning.sql") as f:
    query = f.read()
    db.execute(
        query,
        {
            "start_time": "2025-01-01",
            "end_time": "2027-01-02",
        },
    )

db.close()
