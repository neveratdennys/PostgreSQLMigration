# PostgreSQLMigration
Short scripts to make SQL Server to Postgres migration easier for Views and Function.

Although a lot of changes required for this migration can be completed with simply search and replace, but some changes are difficult to do especially on large databases. This script aims to provide more functionality and reduce manual conversion required given the sizable differences between tsql and pgsql.

List of functionality
- add dbo. (or any schema name) to tables in a FROM/JOIN statement
- replace the convert() function when it is used as a non formatted type cast
