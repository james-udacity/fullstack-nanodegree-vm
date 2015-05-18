## How to run:

- Start `psql`. (Make sure you are in /vagrant/tournament)

- If you don't already have a database named tournament in your PostgreSQL, run the following command:
   `CREATE DATABASE tournament;`

- If it already exists, drop the tables within it or drop the whole database with 
 `DROP DATABASE tournament;` and then run the command above.

- Execute the following to define the tables:
`\i tournament.sql`

- After that completes, exit psql by executing `\q`.

- Run the test suite by executing `python tournament_test.py`.
