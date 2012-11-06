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
import math
import random

def get_aspect (feature, dem, bin_mask, max_bin = 8850, min_bin = 0, bin_size = 50):
    """Calculate aspect information from the given aspect raster generated from 
    a DEM and return bin statistics. Each aspect bin is defined by elevation
    and shares the same spatial area is hypsometry bins. If this function 
    fails at runtime an error is returned for recording in the log file."""
    aspect = []
    try:
        # NOT WRITTEN 
        # NOT WRITTEN 
        return aspect, False
    except:
        return aspect, True
    

def get_attributes (feature):
    """Return feature attribute values: GLIMSID, NAME, GLACTYPE, BGNDATE, 
    ENDDATE, CENLON, CENLAT and AREA. If value doesn't exist it should be
    left blank. If this function fails at runtime an error is returned for
    recording in the log file."""
    attributes = [''] * 8
    try:
        attributes[0] = str(feature.GLIMSID)
        attributes[1] = str(feature.NAME)
        attributes[2] = str(feature.GLACTYPE)
        attributes[3] = str(feature.BGNDATE)
        attributes[4] = str(feature.ENDDATE)
        attributes[5] = str(feature.CENLON)
        attributes[6] = str(feature.CENLAT)
        attributes[7] = str(feature.AREA)
        return attributes, False
    except:
        return attributes, True
    
    
def get_centerline (features, dem, workspace, output, min_bin = 0, bin_size = 50):
    """Returns a center line feature of the given polygon feature based
     on elevation. Center line determined by contour line centroid. If 
     there are multiple contours are found at a bin location then the 
     largest is selected. """
    centerline = output + '\\centerline.shp'

    
    return centerline

def get_hypsometry (feature, dem, workspace, raster_scaling = 1000, max_bin = 8850, min_bin = 0, bin_size = 50):
    """Calculate hypsometry information from the given digital elevation model
    (DEM) and return bin statistics. If this function fails at runtime an error
    is returned for recording in the log file."""
    hypsometry = []
    try:
        reclassify_range = '' # re-map string
        elevation_list = []   # List containing the area and elevation values
            
        # Generate re-map string for the reclassify function. This done by first
        # calculating the number of bins and then finding the low and high values
        # for each bin and then giving it a label.
        total_bins = round(math.ceil(float(max_bin - min_bin) / float(bin_size)), 0)
        for bin_num in range (0, int(total_bins)):  # For each bin...
            low_value =  bin_num * bin_size         # Low value in range and re-map value
            high = float((bin_num + 1) * bin_size)  # High value in range
            reclassify_range += str(float(low_value)) + " " + str(high) + " " + str(low_value) + ";"
            
            hypsometry.append(float(low_value)) # Append the bin value to the hypsometry list
    
        # Reclassify the DEM based on bins
        reclassify =  workspace + '\\' + 'Reclassify_Raster_' + str(feature.GLIMSID) + '.img'
        reclass_raster = ARCPY.sa.Reclassify (dem, "Value", reclassify_range, "NODATA")
        reclass_raster.save(reclassify)
        
        # Create a clipped feature from the input raster.
        bin_features = raster_to_polygon(feature, reclassify, workspace, raster_scaling)
        
        # Iterate over the feature table and generate a list of bin values and area of each
        rows = ARCPY.SearchCursor(bin_features)
        for row in rows:
            elevation_list.append([float(row.GRIDCODE/raster_scaling), float(row.F_AREA)])
            
        item_found = False # Switch to identify if an element exists or not
        current_bin = 0.0 # Bin value to print
        for index, hypso_bin in enumerate (hypsometry): # For each hypsometry bin
            for item in elevation_list:      # Loop through the elevation list 
                if item[0] == hypso_bin:        # If the value in elev. List is found...
                    current_bin += item[1]      # ... add it to the hypsometry list
                    item_found = True
                    
            if item_found == False: # If an element is NOT found in elevation list...
                hypsometry[index] = str(0.0) # set elevation bin to 0.0
            else:                   # If an element is found
                # Set elevation bin to sum of values and remove decimals by rounding
                hypsometry[index] = str(round(current_bin, 0)) 
                item_found = False  # Reset the switch
                current_bin = 0.0   # Reset bin value to print
        
        ARCPY.Delete_management(reclassify) # Remove the reclassified raster from workspace
        del row
        del rows
        return hypsometry, False, bin_features
    except:
        return hypsometry, True, bin_features

    
def get_properties (raster, prop = ''):
    """Return the desired property from the input raster layer. These include:
    MINIMUM, MAXIMUM, MEAN, STD, ... etc."""
    return str(ARCPY.GetRasterProperties_management(raster, prop))


def get_slope (feature, dem, bin_mask, workspace, raster_scaling = 0, z_value = 1.0, max_bin = 8850, min_bin = 0, bin_size = 50):
    """Calculate slope information from the given slope raster generated from 
    a DEM and return bin statistics. Each slope bin is defined by elevation
    and shares the same spatial area is hypsometry bins. If this function 
    fails at runtime an error is returned for recording in the log file."""
    
    slope_list = []

    return slope_list, False
    #except:
    #   return  slope, True
        
        
def get_statistics (feature, dem, workspace, raster_scaling = 1000):
    """Return basic feature statistics which include elevation maximum, 
    elevation minimum, median elevation and mean elevation. If this function
    fails at runtime an error is returned for recording in the log file."""
    statistics = [''] * 3
    try:
        area_list = []
        value_list = []
    
        raster_feature = raster_to_polygon(feature, dem, workspace, raster_scaling)
        
        rows = ARCPY.SearchCursor(raster_feature)
        for row in rows:
            area_list.append(row.F_AREA)
            value_list.append(row.GRIDCODE / raster_scaling)
            
        statistics[0] = str(min(value_list)) # Get Minimum Value 
        statistics[1] = str(max(value_list)) # Get Maximum Value
        
        # Weighted Average value - (sum value * area) / sum area
        numerator = sum ((value_list[i] * area_list[i]) for i in range(0, len(area_list)))
        denominator =  sum (area_list[i] for i in range (0, len(area_list)))
        statistics[2] = str(numerator / denominator)
    
        ARCPY.Delete_management(raster_feature) # Delete masked raster feature
        return statistics, False
    except:
        return statistics, True
        

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
        return subset, True
    
    
def raster_to_polygon (feature, raster, workspace, raster_scaling = 1000):
    """Convert raster to a features class, clip it to an input feature and
    calculate the area of each polygon. This new feature class is then 
    returned for calculating statistics. """
    
    # Scale the subset DEM and temporarily save it to file. If it is not
    # saved an error is sometimes thrown when converting to polygon.
    # This is no good reason for this VAT error.
    rand_id = str(random.randrange(10000, 999999))
    subset_name = workspace + '\\raster_to_poly_' + rand_id + '.img'
    subset = ARCPY.sa.Int(ARCPY.sa.Raster(raster) * raster_scaling + 0.5)
    subset.save(subset_name)

    polygon = ARCPY.RasterToPolygon_conversion(subset, subset_name, "NO_SIMPLIFY")
    clipped = ARCPY.Clip_analysis(polygon, feature.shape, 'in_memory\\clip_' + rand_id)
    feature = ARCPY.CalculateAreas_stats(clipped, 'in_memory\\area_'+ rand_id)
    
    ARCPY.Delete_management(subset)
    ARCPY.Delete_management(polygon)
    ARCPY.Delete_management(clipped)
    
    return feature
    
    