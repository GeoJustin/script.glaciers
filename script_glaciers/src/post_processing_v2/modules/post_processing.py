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
import log
import os
import data_prep as DP
        
class process ():
    
    def __init__ (self, Input, Output, DEM, Workspace, binSize, minBin, maxBin):
        
        try: import arcinfo # Get ArcInfo License - @UnresolvedImport @UnusedImport
        except: print 'ArcInfo license NOT available'

        try: # Check out Spatial Analyst extension if available.
            if ARCPY.CheckExtension('Spatial') == 'Available':
                ARCPY.CheckOutExtension('Spatial')
                print 'Spatial Analyst is available'
        except: print 'Spatial Analyst extension not available'

        # Set environment
        ARCPY.env.workspace = Workspace
                
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
        multipart = DP.check_multipart(input_copy, Workspace) # Check for multi-part Polygons
        __Log.print_line('   Multi-Part Polygons - ' + multipart + ' found')
        
        # Check to see if the area from the AREA column matches the actual area
        # calculated. If not signal the user to correct. Print results to log.
        print '     Checking Area'
        area = DP.check_area(input_copy, Workspace)
        __Log.print_line('   Area - ' + area[2] + ' difference')
        __Log.print_line('                   ' + 'Original area: ' + area[0] + ' , Final area: ' + area[1], True)
        
        # Check to see if there are any topology errors in the input file. If there 
        # are signal the user to correct before moving forward. Print to log.
        print '     Checking Topology'
        topology = DP.check_topology(input_copy, Workspace)
        __Log.print_line('   Topology - ' + topology[0] + ' errors on ' + topology[1] + ' features')
        __Log.print_line('                   Rule set - Must Not Overlap (Area)', True)
        
        # Warnings: 
        if multipart <> str(0): print "WARNING:  Multi-part features found.."
        if area [2] > 1 or area[2] < -1: 'WARNING: The AREA difference exceeds the threshold.'
        if topology[0] <> str(0): raw_input(str(topology[0]) + "WARNING: Topology errors found.")
       
        __Log.print_break() # Break for next section in the log file.
     
        #_______________________________________________________________________
        #*******Prepare Input file*********************************************
        print 'Generating Glacier IDs'
        glims_ids = DP.generate_GLIMSIDs(input_copy, Workspace) # Copy to Output
        __Log.print_line('   GLIMS IDs - ' + glims_ids + ' GLIMS IDs Generated')
        
        
        

        print 'Processing Complete'
#_______________________________________________________________________________
#***  DRIVER *******************************************************************
# HARD CODE INPUTS HERE !
def driver():
    Input = r'A:\Desktop\TestDataPrep\TestGlaciers.shp'
    Output = r'A:\Desktop\TestDataPrep\Output\TestGlacier_Out.shp'
    Workspace = r'A:\Desktop\TestDataPrep\Workspace'
    DEM = r''
    #Bins - Bin size based on DEM elevation units
    binSize = 50 #Meters
    #Bin measured from base bin elevation i.e. 8800 is 8800-8850
    maxBin = 8800 #Based on Everest.
    minBin = 0

    process (Input, Output, DEM, Workspace, binSize, minBin, maxBin)

if __name__ == '__main__':
    driver()