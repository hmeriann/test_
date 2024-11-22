import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("config")
parser.add_argument("--arch")

args = parser.parse_args()
if not args:
    print("SET path to the out_of_tree_extensions.cmake file")

config = args.config
arch = args.arch

with open(config, "r") as file:
    content = file.read()

    # Adjusted regex for matching after `load(`
    pattern = r"duckdb_extension_load\(\s*([^\s,)]+)"
    matches = re.findall(pattern, content)
    print(matches)

if arch == arch.contains("aarch64"):
    matches = matches.replace('[', '(').replace(']', ')')