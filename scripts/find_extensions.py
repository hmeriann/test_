import re

with open("ext/.github/config/out_of_tree_extensions.cmake", "r") as file:
    content = file.read()

    # Adjusted regex for matching after `load(`
    pattern = r"duckdb_extension_load\(\s*([^\s,)]+)"
    matches = re.findall(pattern, content)
    
    print(matches)