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
print(url, "🥵")
all = duckdb.sql(f"SELECT * FROM read_json('{ input_file }')")
rows = all.fetchall()
conclusions = [row[0] for row in rows]
print(conclusions)
failures=0
for c in conclusions:
    if c == 'failure':
        failures+=1
    else:
        break

def create_issue_body():
    failures_list = "failures_list.md"
    duckdb.sql(f"""
                COPY (
                    SELECT conclusion, startedAt, url
                    FROM read_json('{ input_file }') 
                    WHERE conclusion='failure'
                    LIMIT '{ failures }'
                )  
                TO '{ failures_list }' (HEADER 0, QUOTE '', SEPARATOR '|');
                """)
    with open("issue_body_{}.txt".format(architecture), 'w') as f:
        f.write(f"At least one job had failed in the **'{ nightly_build }'** nightly-build run consecutively '{ failures }' times: [ Run Link ](https:{ url })\n")
        f.write(f"#### Failure Details\n\n")
        f.write(f"| Conclusion | Started At | Run URL |\n")
        f.write(f"|------------|------------|---------|\n")
        with open(failures_list, 'r') as failures_file:
            f.write(failures_file.read())

def main():
    if failures >= 1:
        print(f"Found '{ failures }' failures.")
        # ???: Do we want to report only when >= 4 consecutive failures?
        # if failures >= 4:
        create_issue_body()
        return 1
    else:
        print(f"No failures found.")

        return 0

if __name__ == "__main__":
    main()