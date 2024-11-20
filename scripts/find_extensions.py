import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("config")
args = parser.parse_args()
if not args:
    print("SET path to the out_of_tree_extensions.cmake file")

config = args.config

with open(config, "r") as file:
    content = file.read()

    # Adjusted regex for matching after `load(`
    pattern = r"duckdb_extension_load\(\s*([^\s,)]+)"
    matches = re.findall(pattern, content)
    print(matches)