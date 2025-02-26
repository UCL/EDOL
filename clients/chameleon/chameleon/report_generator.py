import duckdb

with open("binning.sql") as f:
    query = f.read().format(
        start_time="2025-01-01",
        end_time="2027-01-02",
        interval="21 minutes",
        output_file="chameleon_report.csv",
    )

    db = duckdb.connect("chameleon.duckdb", read_only=True)
    db.execute(query)
    db.close()
