# MACOG CRASH 

This document is a running dataset with cleaned Lat Long coordinants provided by MACOG.

###### Iterations of the document will be produced as versions.  Details for those are found below.

## v.1 - 02.07.2020
2018 MARSHALL COUNTY crash data coordinates are not cleaned and the Lat Long is provided by the origin ARIES dataset.
2018 ELKHART COUNTY Narrative is missing from the origin data
2018 ST JOSEPH COUNTY Narrative is missing from the origin data

## v.2 - 03.23.2021
soc.collision.py created as a basic cleaner module 
	Stage One Processing: Removes points outside of a rough MACOG area of interest 
	### Stage One Processing: Adds updated street names and zip codes columns based on open  street maps pull 
	### Stage One Processing: Creates an updated Roadway column from Roadway ID & Roadway Suffix that can be used to compare against pulled data 
	### Stage One Processing: Creates and Intersecting Road column with combined data from Intersecting Road & Intersecting Road Number 
	### Stage One Processing: Eliminates directionals on State facilities to help with filters 
