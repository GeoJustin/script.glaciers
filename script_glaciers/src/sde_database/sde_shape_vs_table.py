"""****************************************************************************
 Name:         sde_database.sde_connections
 Purpose:     
 
Created:         Apr 8, 2013
Author:          Justin Rich (justin.rich@gi.alaska.edu)
Location: Geophysical Institute | University of Alaska, Fairbanks
Contributors:

Copyright:   (c) Justin L. Rich 2013
License:     Although this application has been produced and tested
 successfully, no warranty expressed or implied is made regarding the
 reliability and accuracy of the utility, or the data produced by it, on any
 other system or for general or scientific purposes, nor shall the act of
 distribution constitute any such warranty. It is also strongly recommended
 that careful attention be paid to the contents of the metadata / help file
 associated with these data to evaluate application limitations, restrictions
 or intended use. The creators and distributors of the application shall not
 be held liable for improper or incorrect use of the utility described and/
 or contained herein.
****************************************************************************"""
import sys, os
sys.path.append (os.path.dirname(os.path.dirname(__file__)))

import arcpy as ARCPY                                         #@UnresolvedImport                             

    
ARCPY.env.workspace = r'Database Connections\Alaska_Glaciers.sde'

output_location = r'A:\Desktop\ServerOutput'
input_feature = 'glaciers_alaska.sde.modern'
input_table = 'glaciers_alaska.sde.modern_hypsometry'

# Get list of GLIMS ID's that Exist in Table
list_glimsids = []
rows = ARCPY.SearchCursor (input_table)
for row in rows:
    list_glimsids.append(row.glimsid)
del row, rows

print len(list_glimsids)


projection = ARCPY.Describe(input_feature).spatialReference
feature = ARCPY.CreateFeatureclass_management (output_location, 'Missing.shp', 'POLYGON', input_feature, '', '', projection)
insert = ARCPY.InsertCursor(feature)


rows = ARCPY.SearchCursor (input_feature)
for row in rows:
    if row.glimsid not in list_glimsids:
        print 'Missing Feature: ', row.glimsid       
        insert.insertRow(row)
del row, rows