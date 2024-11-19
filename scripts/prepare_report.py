import duckdb
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file_name")
args = parser.parse_args()
if not args:
    print("SET file_name argument")

file_name = args.file_name

with open("res.md", 'w') as f:
    f.write(f"\n#### Extensions failed to INSTALL or to LOAD:\n")
    f.write(f" Nightly-build | Runs_on | Version | Extension | Failed statement \n")
    f.write(f"----|----|----|----|----\n")
    duckdb.sql(f"""
                COPY (SELECT * 
                    FROM read_csv("{ file_name }")
                        ORDER BY nightly_build, runs_on, version, extension
                    )
                TO tmp.md (HEADER 0, SEPARATOR '|')
                """)
    with open("tmp.md", 'r') as tbl:
        f.write(tbl.read())
