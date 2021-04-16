# %load_ext autotime
# import pypyodbc as odbc
import pyodbc as odbc
# import win32.com as odbc
import csv
import sys
import os

# [x for x in odbc.drivers() if x.startswith('Microsoft Access Driver')]
# 
con = (
	r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};' 
	r'DBQ=X:\Users\rdeline\Documents\temp\Elkhart_County_2015.accdb;'
	)

cnxn = odbc.connect(con)
cur = cnxn.cursor()
for table_info in cur.tables(tableType = 'TABLE'):
	print(table_info.table_name)




# MS Access DB Connection
# odbc.lowercase = False
# con = odbc.connect(
# 	r"Driver = {Microsoft Access Driver (*.mbd, *.accdb)};" +
# 	r"Dbq = X:/Users/rdeline/Documents/temp/Elkhart County 2015.accdb;")

# # Open Cursor and Execute SQL
# cur = con.cursor()
# cur.execute("SELECT Master Record Number FROM Collision");

# # Open csv and iterate through results
# with open('X:/Users/rdeline/Documents/temp/Output.csv', 'w', newline = '') as f:
# 	writer = csv.writer(f)
# 	for row in cur.fetchall():
# 		writer.writerow(row)

# cur.close()
# con.close()

# Open Access App and Database
# oApp = odbc.client.Dispatch("Access.Application")
# oApp.OpenCurrentDatabase('X:/Users/rdeline/Documents/temp/Elkhart County 2015.accdb')

# # Export tabe to dataframe
# acExportDelim = 2
# oApp.DoCmd.TransferText(acExportDelim, None, "Collision", 'X:/Users/rdeline/Documents/temp/Output.csv')

# oApp.DoCmd.CloseDatabase
# oApp.Quit
# oApp = None

# con = odbc.connect('Driver = {Microsoft Access Driver (*.mdb, *.accdb)}; DBQ = X:/Users/rdeline/Documents/temp/Elkhart County 2015.accdb;')
# cur = con.cursor()

# def output_col(col)
# 	if col:
# 		if isinstance(col, unicode):
# 			return col.encode('utf-8')
# 		else:
# 			return str(col)
# 	else:
# 		return ""

# writer = csv.writer(open('X:/Users/rdeline/Documents/temp/Output.csv', 'wb'), delimeter = ',')

# writer.writerow([t[0] for t in row.cursor_description])
# while 1:
# 	if not row:
# 		break
# 	writer.writerow(map(output_col, row))
# 	row = cursor.fetchone()

# print(writer)