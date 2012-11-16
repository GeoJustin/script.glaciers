"""****************************************************************************
 Name: repair_rgi.repair_rgi
 Purpose: To repair any geometry error that may occur and to find errors in
        area calculation, topology and find any multi-part / single-part polygons
 
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
import os
import sys
import glob
import arcpy as ARCPY                                        #@UnresolvedImport
import glacier_utilities.functions.data_prep as DP
import glacier_utilities.output_file.output_file_log as LOG
import glacier_utilities.general_utilities.variables as VAR

class rgi_process ():
    
    def __init__ (self, input_folder, output_folder, variables):
        
        try: # Start Log file and write it to the output folder
            log_path = os.path.dirname(os.path.abspath(output_folder))
            __Log = LOG.Log(log_path)
        except:
            print 'Log file could not be written to the output folder.'
            sys.exit()
        
        try:  # Get ArcInfo License if it's available
            import arcinfo                          #@UnresolvedImport @UnusedImport
        except:
            __Log.print_line('ArcInfo license NOT available')
            sys.exit()

        try: # Check out Spatial Analyst extension if available.
            if ARCPY.CheckExtension('Spatial') == 'Available':
                ARCPY.CheckOutExtension('Spatial')
                __Log.print_line('Spatial Analyst is available')
        except: 
            __Log.print_line('Spatial Analyst extension not available')
            sys.exit()

        try: # Set environment
            workspace = output_folder + '\\workspace'
            os.makedirs(workspace) # Create Workspace
            ARCPY.env.workspace = workspace
        except:
            __Log.print_line('WARNING - Workspace folder already exists.')
            sys.exit()

        # Read variables
        check_header = variables.read_variable('RGIHEADER')

        # Print run time parameters
        __Log.print_line("Input File: " + input_folder)
        __Log.print_line('Output Folder: ' + output_folder)
        __Log.print_line('RGI Header to Match: ')
        __Log.print_line('   ' + str(check_header))
        __Log.print_break()
        
        # For each feature class within the input folder...
        for shapefile in glob.glob (os.path.join (input_folder, '*.shp')):
            __Log.print_line(os.path.basename(shapefile))
                    
            # Copy feature to workspace (output folder)
            working_shapefile = output_folder + '\\' + os.path.basename(shapefile)
            ARCPY.CopyFeatures_management (shapefile, working_shapefile)


            # Check to see if the input file follows RGI table headings.
            formate_error, not_found = DP.check_formate(working_shapefile, check_header)
            if formate_error == False:
                __Log.print_line('    Input header information is consistent with the standard set')
            if formate_error == True:
                __Log.print_line('    ERROR - Input header information is NOT consistent with the standard set')
                __Log.print_line('        Items not found: ' + not_found)
                
            # Check geometries. If there are errors, correct them and print the
            # results to the log file
            repair = DP.repair_geometry(working_shapefile)
            __Log.print_line('    Geometry - ' + repair[0] + ' errors found (Repaired ' + repair[1] + ')')
               
            # Check to see if there are any multi-part polygons in the input file. If
            # so, prompt the user to stop and correct. Print to log file.
            multipart = DP.check_multipart(working_shapefile, workspace) # Check for multi-part Polygons
            __Log.print_line('    Multi-Part Polygons - ' + multipart + ' found')
            
            # Check to see if the area from the AREA column matches the actual area
            # calculated. If not signal the user to correct. Print results to log.
            area = DP.check_area(working_shapefile, workspace)
            __Log.print_line('    Area - ' + area[2] + ' difference')
            __Log.print_line('        Original area: ' + area[0] + ' , Final area: ' + area[1], True)
            
            # Check to see if there are any topology errors in the input file. If there 
            # are signal the user to correct before moving forward. Print to log.
            topology = DP.check_topology(working_shapefile, workspace)
            __Log.print_line('    Topology - ' + topology[0] + ' errors on ' + topology[1] + ' features')
            __Log.print_line('        Rule set - Must Not Overlap (Area)', True)
           
            __Log.print_break() # Break for next section in the log file.
            
        try: # Script Complete. Try and delete workspace 
            ARCPY.Delete_management(workspace)
            __Log.print_break()
            __Log.print_line('Processing Complete')
        except: 
            __Log.print_break()
            __Log.print_line('Workspace Could not be deleted')
            __Log.print_line('Processing Complete')
        
#_______________________________________________________________________________
#***  DRIVER *******************************************************************
# HARD CODE INPUTS HERE !

def driver():
    input_folder = r'A:\Desktop\TestDataPrep\Output\Input'
    output_folder = r'A:\Desktop\TestDataPrep\Output\Output'

    import glacier_utilities.general_utilities.variables  as variables
    VAR = variables.Variables()
        
    rgi_process (input_folder, output_folder, VAR)

if __name__ == '__main__':
    driver()