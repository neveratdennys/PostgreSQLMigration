# PostgreSQLMigration
Scripts to make SQL Server to Postgres migration easier for functions, stored procedures and other scripts.

The functionalities of this Python project is only possible after applying [sqlserve2pgsql](https://github.com/dalibo/sqlserver2pgsql) for schema/data and AWS Schema Conversion for views/functions. This combination of tools already complete most of the migration, leaving fewer unconverted cases to handle; and this project specifically handles repetitive instances of this final manual migration process.

## List of functionality
- Released: 
	- Windows executable for combining multiple SQL scripts into one
- General:
	- replace the convert() function when it is used as a non formatted type cast
	- standardize keyword capitalization along the relevant keywords directly involved
	- replace the charindex() function with position()
	- replace .nodes() calls with relavent structure (still requires some manual work after replacement)
	- replace contains() function to ts_vector() @@ ts_query() structure
	- add ON true after INNER/LEFT JOIN LATERAL to complete OUTER/CROSS APPLY conversion
	- find and replace simple relavent strings
- Tools: 
	- split sql dumps to single files, 
  select subset of wanted files and split them to individual files, 
  clean files with excess double quotes

## Disabled functionality
- add dbo. (or any schema name) to tables in a FROM/JOIN statement
- spacing adjustment

## Known issues
- convert() feature does not work if the function call is multiline, however this should be extremely rare
- position() and ts_vector() @@ ts_query() replacements does not function correctly in dynamic sql construction.
- main program hangs on file selection in MINGW64

## Using the tool
1. run
	`git clone https://github.com/neveratdennys/PostgreSQLMigration`
2. from the cloned directory, run `python postgresProcess.py`
3. follow instructions and choose files for conversion
