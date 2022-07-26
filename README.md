# PostgreSQLMigration
Script to make SQL Server to Postgres migration easier for Views and Function.

Although a lot of changes required for this migration can be completed with simply search and replace, but some changes are difficult to do especially on large databases. This project aims to provide more functionality and reduce manual conversion required given the sizable differences between tsql and pgsql.

## List of functionality
- add dbo. (or any schema name) to tables in a FROM/JOIN statement
- replace the convert() function when it is used as a non formatted type cast
- standardize keyword capitalization along the relevant keywords directly involved
- replace the charindex() function with position()
- find and replace simple relavent strings

## Known issues
- spacing can be imperfect depending on conventions
- limited testing in stored procedures and functions.

## Using the tool
1. run `git clone https://github.com/neveratdennys/PostgreSQLMigration`
2. from the cloned directory, run `python postgresProcess.py`
3. choose files for conversion
