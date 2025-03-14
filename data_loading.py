import duckdb

# create a connection to a file called 'deel_interview.duckdb'
con = duckdb.connect("deel_interview.duckdb")
# create tables and load data into it
con.sql("CREATE OR REPLACE TABLE organizations AS SELECT * FROM 'data\deel_takehome\organizations.csv';")
con.sql("CREATE OR REPLACE TABLE invoices AS SELECT * FROM 'data\deel_takehome\invoices.csv';")
# explicitly close the connection
con.close()