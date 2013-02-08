"""****************************************************************************
 Name:         count.counter
 Purpose:     
 
Created:         Feb 6, 2013
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

import arcpy as ARCPY                                        #@UnresolvedImport
import glacier_utilities.general_utilities.environment as ENV

class rgi_process ():
    
    def __init__ (self, input_file, output_folder):
        
        # Setup working environment
        environment = ENV.setup_arcgis(output_folder)
        workspace = environment.workspace
        __Log = environment.log
        
        # Print run time parameters
        __Log.print_line("Input File: " + input_file)
        __Log.print_line('Output Folder: ' + output_folder)
        __Log.print_break()
        
        #Variables / Things to Count
        number_glaciers = 0
        number_points = 0
        total_area = 0
        
        #Count features in original Shp
        rows = ARCPY.UpdateCursor(input_file) 
        for row in rows:
            
            # Increase the Number of glaciers
            number_glaciers += 1 
            
            # Increase the number of points
            geometry = row.getValue('Shape')
            for part in geometry:
                for point in part:
                    number_points += 1
            
        del row , rows #Delete cursors and remove locks
        
        __Log.print_line("Number of Glaciers: " + str(number_glaciers))
        __Log.print_line("Number of Points: " + str(number_points))
        __Log.print_line("Average Number of Points: " + str(number_points / number_glaciers))
        
        
        
        # Calculate Total Area
        area_shapefile = workspace + '\\Area_Shapefile.shp'
        ARCPY.CalculateAreas_stats(input_file, area_shapefile)
    
        rows = ARCPY.SearchCursor(area_shapefile)
        for row in rows:
            total_area += (row.F_AREA/1000000)
        
        ARCPY.Delete_management(area_shapefile) # Delete Area Statistics .shp part results.
        __Log.print_line("Total Area: " + str(total_area)) 
            
            
        # Script Complete. Try and delete workspace   
        removed = environment.remove_workspace()
        if removed == True:
            __Log.print_break()
            __Log.print_line('Processing Complete')
        else:
            __Log.print_break()
            __Log.print_line('Workspace Could not be deleted')
            __Log.print_line('Processing Complete')
            
            
            
def driver():
    input_file = r'A:\Desktop\Glacier_Counting\Input\Wrangells_Modern.shp'
    output_folder = r'A:\Desktop\Glacier_Counting\Output'

        
    rgi_process (input_file, output_folder)

if __name__ == '__main__':
    driver()