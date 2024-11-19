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

result = duckdb.sql(f"""
              WITH runs AS (
                SELECT * FROM read_json('{ input_file }')
              )
              SELECT
                conclusion,
                count(*) AS count
              FROM (
                  SELECT
                    conclusion,
                    (row_number() OVER (ORDER BY startedAt) - row_number() OVER (PARTITION BY conclusion ORDER BY startedAt)) AS freq \
                  FROM runs
              )
              WHERE conclusion='failure' GROUP BY freq, conclusion ORDER BY count DESC LIMIT 1;
              """).fetchall()
# failures=$(tail -n +2 result.csv | awk -F ","  '{ print $2 }')
if result:
    failures = result[0][1]
else:
    failures = 0

def create_issue_body():
    failures_list = "failures_list.md"
    duckdb.sql(f"""
                COPY (
                    SELECT conclusion, startedAt, url
                    FROM read_json('{ input_file }') 
                    WHERE conclusion='failure'
                )  
                TO '{ failures_list }' (HEADER 0, QUOTE '', SEPARATOR '|');
                """)
    with open("issue_body_{}.txt".format(architecture), 'w') as f:
        f.write(f"### '{ nightly_build }':\n\n")
        f.write(f"At least one job had failed in the **'{ nightly_build }'** nightly-build consecutively '{ failures }' times: [ Run Link ](https:'{ url }')\n")
        f.write(f"#### Failure Details\n\n")
        f.write(f"| Conclusion | Started At | Run URL |\n")
        f.write(f"|------------|------------|---------|\n")
        with open(failures_list, 'r') as failures_file:
            f.write(failures_file.read())

def main():
    if failures >= 4:
        print(f"Found '{ failures }' failures.")
        create_issue_body()
        return 1
    else:
        print(f"No failures found.")

        return 0

if __name__ == "__main__":
    main()