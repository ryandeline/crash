import pyodbc
import pandas as pd
conn = pyodbc.connect('Driver = {SQL Server};'
						'Server = server_name';
						'Database = Crash;'
						'Trusted_Connections = yes;')

cursor = conn.cursor()
cursor.execute(''' CREATE TABLE COLLISION
				Master_Record_Number int, Agency nvarchar(25), Local_Code nvarchar(25), County nvarchar(25),
				Township nvarchar(25), City nvarchar(25), Collision_Date Date, Collision_Time TIMESTAMP(),
				Vehicles_Involved int, Trailers_Involved int, Number_Injured int, Number_Dead int, Number_Deer int,
				House_Number int, Roadway_Name nvarchar(50), Roadway_Suffix nvarchar(10), Roadway_Number nvarchar(10).
				Roadway_Interchange nvarchar(10), Roadway_Ramp nvarchar(10), Roadway_Id nvarchar(50),
				Intersecting_Road nvarchar(50), Intersecting_Road Number nvarchar(10), Mile_Marker DECIMAL(10,2),
				Interchange nvarchar(2), Corporate_Limits nvarchar(2), Property_Type nvarchar(10),
				Feet_From int, Direction nvarchar(2), Latitude DECIMAL(6, 4), Longitude DECIMAL(6,4),
				Roadway_Class nvarchar(50), Traffic_Control_Devices nvarchar(2), Aggressive_Driving nvarchar(2),
				Hit_and_Run nvarchar(2), Locality nvarchar(10), School_Zone nvarchar(2), Rumble_Strips nvarchar(2),
				Construciton nvarchar(2), Light_Condition nvarchar(25), Weather_Conditions nvarchar(50),
				Surface_Condition nvarchar(25), Type_of_Median nvarchar(15), Roadway_Junction_Type nvarchar(50),
				Road_Character nvarchar(15), Roadway_Surface nvarchar(15), Primary_Factor nvarchar(50),
				Damage_Estimate nvarchar(15), Manner_of_Collision nvarchar(50), Time_Notified int, Time_Arrived int,
				Investigation_Complete nvarchar(2), Photos_Taken nvarchar(2), Officer_Last_Name nvarchar(15),
				Officer_First_Name nvarchar(2), Officer_Id nvarchar(10), Unique_Locaiton_Id nvarchar(100),
				State_Property_Damage BOOLEAN, Traffic_Control nvarchar(25), Narrative nvarchar(200))''')

cursor.execute(''' CREATE TABLE INDIVIDUAL
				Master_Record_Number int, Vehicle Number int, Person Number int, City nvarchar(25), State nvarchar(2),
				Zip_Code nvarchar(10), Person_Type nvarchar(25), Birth_Date DATE, Age int, Gender nvarchar(10), 
				Popsition_in_Vehicle nvarchar(25), Ejection_Trapped nvarchar(25), Safety_Equipment_Used nvarchar(25),
				Safety_Equipment_Effective nvarchar(2), Injury_Status nvarchar(25), Nature_of_Injury nvarchar(25),
				Location_of_Injury nvarchar(25), Test_Given nvarchar(25), Test_Results nvarchar(25), Drugs nvarchar(20), EMS_Number nvarchar(10))''')

cursor.execute(''' CREATE TABLE MACOG_INJURY_STATUS
				Master_Record_Number int, Collision Date Date, Crash_Severity nvarchar(25),
				Fatal int, Incapacitating int, Non_Incompacitating int, Possible int))''')

cursor.execute(''' CREATE TABLE MACOG_LATITUDE_LONGITUDE
				Master_Record_Number int, MACOG_Latitude DECIMAL(6,4), MACOG_Longitude DECIMAL(6,4)''')

cursor.execute(''' CREATE TABLE UNIT
				Master_Record_Number int, Vehicle Number int, Vehicle_Type nvarchar(50), Year nvarchar(4), Make nvarchar(25),
				Model nvarchar(25), Occupants int, State_of_License nvarchar(2), Axcles int, Speed_Limit int, Towed nvarchar(2),
				Vehicle_Use nvarchar(25), Type_of_Roadway nvarchar(50), Direction_of_Travel nvarchar(2), Emergency_Run nvarchar(2),
				Fire nvarchar(2), Collision_With nvarchar(25), Pre_Crash_Vehicle_Action nvarchar(25)''')