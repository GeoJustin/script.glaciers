"""****************************************************************************
 Name:         arcgis_entrypoints.arcgis_gen_rgiid
 Purpose:     entry point for ArcGIS to run gen_rgiid
 
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
import glacier_utilities.functions.data_pop.generate_RGIIDs as gen_rgi
import arcpy as ARCPY                                        #@UnresolvedImport

# Read parameter values from ArcGIS tool input
# 1 - The file RGI ID values will be added to. File must have a 'rgiid' field.
# 2 - The RGI version
# 3 - The RGI region

rgi_file = ARCPY.GetParameterAsText(0)
rgi_version = ARCPY.GetParameterAsText(1)
rgi_region = ARCPY.GetParameterAsText(2)

# Run the Generate RGI ID function
gen_rgi (rgi_file, rgi_version, rgi_region)

# Driver - Currently Does nothing
def driver():
    pass
if __name__ == '__main__':
    driver()