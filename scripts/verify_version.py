import duckdb
import argparse

# Verifying version
parser = argparse.ArgumentParser()
parser.add_argument("full_sha")
parser.add_argument("--workflow")
parser.add_argument("--architecture")
args = parser.parse_args()
if not args:
    print("NO SHA SET")

full_sha = args.full_sha
workflow = args.workflow
architecture = args.architecture

short_sha=duckdb.sql("PRAGMA version").fetchone()[1]
print(short_sha, args.full_sha)
if not args.full_sha.startswith(short_sha):
    message = f"#### The version of `{ workflow }` build (`{ short_sha }`) is not the same as the version triggered the build (`{ full_sha }`).\n "
    with open("issue_body_{}}.txt".format(architecture), 'w') as f:
        f.write(message)
    print(message)