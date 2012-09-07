"""-----------------------------------------------------------------------------
 Name:        GINA_Statistics
 Purpose:     Calculates statistics for the 'Process for GINA' program.

 Author:      glaciologist

 Created:     08/26/2011
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
import arcpy, numpy                                             #@UnresolvedImport

class CompileBins ():

    def __init__ (self, Input, Output, DEM, Workspace, binSize, maxBin, minBin, originalCount, __Log):

        __Log.printLine ('Starting Hypsometry')

        print 'Creating output bin file...'
        __output = self.__createCSV(Output, (maxBin/binSize)+1, binSize, minBin)

        XCellSize = self.__getStat(DEM, 'CELLSIZEX')
        YCellSize = self.__getStat(DEM, 'CELLSIZEY')
        __cellArea = float(XCellSize) * float(YCellSize)

        print 'Input raster cell size: ' + XCellSize + ' x ' + YCellSize

        __countPercent = 0
        rows = arcpy.UpdateCursor(Input)
        for row in rows:

            #Extract Feature. This should not be needed but for some reason geometry
            #is sometimes lost with the extract if this doesn't exist.
            query =  ' \"ID\" = ' + " \'" + str(row.ID) + "\' "
            Feature = arcpy.Select_analysis(Input, Workspace + '\\Feature.shp', query)


            #Currently processing ---------------
            print 'Hypsometry ' + str(round((float(__countPercent) / float(originalCount)*100),1)) + '% Complete'
            __countPercent += 1
            print 'Feature ' + str(row.id) + ' '+ str(row.Name) + ' - Code: ' + str(row.Code)
            print '   Area: ' + str(row.Area) + ' Sqr.'
            print '   Centroid (DD): ' + str(row.Lat) + ', ' + str(row.Lon)
            #Find the Centroid Point
            featureCenter = row.getValue(arcpy.Describe(Input).shapeFieldName)
            print '   Centroid (Meters):' + str(featureCenter.centroid.X) + ', ' + str(featureCenter.centroid.Y)


            try:
            #Extract----------
                __exportRaster = Workspace + '\\ExtractRaster.img'
                extracted = arcpy.sa.ExtractByMask (DEM, Feature)
                extracted.save(__exportRaster)

            except:
                print 'FEATURE FAILED - Could Not Extract Raster (Bin Statistics).'
                __Log.printLine (str(row.id) + 'FEATURE FAILED - Could Not Extract Raster (Bin Statistics).')

            #-------------------------Bin Processing----------------------------
            #An array with the number of bins plus 6 header-like fields
            #Convert to Numpy Array.

            __binStats = numpy.zeros ([(maxBin/binSize) + 12], dtype = numpy.object)

            #Copy Statistics
            try:
                __binStats [0] = row.id
                __binStats [1] = row.Name
                __binStats [2] = str(row.Code)
                __binStats [3] = row.Date
                __binStats [4] = row.Lat
                __binStats [5] = row.Lon
                __binStats [6] = row.Area
            except:
                print "FEATURE FAILED - Could not copy statistics."
                __Log.printLine (str(row.id) + 'FEATURE FAILED - Could not copy statistics.')

            #Get Minimum and Maximum
            try:
                __binStats [7] = round(float(self.__getStat(extracted, 'MINIMUM')),0)
                __binStats [8] = round(float(self.__getStat(extracted, 'MAXIMUM')),0)
            except:
                print "FEATURE FAILED - Could not get Minimum & Maximum."
                __Log.printLine (str(row.id) + 'FEATURE FAILED - Extract and Basic Statistics.')

            #Calculate Median and Mean
            try:
                __raster = arcpy.RasterToNumPyArray(__exportRaster, '', '', '', -9999)
                maskedRaster = numpy.ma.masked_equal (__raster, -9999)
                __binStats [9] = round(numpy.ma.median(maskedRaster),0)
                __binStats [10] =  round(maskedRaster.mean(),0)
                del __raster, maskedRaster
                print '     Mean: '+ str(__binStats [10]) + ' & Median: ' + str(__binStats [9])
                print '     Min: '+ str(__binStats [7]) + ' & Max: ' + str(__binStats [8])
                print '     Processing bin statistics...'
            except:
                print "FEATURE FAILED - Could not get Median & Mean."
                __Log.printLine (str(row.id) + 'FEATURE FAILED - Could not get Median & Mean.')

            #Calculate Bin Statistics.
            try:
                reclassifyRanges ="0.0 50.0 0;"
                for __bin in range (1, (maxBin/binSize)+1):
                    low = str(__bin * binSize * 1.0)
                    high = str((__bin + 1) * binSize * 1.0)
                    value = str(__bin)
                    reclassifyRanges += low + " " + high + " " + value + ";"

                __reclassified = arcpy.sa.Reclassify (extracted, "Value", reclassifyRanges, "NODATA")
                __reclassified.save(Workspace+'\\tempReclass.tif') #It tends to get ahead of itself if this is not here

                binRows = arcpy.SearchCursor (__reclassified)
                for binrow in binRows:
                    value = binrow.getValue ('VALUE')
                    count = binrow.getValue ('COUNT')
                    __binStats [value + 11] = round((count * __cellArea),0)

                try: del binrow, binRows #Delete cursors and remove locks
                except: pass

                print ''

            except:
                print 'FEATURE FAILED - Bin Statistics.'
                __Log.printLine (str(row.id) + 'FEATURE FAILED - Bin Statistics.')
                print ''

            self.__printLine(__output, (maxBin/binSize) + 12, __binStats)

            try: arcpy.Delete_management(__reclassified)
            except: pass

            try: arcpy.Delete_management(__exportRaster)
            except: pass

            try: arcpy.Delete_management(Feature)
            except: pass

        del row , rows #Delete cursors and remove locks

        print 'Bin Statistics Generated'
        __Log.printLine ('End Hypsometry')
        __Log.printBreak()


#_______________________________________________________________________________
#***FUNCTIONS*******************************************************************
    def __getStat (self, raster, stat):
        """Return the desired statistics from the input raster layer"""
        return str(arcpy.GetRasterProperties_management(raster, stat))


    #PRINTING
    def __createCSV (self, Output, bins, binSize, minBin):
        """Print a CSV file with header along the top."""
        outputFile = open ((Output), 'w')
        header = 'ID, Name, Code, Date, Latitude, Longitude, Area, Elev_Min, Elev_Max, Median, Mean'
        interval = minBin
        for entry in range (0, bins):                           #@UnusedVariable
            header += ',B' + str(interval)
            interval += binSize
        outputFile.write(header + '\n')
        return outputFile

    def __printLine (self, outputFile, bins, binStats):
        """Print to a CSV file with year on the left and month along the top."""
        printLine = ''
        for binNumber in range (bins):
            printLine += str(binStats[binNumber]) + ','
        outputFile.write(printLine + '\n')
