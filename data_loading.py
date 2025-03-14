import duckdb


con = duckdb.connect("deel_interview.duckdb")

con.sql("CREATE OR REPLACE TABLE organizations AS SELECT * FROM 'data\deel_takehome\organizations.csv';")
con.sql("CREATE OR REPLACE TABLE invoices AS SELECT * FROM 'data\deel_takehome\invoices.csv';")

con.close()