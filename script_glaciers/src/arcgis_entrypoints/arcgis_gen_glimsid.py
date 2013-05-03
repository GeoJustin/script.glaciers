"""****************************************************************************
 Name:         arcgis_entrypoints.arcgis_gen_glimsid
 Purpose:     entry point for ArcGIS to run gen_glimsid
 
Created:         May 3, 2013
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

import glacier_utilities.functions.data_pop as DP
import arcpy as ARCPY                                        #@UnresolvedImport

# Read parameter values from ArcGIS tool input
# 1 - The file RGI ID values will be added to. File must have a 'glimsid' field.
# 2 - A workspace to re-project data to. 

try: glims_file = ARCPY.GetParameterAsText(0)
except: ARCPY.AddError('GLIMS Input File Error')

try: glims_workspace = ARCPY.GetParameterAsText(1)
except: ARCPY.AddError('GLIMS Version Information Error')

# Run the Generate GLIMS ID function
try:
    DP.generate_GLIMSIDs(glims_file, glims_workspace)
except:
    ARCPY.AddError('Errors generated during function execution')

# Driver - Currently Does nothing
def driver():
    pass
if __name__ == '__main__':
    driver()