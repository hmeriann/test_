import duckdb
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file_name")
args = parser.parse_args()
if not args:
    print("SET file_name argument")

file_name = args.file_name

with open("res.md", 'w') as f:
    f.write(f"runs_on,version,extension,failed_statement\n")
    f.write(f"----|----|----|----\n")
    duckdb.sql(f"""
        .mode markdown
        COPY (SELECT * FROM read_csv("{ file_name }")
            GROUP BY extension, ORDER BY failed_statement)
        TO tmp.md (HEADER 1, SEPARATOR '|')
    """)
    with open("tmp.md", 'r') as tbl:
        f.write(tbl.read())