# PostgreSQLMigration
Scripts to make SQL Server to Postgres migration easier for functions, stored procedures and other scripts.

The functionalities of this Python project is only possible after applying [sqlserve2pgsql](https://github.com/dalibo/sqlserver2pgsql) for schema/data and AWS Schema Conversion for views/functions. This combination of tools already complete most of the migration, leaving fewer unconverted cases to handle; and this project specifically handles repetitive instances of this final manual migration process.

## List of functionality
- released: Windows executable for combining multiple SQL scripts into one
- replace the convert() function when it is used as a non formatted type cast
- standardize keyword capitalization along the relevant keywords directly involved
- replace the charindex() function with position()
- replace .nodes() calls with relavent structure (still requires some manual work after replacement)
- replace contains() function to ts_vector() @@ ts_query() structure
- find and replace simple relavent strings
- tools: split sql dumps to single files, 
  select subset of wanted files and split them to individual files, 
  clean files with excess double quotes

## Disabled functionality
- add dbo. (or any schema name) to tables in a FROM/JOIN statement
- spacing adjustment

## Known issues
- convert() feature does not work if the function call is multiline, however this should be extremely rare
- rare exeptions exist with replace / modify features
- main program hangs on file selection in MINGW64

## Using the tool
1. run`git clone https://github.com/neveratdennys/PostgreSQLMigration`
2. from the cloned directory, run `python postgresProcess.py`
3. follow instructions and choose files for conversion
