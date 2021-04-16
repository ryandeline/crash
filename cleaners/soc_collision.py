# %load_ext autotime
# import pyodbc as odbc
import win32.com as odbc
import csv
import re
import pandas as pd
import numpy as np
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm
# import pyad.adbase as ad
# import matplotlib.pyplot as plt 
# import plotly_express as px 
# from scipy import stats

### Stage One Processing: Removes points outside of a rough MACOG area of interest
### Stage One Processing: Adds updated street names and zip codes columns based on open street maps pull
### Stage One Processing: Creates an updated Roadway column from Roadway ID & Roadway Suffix that can be used to compare against pulled data
### Stage One Processing: Creates and Intersecting Road column with combined data from Intersecting Road & Intersecting Road Number
### Stage One Processing: Eliminates directionals on State facilities to help with filters

# Open Access App and Database
oApp = odbc.client.Dispatch("Access.Application")
oApp.OpenCurrentDatabase('X:/Users/rdeline/Documents/temp/Elkhart County 2015.accdb')

# Export tabe to dataframe
acExportDelim = 2
oApp.DoCmd.TransferText(acExportDelim, None, "Collision", 'Output.csv')

oApp.DoCmd.CloseDatabase
oApp.Quit
oApp = None

# odbc.lowercase = False
# con = pypyodbc.connect(
# 	r"Driver = {Microsoft Access Driver (*.mbd, *.accdb)};" +
# 	r"Dbq")
winfile = "F:/Tableau/Transportation/Crash/table/MASTERCRASH.csv"
# winfile = "C:/Users/DeLine/Dropbox/work/MACOG/Crash/table/MASTERCRASH.csv"
woutfile = "F:/Tableau/Transportation/Crash/table/MACOGCRASH.csv"
# woutfile = "C:/Users/DeLine/Dropbox/work/MACOG/Crash/table/MACOGCRASH.csv"

DataFrame = pd.read_csv(winfile, low_memory = False, encoding = "ISO-8859-1")

### Rename Columns
df = DataFrame.rename(columns = {'Master Record Number':'MASTERID',
								'Collision Date': 'Date', 'Collision Time': 'Time', 'Year':'Year', 
								'Roadway Id': 'RoadID','Roadway Suffix': 'Suffix', 'Intersecting Road':'Intersecting', 'Roadway Name': 'Road', 
								'County':'CountyDNU', 'Zip':'ZipCode', 'Community':'Community', 'City':'City DNU', 'Township':'Township', 
								'Agency':'Responding Agency', 'Vehicles Involeved':'Total Vehicles', 'Number Injured':'Injured', 
								'Number Dead':'Fatalities', 'Fatality / Injury':'Fatality / Injury', 'Property Damage Only':'PDO', 'Number of Deer':'Deer Count',  
								'Hit and Run?':'Hit and Run', 'School Zone?':'School Zone',	'Construction?': 'Construction', 
								'Light Condition':'Light', 'Weather Conditions':'Weather', 'Surface Condition':'Surface Conditions', 'Road Character':'Geometry', 
								'Roadway Surface':'Surface','Primary Factor':'Primary Factor'})


### Ensures Lat & Lon are in MACOG aoi.
df = df[df.Latitude.notnull()]
df = df[df.Longitude.notnull()]
df = df[df.Latitude != 0]
df = df[df.Longitude != 0]
df = df[(df['Latitude'] >= 41.017) & (df['Latitude'] <= 41.74)] 
df = df[(df['Longitude'] <= -85.643) & (df['Longitude'] >= -86.625)]
df = df.round({'Latitude':6, 'Longitude':6})
df = df.rename_axis('ID', axis=1)

### Creates Column 'Roadway' with the records concatonated Road Name
road = df['RoadID']
suffix = df['Suffix'].fillna('')
complete_road = road + " " + suffix
df['Roadway'] = complete_road.str.rstrip()

### Creates Column 'Intersecting Road' with the records concatonated Intersecting
df['Intersecting'] = df['Intersecting'].fillna('')
df['Intersecting'] = df.apply(lambda x: x['Intersecting Road Number'] 
	if x['Intersecting'] == "" else x['Intersecting'], axis=1)
df['Intersecting Road'] = df['Intersecting']

