"""****************************************************************************
 Name: repair_rgi.repair_rgi
 Purpose: 
 
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
import log
import os
import glob

class rgi_process ():
    
    def __init__ (self, input_folder, output_folder):
        try: import arcinfo #Get ArcInfo License - @UnresolvedImport@UnusedImport
        except: print 'ArcInfo license NOT available'

        try: # Check out Spatial Analyst extension if available.
            if ARCPY.CheckExtension('Spatial') == 'Available':
                ARCPY.CheckOutExtension('Spatial')
                print 'Spatial Analyst is available'
        except: print 'Spatial Analyst extension not available'

        # Set environment
        from arcpy import env                               #@UnresolvedImport
        env.workspace = output_folder

        # Start Log
        __log = log.Log(output_folder)
        __log.print_line("Input: " + input_folder)
        __log.print_line("Output: " + output_folder)
        __log.print_break()
        
        # For each feature class within the input folder...
        for shapefile in glob.glob (os.path.join (input_folder, '*.shp')):
            print os.path.basename(shapefile)
            __log.print_line(os.path.basename(shapefile))
                    
            # Copy feature to workspace (output folder)
            working_shapefile = output_folder + '\\' + os.path.basename(shapefile)
            ARCPY.CopyFeatures_management (shapefile, working_shapefile)

            # Check geometries and repair if needed.
            repair = self.repair_geometry(working_shapefile)
            __log.print_line('   Geometry - ' + repair[0] + ' errors found (Repair ' + repair[2] + ')')
            if repair [2] == 'Run': __log.print_line(('              ' + repair[1] + ' errors found after repair'), True)
            
            # Check for multi-part polygons.
            multi_part = self.check_multipart(working_shapefile, output_folder)
            __log.print_line('   Multi-Part Polygons - ' + multi_part + ' found')
            
            # Check Area for discrepancies
            area = self.check_area(working_shapefile, output_folder)
            __log.print_line('   Area - ' + area[0] + 'Original , ' + area[1] +  'Final area')

            __log.print_break()
            
        print 'Possessing complete.'
            
    def repair_geometry (self, working_shapefile):
        """Repair geometry error and report the number of errors if any."""
        
        check = ARCPY.CheckGeometry_management(working_shapefile) # Check geometry
        first_count = ARCPY.GetCount_management (check) # Number of Errors found.
        ARCPY.Delete_management(check) # Delete count table
        
        if first_count > 0: # If errors are found.
            ARCPY.RepairGeometry_management(working_shapefile)  # Repair Geometry
            
            check = ARCPY.CheckGeometry_management(working_shapefile) # Check geometry
            secound_count = ARCPY.GetCount_management (check) # Number of Errors found.
            ARCPY.Delete_management(check) # Delete count table
            
            return [str(first_count), str(secound_count), 'Run']
        return [str(first_count), str(0), 'NOT Run']
        
        
    def check_multipart (self, working_shapefile, output_folder):
        """Check for multi-part polygons and report how many."""
        original_count = 0
        final_count = 0
        
        rows = ARCPY.UpdateCursor(working_shapefile) #Count features in original Shp
        for row in rows:
            original_count += 1
        del row , rows #Delete cursors and remove locks

        # Run multi_part-to-single_part operation
        output_multipart = output_folder + '\\Multipart.shp'
        ARCPY.MultipartToSinglepart_management(working_shapefile, output_multipart)

        rows = ARCPY.UpdateCursor(output_multipart) #Count features after multi-to-single
        for row in rows:
            final_count += 1
        del row , rows #Delete cursers and remove locks
        ARCPY.Delete_management(output_multipart) # Delete multi-part .shp part results.
        
        return str(final_count - original_count)
    
    
    def check_area (self, working_shapefile, output_folder):
        """check the area values and make sure they are reasonable."""
        original_sum = 0
        final_sum = 0
        
        # Project to Equal Area
        reprojected = output_folder + '\\Reproject.shp'
        projection = os.path.dirname(os.path.abspath(__file__)) + '\\Cylindrical_Equal_Area_world.prj'
        ARCPY.Project_management(working_shapefile, reprojected, projection)
        
        area_shapefile = output_folder + '\\Area_Shapefile.shp'
        ARCPY.CalculateAreas_stats(reprojected, area_shapefile)
        
        rows = ARCPY.SearchCursor(area_shapefile)
        for row in rows:
            original_sum += row.AREA
            final_sum += (row.F_AREA/1000000)
            
        ARCPY.Delete_management(reprojected) # Delete multi-part .shp part results.
        ARCPY.Delete_management(area_shapefile) # Delete multi-part .shp part results.
        
        return [str(original_sum), str(final_sum)]
        
#_______________________________________________________________________________
#***  DRIVER *******************************************************************
# HARD CODE INPUTS HERE !
def driver():
    input_folder = 'A:\\Desktop\\Test'
    output_folder = 'A:\\Desktop\\Ouput'

    rgi_process (input_folder, output_folder)

if __name__ == '__main__':
    driver()