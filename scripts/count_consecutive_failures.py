import duckdb
import argparse

# Verifying version
parser = argparse.ArgumentParser()
parser.add_argument("input_file")
parser.add_argument("--nightly_build")
parser.add_argument("--architecture")
parser.add_argument("--url")
args = parser.parse_args()

if not args:
    print("Usage: python scripts/count_consecutive_failures.py <input_file>.json --nightly_build --architecture")

input_file = args.input_file
nightly_build = args.nightly_build
architecture = args.architecture
url = args.url
all = duckdb.sql(f"SELECT * FROM read_json('{ input_file }')")
rows = all.fetchall()
conclusions = [row[0] for row in rows]
failures=0
for c in conclusions:
    if c == 'failure':
        failures+=1
    else:
        break

def create_issue_body():
    if failures >= 1:
        failures_list = "failures_list.md"
        duckdb.sql(f"""
                    COPY (
                        SELECT conclusion, createdAt, url
                        FROM read_json('{ input_file }') 
                        WHERE conclusion='failure'
                        LIMIT '{ failures }'
                    )  
                    TO '{ failures_list }' (HEADER 0, QUOTE '', SEPARATOR '|');
                    """)
        with open("issue_body_{}.txt".format(architecture), 'w') as f:
            f.write(f"\nThe **'{ nightly_build }'** nightly-build has not succeeded the previous '{ failures }' times.\nSee the latest run: [ Run Link ](https:{ url })\n")
            f.write(f"#### Failure Details\n\n")
            f.write(f"| Conclusion | Started At | Run URL |\n")
            f.write(f"|------------|------------|---------|\n")
            with open(failures_list, 'r') as failures_file:
                f.write(failures_file.read())
    else:
        with open("issue_body_{}.txt".format(architecture), 'w') as f:
            f.write(f"\nThe **'{ nightly_build }'** nightly-build has succeeded.\nSee the latest run: [ Run Link ](https:{ url })\n")

def main():
    create_issue_body()
    
if __name__ == "__main__":
    main()