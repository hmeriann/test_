import duckdb

# TODO: if it is a release, check also "delta" (only for linux-python3) and "motherduck"

extensions = [ "arrow", "autocomplete", "aws", "azure", "excel", "fts", "httpfs", "iceberg", "icu", "inet", "json",
    "mysql_scanner", "parquet", "postgres_scanner", "spatial", "sqlite_scanner", "substrait", "tpcds", "tpch", "vss", "unexpected" ]

with open("issue_body_Python_extensions.txt", 'w') as f:
    for extension in extensions:
        if extension == "unexpected":
            try:
                duckdb.sql(f"INSTALL {extension}")
                message = f"#### `{extension}` was unexpectedly installed.\n "
                f.write(message)
                print(message)
                try:
                    duckdb.sql(f"LOAD {extension}")
                    message = f"#### `{extension}` was unexpectedly loaded.\n "
                    f.write(message)
                    print(message)
                except Exception as e:
                    print(f"Extension `{extension}` is not loaded\n")
                    pass
            
            except Exception as e:
                print(f"Extension `{extension}` is not installed ✅")
                pass

        else:
            try:
                duckdb.sql(f"INSTALL {extension}")
                print(f"Installed {extension} ✅")

                try:
                    duckdb.sql(f"LOAD {extension}")
                    print(f"Loaded {extension} ✅")
                except Exception as e:
                    message = f"#### Error loading `{extension}`: `{str(e)}`\n "
                    f.write(message)
                    print(message)

            except Exception as e:
                message = f"#### Error installing `{extension}`: `{str(e)}`\n "
                f.write(message)
                print(message)