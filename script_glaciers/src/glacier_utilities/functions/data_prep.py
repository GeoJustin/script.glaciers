"""****************************************************************************
 Name: functions_data_prep
 Purpose: To repair any geometry error that may occur and to find errors in
        area calculation, topology and find any multi-part / single-part
        polygons. Module also generates values to populate fields which should
        exist in the input shapefile.
 
Created: Sep 21, 2012
Author:  Justin Rich (justin.rich@gi.alaska.edu)
Location: Geophysical Institute | University of Alaska, Fairbanks
Contributors:  Christian Kienholz, University of Alaska, Fairbanks

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
    ARCPY.Delete_management(area_shapefile) # Delete Area Statistics .shp part results.
    
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


def check_formate (input_file, headings):
    """Check that column headings exist."""
    item_not_found = False
    field_names = [] # Get input file field names
    
    fields_list = ARCPY.ListFields(input_file)
    for field in fields_list: # Loop through the field names
        if not field.required: # If they are not required 
            field_names.append(field.name) # Append them to the list of field names.

    not_found = '' # Return a list of items not found
    for item in headings: # Look for each item in headings list
        if item[0] not in field_names: # If item is not found 
            item_not_found = True # Set not found to true
            not_found += item[0] + ', ' # Add to the list of items not found
            
    return item_not_found, not_found


def generate_bin_header (max_bin = 8850, min_bin = 0, bin_size = 50):
    """Generate a table list containing table header information by combining
    the initial header information, found in the .var file, with bins, calculated
    here from minimum elevation, maximum elevation and bin size."""
    bin_header = []
    # Calculate number of bins. A ceiling function is used to ensure that the 
    # number of bins is inclusive so the number does not come up short and rounded to 
    # produce an integer.
    total_bins = round(math.ceil(float(max_bin - min_bin) / float(bin_size)), 0)
    for count in range (0, int(total_bins)):                           
            bin_header.append('B' + str(min_bin + (count * bin_size)))
    return bin_header # List of column headers is returned.