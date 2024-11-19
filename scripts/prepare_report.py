import duckdb
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file_name")
args = parser.parse_args()
if not args:
    print("SET file_name argument")

file_name = args.file_name

with open("res.md", 'w') as f:
    f.write(f"\n#### Extensions failed to INSTALL:\n")
    f.write(f"Nightly-build|Runs_on|Version|Extension|Failed statement\n")
    f.write(f"----|----|----|----|----\n")
    duckdb.sql(f"""
                COPY (SELECT * FROM read_csv("{ file_name }")
                    WHERE column4='INSTALL'
                    ORDER BY column1, column2, column3)
                TO tmp.md (HEADER 0, SEPARATOR '|')
                """)
    with open("tmp.md", 'r') as tbl:
        f.write(tbl.read())
    
    f.write(f"\n#### Extensions failed to LOAD:\n")
    f.write(f"Nightly-build|Runs_on|Version|Extension|Failed statement\n")
    f.write(f"----|----|----|----|----\n")
    duckdb.sql(f"""
                COPY (SELECT * FROM read_csv("{ file_name }")
                    WHERE column4='LOAD'
                    ORDER BY column1, column2, column3)
                TO tmp.md (HEADER 0, SEPARATOR '|')
                """)
    with open("tmp.md", 'r') as tbl:
        f.write(tbl.read())