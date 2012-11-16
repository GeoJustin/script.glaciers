"""****************************************************************************
 Name: functions_data_calc
 Purpose: The purpose of this module is to hold the post proccess functions 
     that deal with calculation of statistics including hypsometry, slope
     and aspect information. 
 
Created: Oct 12, 2012
Author:  Justin Rich (justin.rich@gi.alaska.edu)
Location: Geophysical Institute | University of Alaska, Fairbanks
Contributors: Christian Kienholz, University of Alaska, Fairbanks

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

def get_aspect (feature, bin_mask, bins, workspace, raster_scaling = 1000):
    """Calculate aspect information from the given feature centerline based
    on a bin mask. A bin mask is one of the standard outputs from calculating 
    hypsometry. Aspect is 0 -360 degrees clockwise from north and starts from 
    the lowest elevation toward the highest."""
    try:
        aspect_list = [str(0.0)] * len(bins) # string list of 0.0 to return
        bin_list = bins # List of bin values
        centerline_list = [] # List to hold current features length and slope values
        
        rows = ARCPY.SearchCursor (bin_mask)
        for row in rows: # For each bin within the bin mask
            elevation_bin = int(row.GRIDCODE / raster_scaling) # Get bin value
            
            # Clip centerline to current bin and count the features generated
            clipped_line = ARCPY.Clip_analysis (feature, row.shape, 'in_memory\\clipped_line')
            feature_count = int(ARCPY.GetCount_management(clipped_line).getOutput(0)) 
            
            if feature_count > 0: # If there is 1 or more features
                ARCPY.CalculateField_management(clipped_line, 'LENGTH', 'float(!shape.length@meters!)', 'PYTHON')
                
                # Lines with multi-part features sometimes have reversed directions do to where
                # points are placed for the beginning and end of line segments within the multi-part line. 
                m_to_s = ARCPY.MultipartToSinglepart_management (clipped_line, 'in_memory\\m_to_s')
            
                # Calculate mean direction of lines
                direction = ARCPY.DirectionalMean_stats(m_to_s, 'in_memory\\direction_line', "DIRECTION")  
                
                bin_aspects = []
                dir_rows = ARCPY.SearchCursor (direction) # Read the direction feature 
                for dir_row in dir_rows: # For each record (there should only be one
                    bin_aspects = dir_row.CompassA # Get direction
                del dir_row, dir_rows
                        
                ARCPY.Delete_management(direction) # Clean up temporary clip
                    
                # Add the current bin and average aspect to the centerline list
                centerline_list.append([elevation_bin, round(bin_aspects, 2)])

                
                ARCPY.Delete_management(m_to_s) # Clean up temporary clip
            ARCPY.Delete_management(clipped_line) # Clean up temporary clip
        del row, rows
    
        # Look to see if there is an aspect value for the given bin
        for index, entry in enumerate (bin_list): # For each bin (all of them)
            bin_number = int(entry[1:]) # Convert string to int ('B150' to 150)
            for item in centerline_list: # For each item in current feature
                if item[0] == bin_number: # If item bin matches all bin 
                    aspect_list[index] = str(item[1]) # Place slope value
        
        return aspect_list, False
    except:
        return aspect_list, True
    

def get_attributes (feature, Attribute_header):
    """Return feature attribute values: GLIMSID, NAME, GLACTYPE, BGNDATE, 
    ENDDATE, CENLON, CENLAT and AREA. If value doesn't exist it should be
    left blank. If this function fails at runtime an error is returned for
    recording in the log file."""
    attributes = [''] * len(Attribute_header)
    try:
        for position, item in enumerate (Attribute_header):
            attributes[position] =  str(feature.getValue(item))
        return attributes, False
    except:
        return attributes, True
    
    
def get_centerline (feature, dem, workspace, eu_cell_size = 2, smoothing = 4):
    """Returns a center line feature of the given polygon feature based on
    cost over an euclidean distance raster and cost path. points are seeded
    using minimum and maximum elevation."""    
    centerline = workspace + '\\centerline.shp'
    center_length = 0
    center_slope = 0
    try: 
        ARCPY.env.snapRaster = dem
        ARCPY.env.overwriteOutput = True
        
        # Get minimum and maximum points
        masked_dem = ARCPY.sa.ExtractByMask (dem, feature.shape)
        
        # Find the maximum elevation value in the feature, convert them to
        # points and then remove all but one.
        maximum = get_properties (masked_dem, 'MAXIMUM') 
        maximum_raster = ARCPY.sa.SetNull(masked_dem, masked_dem, 'VALUE <> ' + maximum)
        maximum_point = ARCPY.RasterToPoint_conversion(maximum_raster, 'in_memory\\max_point')
        rows = ARCPY.UpdateCursor (maximum_point)
        for row in rows:
            if row.pointid <> 1:
                rows.deleteRow(row)
        del row, rows
        
        # Find the minimum elevation value in the feature, convert them to
        # points and then remove all but one.
        minimum = get_properties (masked_dem, 'MINIMUM')
        minimum_raster = ARCPY.sa.SetNull(masked_dem, masked_dem, 'VALUE <> ' + minimum)
        minimum_point = ARCPY.RasterToPoint_conversion(minimum_raster, 'in_memory\\min_point')
        rows = ARCPY.UpdateCursor (minimum_point)
        for row in rows:
            if row.pointid <> 1:
                rows.deleteRow(row)
        del row, rows
        
        # Calculate euclidean Distance to boundary line for input DEM cells.
        polyline = ARCPY.PolygonToLine_management(feature.shape, 'in_memory\\polyline')
        eucdist = ARCPY.sa.EucDistance(polyline, "", eu_cell_size, '')
        masked_eucdist = ARCPY.sa.ExtractByMask (eucdist, feature.shape)
        
        # Calculate the cost raster by inverting the euclidean distance results,
        # and rasing it to the power of x to exaggerate the least expensive route.
        cost_raster = (-1 * masked_eucdist + float(maximum))**5
        
        # Run the cost distance and cost path function to find the path of least
        # resistance between the minimum and maximum values. The results are set
        # so all values equal 1 (different path segments have different values)
        # and convert the raster line to a poly-line.
        backlink = 'in_memory\\backlink'
        cost_distance = ARCPY.sa.CostDistance(minimum_point, cost_raster, '', backlink)
        cost_path = ARCPY.sa.CostPath(maximum_point, cost_distance, backlink, 'EACH_CELL', '')
        cost_path_ones = ARCPY.sa.Con(cost_path, 1, '', 'VALUE > ' + str(-1)) # Set all resulting pixels to 1
        r_to_p = ARCPY.RasterToPolyline_conversion (cost_path_ones, 'in_memory\\raster_to_polygon')
    
        # Smooth the resulting line. Currently smoothing is determined by minimum
        # and maximum distance. The greater change the greater the smoothing.
        smooth_tolerance = (float(maximum) - float(minimum)) / smoothing
        ARCPY.SmoothLine_cartography(r_to_p, centerline, 'PAEK', smooth_tolerance, 'FIXED_CLOSED_ENDPOINT', 'NO_CHECK')
    
        field_names = [] # List of field names in the file that will be deleted.
        fields_list = ARCPY.ListFields(centerline)
        for field in fields_list: # Loop through the field names
            if not field.required: # If they are not required append them to the list of field names.
                field_names.append(field.name)
        # Add new fields to the center line feature
        ARCPY.AddField_management(centerline, 'GLIMSID', 'TEXT', '', '', '25')
        ARCPY.AddField_management(centerline, 'LENGTH', 'FLOAT')
        ARCPY.AddField_management(centerline, 'SLOPE', 'FLOAT')
        ARCPY.DeleteField_management(centerline, field_names) # Remove the old fields.
        
        # Calculate the length of the line segment and populate segment data.
        ARCPY.CalculateField_management(centerline, 'LENGTH', 'float(!shape.length@meters!)', 'PYTHON')
        rows = ARCPY.UpdateCursor (centerline)
        for row in rows:
            row.GLIMSID = feature.GLIMSID # Get GLIMS ID and add it to segment
            center_length = row.LENGTH # Get the length of the center line
            # Calculate slope of the line based on change in elevation over length of line
            center_slope = round(math.degrees(math.atan((float(maximum) - float(minimum)) / row.LENGTH)), 2)
            row.SLOPE = center_slope # Write slope to Segment
            rows.updateRow(row) # Update the new entry
        del row, rows #Delete cursors and remove locks    
    
        ARCPY.env.overwriteOutput = False
        return centerline, center_length, center_slope, False
    except:
        ARCPY.env.overwriteOutput = False
        return centerline, '', '', True


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
        del row, rows
            
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
        
        return hypsometry, False, bin_features
    except:
        return hypsometry, True, bin_features

    
def get_properties (raster, prop = ''):
    """Return the desired property from the input raster layer. These include:
    MINIMUM, MAXIMUM, MEAN, STD, ... etc."""
    return str(ARCPY.GetRasterProperties_management(raster, prop))


def get_slope (feature, bin_mask, bins, workspace, raster_scaling = 1000, bin_size = 50):
    """Calculate slope information along the center line by clipping segements of the 
    centerline to each bin. A bin mask is required and is calculated as a standard
    output of the 'get_hypsometry' function. Slope calculations assume centerline 
    segment runs the length of the bins so first and last values may be incorrect if
    if the line end before it reaches the end of a bin or starts within it."""
    slope_list = [str(0.0)] * len(bins) # string list of 0.0 to return
    bin_list = bins # List of bin values
    centerline_list = [] # List to hold current features length and slope values
            
    try:
        rows = ARCPY.SearchCursor (bin_mask)
        for row in rows: # For each bin within the bin mask
            elevation_bin = int(row.GRIDCODE / raster_scaling) # Get bin value
            
            # Clip centerline to current bin and calculate it's length
            clipped_line = ARCPY.Clip_analysis (feature, row.shape, 'in_memory\\clipped_line' )
            ARCPY.CalculateField_management(clipped_line, 'LENGTH', 'float(!shape.length@meters!)', 'PYTHON')
            
            length = 0
            try: # Fails if feature is empty (i.e. there is no centerline in the bin
                # Open clipped line segment and look for it's length
                clip_rows = ARCPY.SearchCursor (clipped_line)
                for clip_row in clip_rows:
                    length += clip_row.LENGTH # Get length
                del clip_row, clip_rows
            except: pass
            
            # If there is a line segment, calculate slope and append it list
            if length <> 0:  # with elevation bin value
                center_slope = round(math.degrees(math.atan(float(bin_size) / length)), 2)
                centerline_list.append([elevation_bin, center_slope])
            
            ARCPY.Delete_management(clipped_line) # Clean up temporary clip
        del row, rows    
        
        # Look to see if there is a slope value for the given bin
        for index, entry in enumerate (bin_list): # For each bin (all of them)
            bin_number = int(entry[1:]) # Convert string to int ('B150' to 150)
            for item in centerline_list: # For each item in current feature
                if item[0] == bin_number: # If item bin matches all bin 
                    slope_list[index] = str(item[1]) # Place slope value

        return slope_list, False # Return current features slope values
    except:
        return  slope_list, True # Return anything that was run or empty list of '0.0'
        
        
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
        # Buffer the input features geometry
        cellsize = float(get_properties(raster, 'CELLSIZEX')) * buffer_scale
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
    
    