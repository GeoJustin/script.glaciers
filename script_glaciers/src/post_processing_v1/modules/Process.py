"""-----------------------------------------------------------------------------
 Name:        GINA_Process
 Purpose:     Controls the processing for the 'Process for GINA' program.

 Author:      glaciologist

 Created:     26/08/2011
 Copyright:   (c) glaciologist 2011

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
-----------------------------------------------------------------------------"""
#!/usr/bin/env python
import os, shutil                                   
import arcpy                                                #@UnresolvedImport

class process ():

    def __init__ (self, Input, Output, DEM, Projection, Workspace, checkGLIMS, checkGINA, checkStats):


        try: import arcinfo #Get ArcInfo License - @UnresolvedImport @UnusedImport
        except: print 'ArcInfo license NOT available'

        try: #Check out Spatial Analyst extension if available.
            if arcpy.CheckExtension('Spatial') == 'Available':
                arcpy.CheckOutExtension('Spatial')
                print 'Spatial Analyst is available'
        except: print 'Spatial Analyst extension not available'

        #Set environment
        from arcpy import env                               #@UnresolvedImport
        env.workspace = Workspace

        #Start Log
        import Log
        __Log = Log.log(Output)
        __Log.printBreak()
        __Log.printLine("Input: " + os.path.basename(Input))
        __Log.printLine("DEM: " + os.path.basename(DEM))
        __Log.printLine("Output: " + Output)
        __Log.printBreak()

        #Try and clear the workspace incase there are files in it.
        self.clearWorkspace(Workspace)


#_______________________________________________________________________________
#*******Input File Cleanup******************************************************

        # Repair Geometry
        print 'Checking input polygons'
        print '     Checking geometry'
        arcpy.RepairGeometry_management(Input)

        #Check for multi-part Polygons
        print '     Check for multi-part polygons'
        rows = arcpy.UpdateCursor(Input) #Count features in original Shp
        originalCount = 0
        for row in rows:
            originalCount += 1
        del row , rows #Delete cursors and remove locks

        __outputMultipart = Workspace + '\\Multipart.shp'
        arcpy.MultipartToSinglepart_management(Input, __outputMultipart)

        rows = arcpy.UpdateCursor(__outputMultipart) #Count features after multi-to-single
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

#_______________________________________________________________________________
#*******Create Glacier ID's*****************************************************
        print 'Generating Glacier IDs'

        arcpy.AddField_management(Input, 'Lat', 'DOUBLE')
        arcpy.AddField_management(Input, 'Lon', 'DOUBLE')

        rows = arcpy.UpdateCursor(Input)
        for row in rows:
            #Find the Centroid Point
            featureCenter = row.getValue(arcpy.Describe(Input).shapeFieldName)
            X = int((featureCenter.centroid.X) * 1000)
            Y = int((featureCenter.centroid.Y) * 1000)

            if X < 0: X = str(-1 * X) + "W"
            else: X = str(X) + "E"

            if Y < 0: Y = str(-1 * Y) + "S"
            else: Y = str(Y) + "N"

            row.id = "G"+ X + Y #GLIMS ID is concatenated
            row.Lat = featureCenter.centroid.Y #Temp. Field
            row.Lon = featureCenter.centroid.X #Temp. Field

            rows.updateRow(row) # The information is saved for the polygon shapefile (like save edits)

        #Delete cursors and remove locks
        del row
        del rows

#_______________________________________________________________________________
#*******Create GLIMS Output*****************************************************

        if checkGLIMS == 1:

            print 'GLIMS code not written'
            #GLIMS stuff goes here.

#_______________________________________________________________________________
#*******Create GINA Output******************************************************
        if checkGINA == 1:

            print 'Generating GINA Files.'
            print ''
            __Log.printLine ('Starting GINA Processing')

            #Create a directory to store GINA files in.
            GINADirectory = Output + "\\GINA\\"
            try:
                os.mkdir(GINADirectory)
            except:
                print 'Directory already exists:'
                print GINADirectory
                raw_input("Script is Complete. Have a nice day!")
                import sys
                sys.exit()

            #Create Base file name (i.e. base + _GINA.shp, base + _Stats.csv... etc.)
            __output = GINADirectory + os.path.basename(os.path.splitext(Input)[0])

            __outputGINA = __output + '_GINA.shp'
            arcpy.Project_management(Input, __outputGINA, Projection, 'NAD_1983_To_WGS_1984_1')

            #-------Create Statistics & Bins------------------------------------
            if checkStats == 1:
                #Bins - Bin size based on DEM elevation units
                binSize = 50 #Meters
                #Bin measured from base bin elevation i.e. 8800 is 8800-8850
                maxBin = 8800 #Based on Everest.
                minBin = 0
                __Log.printLine('Hypsometry Bin Size: ' + str(binSize))
                __Log.printLine('Hypsometry Max Bin: ' + str(maxBin))
                __Log.printLine('Hypsometry Min Bin: ' + str(minBin))

                import GINA_Statistics
                __outputBinFile = __output + '_BinStats.csv'
                GINA_Statistics.CompileBins(__outputGINA, __outputBinFile, DEM, Workspace, binSize, maxBin, minBin, originalCount, __Log)

                #Try and clear the workspace in case there are files in it.
                self.clearWorkspace(Workspace)

        __Log.printBreak()
        __Log.printLine('All Processing Complete')

#_______________________________________________________________________________
#*******Final Clean up**********************************************************
        #Drop Lat & Lon Fields.
        print "Removing Lat & Lon fields."
        arcpy.DeleteField_management(Input, ["Lat", "Lon"])

        #Try and clear the workspace in case there are files in it.
        self.clearWorkspace(Workspace)

        raw_input("Script is Complete. Have a nice day!")

#_______________________________________________________________________________
#***FUNCTIONS*******************************************************************
    def clearWorkspace (self, Workspace):
        """Purpose - Removes all files from the workspace. Used to periodically
        clear the workspace of unneeded potentially troublesome data"""
        try:
            for dirname, dirnames, filenames in os.walk(Workspace):
                for files in filenames:
                    os.remove(os.path.join(dirname, files))
                for subdirectories in dirnames:
                    shutil.rmtree(os.path.join(dirname, subdirectories))
        except:
            pass



#_______________________________________________________________________________
#***  DRIVER *******************************************************************
# HARD CODE INPUTS HERE !
def driver():
    Input = 'C:\\Users\\glaciologist\\Desktop\\GINAFY\\Input\\GlacierBay_DRGs.shp'
    Output = 'C:\\Users\\glaciologist\\Desktop\\TestOut'
    Projection = 'X:\\Programs\\PostProcess\\Projection\\NAD_1983_Alaska_Albers.prj'
    Workspace = 'X:\\Programs\\PostProcess\\Workspace'
    DEM = 'C:\Users\glaciologist\Desktop\GINAFY\DEMs\DEM_NED_Albers.tif'
    checkGLIMS = 0
    checkGINA = 1
    checkStats = 1

    process (Input, Output, DEM, Projection, Workspace, checkGLIMS, checkGINA, checkStats)

if __name__ == '__main__':
    driver()