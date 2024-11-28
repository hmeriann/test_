import duckdb
import argparse
import re
import random
import string

# Verifying version
parser = argparse.ArgumentParser()
parser.add_argument("nightly_build")
parser.add_argument("--runs_on")
parser.add_argument("--version")
args = parser.parse_args()
if not args:
    print("SET nightly_build parameter")

nightly_build = args.nightly_build
runs_on = args.runs_on
version = args.version

# TODO: if it is a release, check also "delta" (only for linux-python3) and "motherduck"

# with open("extensions/.github/config/out_of_tree_extensions.cmake", "r") as file:
with open("/Users/zuleykhapavlichenkova/Documents/test_/ext/.github/config/out_of_tree_extensions.cmake", "r") as file:
    content = file.read()
    pattern = r"duckdb_extension_load\(\s*([^\s,)]+)"
    extensions = re.findall(pattern, content)

with open("issue_ext_{}.txt".format(nightly_build), 'w') as f:
    for extension in extensions:
        try:
            duckdb.sql(f"INSTALL { extension }")
            print(f"Installed { extension } ")

            try:
                duckdb.sql(f"LOAD { extension }")
                print(f"Loaded { extension } ")
            except Exception as e:
                message = f"- Error loading { extension } { nightly_build } on { runs_on }_{ version }: {str(e)}\n "
                f.write(f"{ nightly_build },NULL,{ runs_on },{ version },{ extension },INSTALL\n")
                print(message)
        except Exception as e:
            message = f"- Error installing { extension } { nightly_build } on { runs_on }_{ version }: {str(e)}\n "
            f.write(f"{ nightly_build },NULL,{ runs_on },{ version },{ extension },LOAD\n")
            print(message)
    
    # negative test to make sure that DuckDB handles non-existing extension name
    print(f"Running negative test with the random name of extension...")
    unexpected = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
    try:
        duckdb.sql(f"INSTALL { unexpected }")
        message = f"#### { unexpected } was unexpectedly installed on { nightly_build } { runs_on }_{ version }.\n "
        f.write(f"{ nightly_build },NULL,{ runs_on },{ version },{ unexpected },INSTALL\n")
        print(message)
        try:
            duckdb.sql(f"LOAD { unexpected }")
            message = f"#### { unexpected } was unexpectedly loaded on { nightly_build } { runs_on }_{ version }.\n "
            f.write(f"{ nightly_build },NULL,{ runs_on },{ version },{ unexpected },LOAD\n")
            print(message)
        except Exception as e:
            print(f"Extension { unexpected } is not loaded on { nightly_build } { runs_on }_{ version }: {str(e)}\n")
            pass
    except Exception as e:
        print(f"Extension { unexpected } is not installed on { nightly_build } { runs_on }_{ version }: {str(e)}\n ")
        pass