### Geo search for consistent street & zip.  Creating new columns 'Street' & 'Zip Code'  -long run time geocoding every row.  comment out if not desired
geo = Nominatim(user_agent = "Standard_Road", timeout = 10)
geocode = RateLimiter(geo.reverse, min_delay_seconds = 2)
tqdm.pandas()
g = df['Latitude'].map(str) + ',' + df['Longitude'].map(str)
g[0]
d = g.progress_apply(lambda x: geo.reverse(x).raw['address'])
df2 = pd.DataFrame(data = d)
df['Street'] = [df2.get('road') for df2 in df2[0]]
df['Zip Code'] = [df2.get('postcode') for df2 in df2[0]]

### Drop Unnecessary Columns - If on is desired please contact rdeline@macog.com
df = df.drop(['Local Code','CountyDNU','City DNU', 'Township', 'House Number', 'Road', 
				'RoadID', 'Intersecting','Intersecting Road Number','Mile Marker', 'Type of Median',
				'Interchange','Suffix', 'Roadway Number', 'Roadway Interchange','Year',
				'Roadway Ramp','Corporate Limits?','Property Type','Direction','LatitudeDNU',
				'LongitudeDNU','Time Notified','Time Arrived','Investigation Complete?','Photos Taken?',
				'Officer First Name','Officer Id','Unique Location Id','State Property Damage?'], axis=1) #,  

### Organize Columns
df = df[['MASTERID','Date','Time','Roadway','Intersecting Road', 'Street', 'Zip Code', 'Responding Agency','Locality',
			'School Zone', 'Construction','Construction Type','Rumble Strips?','Traffic Control','Light','Weather',
			'Surface Conditions','Geometry','Surface','Primary Factor','Manner of Collision','Damage Estimate',
			'Officer Last Name','Narrative']]


df.to_csv(woutfile, sep = ',')

#     

# class Address(ad.ADBase):
# 	def initialize(self):
# 		self.adbase = self.get_ad_api()
# 		self.hass = self.get_plugin_api("HASS")

# 		self.adbase.log("App Started.")
# 		entities = self.args["entities"]

# 		if isinstance(sentities, str):
# 			entities = [ent_id.strip() for ent_id in entities.split(",")]

# 		for entitiy in entities:
# 			self.update_address(entitiy)
# 			self.hass.listen_state(self.location_change_cb, entitiy)
# 			self.adbase.log(f"State listener for {entity} started.")

# 	def location_change_cb(self, entity, attribute, old, new, kwargs):
# 		self.update_address(entity)

# 	def update_address(self, entity):
# 		entity_state = self.hass.get_state(entity, attribute = "all")
# 		state = entity_state['state']
# 		attributes = entity_state['attributes']

# 		Latitude = attributes.get('Latitude')
# 		Longitude = attributes.get('Longitude')

# 		if not latitude and not longitude:
# 			self.adbase.log(f"No Latitude/Longitude attribute found for {entity}")
# 			return

# 		geo = Nominatim(user_agent = "Standard_Road")
# 		geocode = RateLimiter(geo.geocode, min_delay_seconds = 1)
# 		data = geo.reverse(f"{Latitude}, {Longitude}")
# 		raw = data.raw["address"]
# 		self.adbase.log(raw)

# 		for attr in raw:
# 			attributes[attr] = raw[attr]

# 		self.adbase.log(f"Updating state for {entity}")
# 		self.hass.set_state(entity, state = state, attributes = attributes, namespace = "hass")

# class Address(ad.ADBase):
# 	def initialize(self):
# 		self.adbase = self.get_ad_api()
# 		self.hass = self.get_plugin_api("HASS")

# 		self.adbase.log("App Started.")
# 		entities = self.args["entities"]

# 		if isinstance(sentities, str):
# 			entities = [ent_id.strip() for ent_id in entities.split(",")]

# 		for entitiy in entities:
# 			self.update_address(entitiy)
# 			self.hass.listen_state(self.location_change_cb, entitiy)
# 			self.adbase.log(f"State listener for {entity} started.")

# 	def get_address(self, entitiy, attribute, old, new, kwargs):
# 		attributes = self.hass.get_state(entity, attribute = "all")['attributes']
# 		lattitude = df['Latitude']
# 		longitude = df['Longitude']

# 		if not lattitude and not longitude:
# 			self.adbase.log(f"No latitude/longitude attribute found for {entity}")

# 		geo = Nominatim(user_agent = "Standard_Road")
# 		geocode = RateLimiter(geo.geocode, min_delay_seconds = 1)
# 		data = geo.reverse(f"{Latitude}, {Longitude}")
# 		raw = data.raw["address"]

# 		for attr in raw:
# 			attributes[attr] = raw[attr]

# 		self.adbase.log(f"Updating state for {entity}")
# 		self.hass.set_state(entity, state = state, attributes = attributes)	