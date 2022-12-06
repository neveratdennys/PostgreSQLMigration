## Post-AWS tool notes

- AWS Schema Migration generates functions and stored procedures with `CREATE OR REPLACE`. This may result in unwanted behaviour if some parameter are edited, since PostgreSQL supports overloading for both objects and may create functions or stored procedures with the same name but different parameter types.
	- It may be better to write `DROP FUNCTION IF NOT EXISTS` (or stored procedures) before every `CREATE OR REPLACE` statement to avoid unwanted overloading; or simply drop both objects before creating again.
