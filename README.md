# PostgreSQLMigration
Script to make SQL Server to Postgres migration easier for functions and stored procedures.

The functionalities of this Python project is only possible after applying [sqlserve2pgsql](https://github.com/dalibo/sqlserver2pgsql) for schema/data and AWS Schema Convertion for views/functions. This combination of tools already complete most of the migration, leaving only few unconverted cases to handle; and this project specifically handles repetitive instances of this final manual migration process.

## List of functionality
- replace the convert() function when it is used as a non formatted type cast
- standardize keyword capitalization along the relevant keywords directly involved
- replace the charindex() function with position()
- find and replace simple relavent strings
- tools: split sql dumps to single files

## Disabled functionality
- add dbo. (or any schema name) to tables in a FROM/JOIN statement
- spacing adjustment

## Known issues
- convert() feature does not work if the function call is multiline
- rare exeptions exist with replace / modify features, may not be fit to use on very large files
- program hangs on file selection

## Using the tool
1. run`git clone https://github.com/neveratdennys/PostgreSQLMigration`
2. from the cloned directory, run `python postgresProcess.py`
3. follow instructions and choose files for conversion
