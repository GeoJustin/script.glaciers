"""****************************************************************************
 Name: post_processing_v2
 Purpose: 
 
Created: Aug 24, 2012
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
import arcpy as ARCPY                                         #@UnresolvedImport
import functions_data_prep as DP
import functions_data_calc as DC
import log
import csv
import os

class process ():
    
    def __init__ (self, Input, Output, DEM, workspace, variables):
        
        try: import arcinfo # Get ArcInfo License - @UnresolvedImport @UnusedImport
        except: print 'ArcInfo license NOT available'

        try: # Check out Spatial Analyst extension if available.
            if ARCPY.CheckExtension('Spatial') == 'Available':
                ARCPY.CheckOutExtension('Spatial')
                print 'Spatial Analyst is available'
        except: print 'Spatial Analyst extension not available'

        # Set environment
        ARCPY.env.workspace = workspace
                
        # Start Log
        log_path = os.path.dirname(os.path.abspath(Output))
        __Log = log.Log(log_path)
        __Log.print_break()
        __Log.print_line("Input File: " + os.path.basename(Input))
        __Log.print_line("Input DEM: " + os.path.basename(DEM))
        __Log.print_line('Output Folder: ' + os.path.dirname(os.path.abspath(Output)))
        __Log.print_line("Output File: " + os.path.basename(Output))
        __Log.print_break()
        
        # Create a copy of the input file in the output folder. This will be the
        # actual result file after fields are updated. This is done so no changes
        # are imposed on the original file.
        input_copy = ARCPY.CopyFeatures_management(Input, Output)
        """
        #_______________________________________________________________________
        #*******Input File Cleanup**********************************************   
        print 'Checking input polygons'
        print '     Checking geometry'
        # Check geometries. If there are errors, correct them and print the
        # results to the log file
        repair = DP.repair_geometry(input_copy)
        __Log.print_line('   Geometry - ' + repair[0] + ' errors found (Repaired ' + repair[1] + ')')
           
        # Check to see if there are any multi-part polygons in the input file. If
        # so, prompt the user to stop and correct. Print to log file.
        print '     Checking for Multi-part Polygons'
        multipart = DP.check_multipart(input_copy, workspace) # Check for multi-part Polygons
        __Log.print_line('   Multi-Part Polygons - ' + multipart + ' found')
        
        # Check to see if the area from the AREA column matches the actual area
        # calculated. If not signal the user to correct. Print results to log.
        print '     Checking Area'
        area = DP.check_area(input_copy, workspace)
        __Log.print_line('   Area - ' + area[2] + ' difference')
        __Log.print_line('                   ' + 'Original area: ' + area[0] + ' , Final area: ' + area[1], True)
        
        # Check to see if there are any topology errors in the input file. If there 
        # are signal the user to correct before moving forward. Print to log.
        print '     Checking Topology'
        topology = DP.check_topology(input_copy, workspace)
        __Log.print_line('   Topology - ' + topology[0] + ' errors on ' + topology[1] + ' features')
        __Log.print_line('                   Rule set - Must Not Overlap (Area)', True)
        
        # Warnings: 
        if multipart <> str(0): print "WARNING:  Multi-part features found.."
        if area [2] > 1 or area[2] < -1: 'WARNING: The AREA difference exceeds the threshold.'
        if topology[0] <> str(0): raw_input(str(topology[0]) + "WARNING: Topology errors found.")
       
        __Log.print_break() # Break for next section in the log file.
        """
        #_______________________________________________________________________
        #*******Prepare Input file*********************************************
        print 'Generating Glacier IDs'
        glims_ids = DP.generate_GLIMSIDs(input_copy, workspace) # Copy to Output
        __Log.print_line('   GLIMS IDs - ' + glims_ids + ' GLIMS IDs Generated')
        
          
        #_______________________________________________________________________
        #*******Calculate Statistics********************************************
        
        # Create output table header information to populate the tables with
        table_output = os.path.dirname(os.path.abspath(Output))
        header = variables.read_variable('RGITABLE')
        max_bin = variables.read_variable('MAXBIN')
        min_bin =  variables.read_variable('MINBIN')
        bin_size = variables.read_variable('BINSIZE')
        table_header = DP.generate_header(header, max_bin, min_bin, bin_size)
        
        # Read other variables
        scaling = variables.read_variable('SCALING')
        z_value = variables.read_variable('ZVALUE')

        # Create an instance of each table
        hypso_csv = csv.csv(table_output, 'Stats_Hypsometry', table_header)
        slope_csv = csv.csv(table_output, 'Stats_Slope', table_header)
        aspect_csv = csv.csv(table_output, 'Stats_Aspect', table_header)

        rows = ARCPY.SearchCursor(input_copy) # Open shapefile to read features
        for row in rows: # For each feature in the shapefile
            
            # Get Attributes information such as GLIMS ID, Lat, Lon, area... etc.
            attribute_info, attribute_error = DC.get_attributes(row)  
            if attribute_error == True: # If function failed
                print ' - ERROR - Could not read attributes' # Print Error to prompt and log file
                __Log.print_line(str(row.GLIMSID) + ' - ERROR - Could not read attributes')
            
            # Subset the DEM based on a single buffered glacier outline
            subset, subset_error = DC.subset(row, DEM, workspace, 2)
            if subset_error == True: # If function failed
                print 'ERROR - Could not subset feature' # Print Error to prompt and log file
                __Log.print_line(str(row.GLIMSID) + ' - ERROR - Could not subset feature')
            
            # Get basic statistics such as minimum elevation, mean... etc.
            statistics_info, statistics_error = DC.get_statistics(row, subset, workspace, scaling) 
            if statistics_error == True: # If function failed
                print 'ERROR - Could not generate basic statistics' # Print Error to prompt and log file
                __Log.print_line(str(row.GLIMSID) + ' - ERROR - Could not generate basic statistics')
            
            hypsometry_info, hypso_error, bin_mask = DC.get_hypsometry(row, subset, workspace, scaling, max_bin, min_bin, bin_size)
            if hypso_error == True:
                print 'ERROR - Could not generate hypsometry data'
                __Log.print_line('ERROR - Could not generate hypsometry data')
            
            slope_info, slope_error = DC.get_slope(row, subset, bin_mask, workspace, scaling, z_value, max_bin, min_bin, bin_size)
            #'ERROR - Could not generate binned aspect data'
            aspect_info, aspect_error = DC.get_aspect(row, subset, bin_mask, max_bin, min_bin, bin_size) 
            #'ERROR - Could not generate binned slope data'
            
    
            print hypso_csv.get_rows(), row.GLIMSID, subset_error, statistics_error, hypso_error, slope_error, aspect_error
            
            # Print row data to csv files as appropriate. 
            hypso_csv.print_line(attribute_info + statistics_info + hypsometry_info)
            slope_csv.print_line(attribute_info + statistics_info + slope_info)
            aspect_csv.print_line(attribute_info + statistics_info + aspect_info)
            
            try: ARCPY.Delete_management(subset)
            except: pass
            
        del row , rows #Delete cursors and remove locks
        
        print 'Processing Complete'
#_______________________________________________________________________________
#***  DRIVER *******************************************************************
# HARD CODE INPUTS HERE !
def driver():
    Input = r'A:\Desktop\TestDataPrep\TestGlaciers.shp'
    Output = r'A:\Desktop\TestDataPrep\Output\TestGlacier_Out.shp'
    Workspace = r'A:\Desktop\TestDataPrep\Workspace'
    DEM = r'A:\Desktop\TestDataPrep\Test_DEM.img'
    
    #Variables - WARNING: Use caution manually changing variables.
    import variables
    variables = variables.Variables()

    process (Input, Output, DEM, Workspace, variables)

if __name__ == '__main__':
    driver()