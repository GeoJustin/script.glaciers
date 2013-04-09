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
import glacier_utilities.functions.data_pop as data_pop
    
ARCPY.env.workspace = r'Database Connections\Alaska_Glaciers.sde'
input_feature = 'glaciers_alaska.sde.mapdate'

print 'Running Function'
# Function to Run**************************************************************


data_pop.generate_RGIIDs(input_feature, 30, 01)


#******************************************************************************
print 'Function Run'