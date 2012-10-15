"""****************************************************************************
 Name: functions_data_prep
 Purpose: To repair any geometry error that may occur and to find errors in
        area calculation, topology and find any multi-part / single-part
        polygons. Module also generates values to populate fields which should
        exist in the input shapefile.
 
Created: Sep 21, 2012
Author:  Justin Rich (justin.rich@gi.alaska.edu)
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
import arcpy as ARCPY                                        #@UnresolvedImport
import os
import math

def repair_geometry (input_file):
    """Repair geometry error and report the number of errors if any."""
    
    check = ARCPY.CheckGeometry_management(input_file) # Check geometry
    first_count = ARCPY.GetCount_management (check) # Number of Errors found.
    ARCPY.Delete_management(check) # Delete count table
    
    ARCPY.RepairGeometry_management(input_file)  # Repair Geometry
    
    check = ARCPY.CheckGeometry_management(input_file) # Check geometry
    secound_count = ARCPY.GetCount_management (check) # Number of Errors found.
    ARCPY.Delete_management(check) # Delete count table
        
    return [str(first_count), str(secound_count)]
    
    
def check_multipart (input_file, workspace):
    """Check for multi-part polygons and report how many."""
    original_count = 0
    final_count = 0
    
    rows = ARCPY.UpdateCursor(input_file) #Count features in original Shp
    for row in rows:
        original_count += 1
    del row , rows #Delete cursors and remove locks

    # Run multi_part-to-single_part operation
    output_multipart = workspace + '\\Multipart.shp'
    ARCPY.MultipartToSinglepart_management(input_file, output_multipart)

    rows = ARCPY.UpdateCursor(output_multipart) #Count features after multi-to-single
    for row in rows:
        final_count += 1
    del row , rows #Delete cursers and remove locks
    ARCPY.Delete_management(output_multipart) # Delete multi-part .shp part results.
    
    return str(final_count - original_count)


def check_area (input_file, workspace):
    """check the area values and make sure they are reasonable."""
    original_sum = 0
    final_sum = 0
    
    # Project to Equal Area
    reprojected = workspace + '\\Reproject.shp'
    projection = os.path.dirname(os.path.abspath(__file__)) + '\\projection\\Cylindrical_Equal_Area_world.prj'
    ARCPY.Project_management(input_file, reprojected, projection)
    
    area_shapefile = workspace + '\\Area_Shapefile.shp'
    ARCPY.CalculateAreas_stats(reprojected, area_shapefile)
    
    rows = ARCPY.SearchCursor(area_shapefile)
    for row in rows:
        original_sum += row.AREA
        final_sum += (row.F_AREA/1000000)
        
    ARCPY.Delete_management(reprojected) # Delete multi-part .shp part results.
    ARCPY.Delete_management(area_shapefile) # Delete multi-part .shp part results.
    
    return [str(original_sum), str(final_sum), str(original_sum-final_sum)]


def check_topology (input_file, workspace):
    """Create Database and check for overlapping features. This function
    is based on one previously created by Christian Kienholz, University
    of Alaska, Fairbanks, 03/2012"""
    # Create Database, add a data set and upload the features
    database = ARCPY.CreateFileGDB_management (workspace, 'database.gdb')
    dataset = ARCPY.CreateFeatureDataset_management (database, 'validation', input_file)
    feature = str(dataset) +'\\feature'
    ARCPY.CopyFeatures_management (input_file, feature)
    
    #Create topology and rules. Add feature to it
    topology = ARCPY.CreateTopology_management (dataset, 'topology_rules')
    ARCPY.AddFeatureClassToTopology_management (topology, feature, 1, 1)
    ARCPY.AddRuleToTopology_management (topology, 'Must Not Overlap (Area)' , feature)
    ARCPY.ValidateTopology_management (topology)
    
    # Export Errors
    ARCPY.ExportTopologyErrors_management (topology, database, 'Errors')
    error_count = ARCPY.GetCount_management (str(database)+ '\\Errors_poly')
    original_count = ARCPY.GetCount_management (input_file)
    
    ARCPY.Delete_management(database) # Delete database

    return [str(error_count), str(original_count)]        


def check_column_formate (input_file):
    """Check that column headings exist, are in the correct order and 
    add if missing. This function utilizes the insert column class and 
    the move column class."""
    
    # Function should check to see if the correct column is included.
    # If it is and it's in the correct location, do nothing
    # If not add it in the correct location.
    # If it is but in the wrong place, move it.
    
    return "function not written yet"


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

        if Y < 0 and Y > -10000: Y = str (0) + str(Y) + "S"     # Values 0--10
        elif Y <= -10000: Y = str(Y) + "S" #Values less then or equal to -10
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


def generate_header (initial_header, max_bin = 8850, min_bin = 0, bin_size = 50):
    """Generate a table list containing table header information by combining
    the initial header information, found in the .var file, with bins, calculated
    here from minimum elevation, maximum elevation and bin size."""
    header = initial_header # Header info given. 
    # Calculate number of bins. A ceiling function is used to ensure that the 
    # number of bins is inclusive so the number does not come up short and rounded to 
    # produce an integer.
    total_bins = round(math.ceil(float(max_bin - min_bin) / float(bin_size)), 0)
    for count in range (0, int(total_bins)):                           
            header.append('B' + str(min_bin + (count * bin_size)))
    return header # List of column headers is returned.