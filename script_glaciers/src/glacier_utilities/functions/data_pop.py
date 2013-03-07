"""****************************************************************************
 Name:         glacier_utilities.functions.data_pop
 Purpose:     
 
Created:         Nov 19, 2012
Author:          Justin Rich (justin.rich@gi.alaska.edu)
Location: Geophysical Institute | University of Alaska, Fairbanks
Contributors:

Copyright:   (c) Justin L. Rich 2012
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
import os
import arcpy as ARCPY                                        #@UnresolvedImport

def generate_GLIMSIDs (input_file, workspace):
    """Generate GLIMS id's for the input table. These are based on latitude
    and longitude. File is re-projected into WGS84 to obtain these. 
    WARNING - ID's checked for Alaska but have NOT YET been verified in 
    other regions."""
    # Create a copy of the input in WGS 84 for calculating Lat. / Lon.
    output_wgs84 = workspace + "\\Input_File_WGS84.shp"
    projection = os.path.dirname(os.path.abspath(__file__)) + '\\projection\\WGS1984.prj'
    ARCPY.Project_management(input_file, output_wgs84, projection)
    
    glims_values = [] # Hold the ID's to add to non WGS-84 Table
    
    rows = ARCPY.UpdateCursor(output_wgs84)
    for row in rows:
        #Find the Centroid Point
        featureCenter = row.getValue(ARCPY.Describe(output_wgs84).shapeFieldName)
        X = int(round(featureCenter.centroid.X, 3) * 1000) # Get X of Centroid
        Y = int(round(featureCenter.centroid.Y, 3) * 1000) # Get Y of Centroid
        
        # Format the E and N/S values appropriately. 
        if X < 0: X = str((360000 + X) ) + "E"                  # Values 180-360
        elif X >= 0 and X < 10000: X = str(00) + str(X) + "E"   # Values 0 - 10
        elif X >= 10000 and X < 100000: X = str(0) + str(X) + "E"  # Values 10 - 100
        else: X = str(X) + "E" # Values Greater then or equal to 100

        if Y < 0 and Y > -10000: Y = str (0) + str(-1*Y) + "S"     # Values 0--10
        elif Y <= -10000: Y = str(-1*Y) + "S" #Values less then or equal to -10
        elif Y >= 0 and Y < 10000: str(0) + str(Y) + "N" #Values 0-10 including 0
        else: Y = str(Y) + "N" # Values greater then or equal to 10

        row.GLIMSID = "G"+ X + Y # GLIMS ID is concatenated
        glims_values.append(str("G"+ X + Y))
        rows.updateRow(row) # The information is saved for the polygon shapefile (like save edits)
    
    ARCPY.Delete_management(output_wgs84) # Delete temporary re-projected file
    del row     #Delete cursors and remove locks
    del rows
    
    # Get ID count to return. i.e. number of glaciers
    id_count = str(len(glims_values))
    
    # Transfer calculated GLIMS IDs to the original input file
    rows = ARCPY.UpdateCursor (input_file)
    for row in rows:
        row.GLIMSID = glims_values.pop() # pop next value and print it to file.
        rows.updateRow(row) # Update the new entry
    del row #Delete cursors and remove locks
    del rows    
    
    return id_count # Return number of IDs generated


def generate_RGIIDs (input_file):
    """Generate RGI id's for the input table."""
    id_count = 0
    #NOT WRITEN
        #NOT WRITEN
            #NOT WRITEN
    return str(id_count)