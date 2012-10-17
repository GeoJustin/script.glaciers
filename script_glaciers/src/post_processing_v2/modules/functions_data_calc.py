"""****************************************************************************
 Name: functions_data_calc
 Purpose: The purpose of this module is to hold the post proccess functions 
     that deal with calculation of statistics including hypsometry, slope
     and aspect information. 
 
Created: Oct 12, 2012
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

def get_aspect (feature, dem, max_bin = 8850, min_bin = 0, bin_size = 50):
    """Calculate aspect information from the given aspect raster generated from 
    a DEM and return bin statistics. Each aspect bin is defined by elevation
    and shares the same spatial area is hypsometry bins. If this function 
    fails at runtime an error is returned for recording in the log file."""
    slope = []
    try:
        # NOT WRITTEN 
        # NOT WRITTEN 
        return slope, False
    except:
        return 'ERROR - Could not generate binned aspect data', True
    

def get_attributes (feature):
    """Return feature attribute values: GLIMSID, NAME, GLACTYPE, BGNDATE, 
    ENDDATE, CENLON, CENLAT and AREA. If value doesn't exist it should be
    left blank. If this function fails at runtime an error is returned for
    recording in the log file."""
    attributes = []
    try:
        attributes.append(str(feature.GLIMSID))
        attributes.append(str(feature.NAME))
        attributes.append(str(feature.GLACTYPE))
        attributes.append(str(feature.BGNDATE))
        attributes.append(str(feature.ENDDATE))
        attributes.append(str(feature.CENLON))
        attributes.append(str(feature.CENLAT))
        attributes.append(str(feature.AREA))
        return attributes
    except:
        return 'ERROR'
    

def get_hypsometry (feature, dem, max_bin = 8850, min_bin = 0, bin_size = 50):
    """Calculate hypsometry information from the given digital elevation model
    (DEM) and return bin statistics. If this function fails at runtime an error
    is returned for recording in the log file."""
    hypsometry = []
    try:
        # NOT WRITTEN 
        # NOT WRITTEN 
        return hypsometry, False
    except:
        return 'ERROR - Could not generate hypsometry data', True

    
def get_properties (raster, prop = ''):
    """Return the desired property from the input raster layer. These include:
    MINIMUM, MAXIMUM, MEAN, STD, ... etc."""
    return str(ARCPY.GetRasterProperties_management(raster, prop))


def get_slope (feature, dem, max_bin = 8850, min_bin = 0, bin_size = 50):
    """Calculate slope information from the given slope raster generated from 
    a DEM and return bin statistics. Each slope bin is defined by elevation
    and shares the same spatial area is hypsometry bins. If this function 
    fails at runtime an error is returned for recording in the log file."""
    aspect = []
    try:
        # NOT WRITTEN 
        # NOT WRITTEN 
        return aspect, True
    except:
        return 'ERROR - Could not generate binned slope data' , False
        
        
def get_statistics (feature, dem):
    """Return basic feature statistics which include elevation maximum, 
    elevation minimum, median elevation and mean elevation. If this function
    fails at runtime an error is returned for recording in the log file."""
    statistics = []
    try:
        # NOT WRITTEN 
        # NOT WRITTEN 
        return statistics, False
    except:
        return 'ERROR - Could not generate basic statistics', True
        

def subset (feature, raster, workspace, buffer_scale = 2):
    """Subset a raster based on an input features boundaries plus a buffer
    which should be greater then the size of the pixels in the given raster.
    This is to ensure there are no gaps between where the raster ends and the
    input feature begins. Any excess raster will be clipped later after it is
    converted to a feature class."""
    subset = workspace + '\\' + 'raster_subset_' + str(feature.GLIMSID) + '.img'
    try:
        cellsize = float(get_properties(raster, 'CELLSIZEX')) * buffer_scale
        
        # Buffer the input features geometry
        mask = ARCPY.Buffer_analysis(feature.shape, ARCPY.Geometry(), cellsize)
        
        # Extract by mask using the buffered feature geometry
        extract = ARCPY.sa.ExtractByMask (raster, mask[0])
        extract.save(subset) # Save extracted mask as subset
        
        return subset, False # Return path to subset location in the workspace
    except:
        return 'ERROR - Could not subset feature', True
    
    
    
    
    
    
    