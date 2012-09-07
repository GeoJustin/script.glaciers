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
import arcpy                                                #@UnresolvedImport
import log
import os
        
class process ():
    
    def __init__ (self, Input, Output, DEM, Workspace, binSize, minBin, maxBin):
        
        try: import arcinfo # Get ArcInfo License - @UnresolvedImport @UnusedImport
        except: print 'ArcInfo license NOT available'

        try: # Check out Spatial Analyst extension if available.
            if arcpy.CheckExtension('Spatial') == 'Available':
                arcpy.CheckOutExtension('Spatial')
                print 'Spatial Analyst is available'
        except: print 'Spatial Analyst extension not available'

        # Set environment
        from arcpy import env                               #@UnresolvedImport
        env.workspace = Workspace
        
        # Try and clear the workspace in case there are files in it.
        self.clearWorkspace(Workspace)
                
        # Start Log
        __Log = log.Log(Output)
        __Log.printBreak()
        __Log.printLine("Input: " + os.path.basename(Input))
        __Log.printLine("DEM: " + os.path.basename(DEM))
        __Log.printLine("Output: " + Output)
        __Log.printBreak()
        
        #*******Input File Cleanup**********************************************
        print 'Checking input polygons'
        print '     Checking geometry'
        arcpy.RepairGeometry_management(Input)  # Repair Geometry
        
        #Check for multi-part Polygons
        print '     Check for multi-part polygons'
        rows = arcpy.UpdateCursor(Input) #Count features in original Shp
        originalCount = 0
        for row in rows:
            originalCount += 1
        del row , rows #Delete cursors and remove locks

        __output_multipart = Workspace + '\\Multipart.shp'
        arcpy.MultipartToSinglepart_management(Input, __output_multipart)

        rows = arcpy.UpdateCursor(__output_multipart) #Count features after multi-to-single
        finalCount = 0
        for row in rows:
            finalCount += 1
        del row , rows #Delete cursers and remove locks

        if originalCount <> finalCount:
            __Log.printLine ('Multi-part features found')
            raw_input("Features are not single part. Stop script and run multipart to single part on features.")

        else:
            print '          No multi-part features found'
            __Log.printLine ('No multi-part features found')
            __Log.printBreak()

        #Try and clear the workspace in case there are files in it.
        self.clearWorkspace(Workspace)
        
        #_______________________________________________________________________
        #*******Input File Cleanup**********************************************
        print 'Generating Glacier IDs'

        arcpy.AddField_management(Input, 'Lat', 'DOUBLE')
        arcpy.AddField_management(Input, 'Lon', 'DOUBLE')
        
        # Create a copy of the input in WGS 84 for calculating Lat. / Lon.
        output_wgs84 = Output + "\\" + os.path.basename(os.path.splitext(Input)[0]) + "_WGS84.shp"
        projectioned = os.path.dirname(os.path.abspath(__file__)) + '\\WGS1984.prj'
        arcpy.Project_management(Input, output_wgs84, projectioned)
        
        
        
#_______________________________________________________________________________
#***  DRIVER *******************************************************************
# HARD CODE INPUTS HERE !
def driver():
    Input = 'C:\\Users\\glaciologist\\Desktop\\GINAFY\\Input\\GlacierBay_DRGs.shp'
    Output = 'C:\\Users\\glaciologist\\Desktop\\TestOut'
    Workspace = 'X:\\Programs\\PostProcess\\Workspace'
    DEM = 'C:\Users\glaciologist\Desktop\GINAFY\DEMs\DEM_NED_Albers.tif'
    #Bins - Bin size based on DEM elevation units
    binSize = 50 #Meters
    #Bin measured from base bin elevation i.e. 8800 is 8800-8850
    maxBin = 8800 #Based on Everest.
    minBin = 0

    process (Input, Output, DEM, Workspace, binSize, minBin, maxBin)

if __name__ == '__main__':
    driver()