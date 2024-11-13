import duckdb
import argparse

# Verifying version
parser = argparse.ArgumentParser()
parser.add_argument("full_sha")
parser.add_argument("--workflow")
parser.add_argument("--platform")
parser.add_argument("--version")
args = parser.parse_args()
if not args:
    print("NO SHA SET")

full_sha = args.full_sha
workflow = args.workflow
version = args.version
platform = args.platform

short_sha=duckdb.sql("PRAGMA version").fetchone()[1]

tested_version = f"{ workflow }_{ platform }_{ version }"
print(short_sha, full_sha)
if not args.full_sha.startswith(short_sha):
    message = f"- The version of `{ tested_version }` build (`{ short_sha }`) is not the same as the version triggered the build (`{ full_sha }`).\n "
    with open("issue_body_{}.txt".format(tested_version), 'w') as f:
        f.write(message)
    print(message)