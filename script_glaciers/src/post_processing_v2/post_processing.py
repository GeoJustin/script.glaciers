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
import sys, os
sys.path.append (os.path.dirname(os.path.dirname(__file__)))

import arcpy as ARCPY                                         #@UnresolvedImport
import glacier_utilities.functions.data_prep as DP                              
import glacier_utilities.functions.data_calc as DC
import glacier_utilities.functions.data_pop as POP                         
import glacier_utilities.output_file.output_file_log as LOG
import glacier_utilities.output_file.output_file_csv as CSV                                       


class process (object):
    
    def __init__ (self, input_features, output_location, DEM, variables):
        
        # Create a copy of the input file in the output folder. This will be the
        # actual result file after fields are updated. This is done so no changes
        # are imposed on the original file.
        try:
            output = output_location + '\\' + os.path.basename(input_features)
            input_copy = ARCPY.CopyFeatures_management(input_features, output)
        except:
            print 'Output Glacier file already exists or the output folder is not available.'
            sys.exit()
        
        try: # Start Log file and write it to the output folder
            log_path = os.path.dirname(os.path.abspath(output))
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
            workspace = output_location + '\\workspace'
            os.makedirs(workspace) # Create Workspace
            ARCPY.env.workspace = workspace
        except:
            __Log.print_line('WARNING - Workspace folder already exists.')
            sys.exit()
                        
        
        # Read Variables
        centerlines = variables.read_variable('CENTERLINES')
        hypsometry = variables.read_variable('HYPSOMETRY')
        slope = variables.read_variable('SLOPE')
        aspect = variables.read_variable('ASPECT')
        glimsids = variables.read_variable('GLIMSIDS')
        rgiids = variables.read_variable('RGIIDS')        
        
        # Create output table header information to populate the tables with
        table_output = os.path.dirname(os.path.abspath(output))
        Attribute_header = variables.read_variable('ATTABLE')
        Statistics_header = variables.read_variable('STATABLE')
        max_bin = variables.read_variable('MAXBIN')
        min_bin =  variables.read_variable('MINBIN')
        bin_size = variables.read_variable('BINSIZE')
        bin_header = DP.generate_bin_header(max_bin, min_bin, bin_size)
        header = Attribute_header + Statistics_header + bin_header
        
        # Read other variables
        check_header = variables.read_variable('RGI_SPEC')
        subset_buffer = variables.read_variable('BUFFER')
        scaling = variables.read_variable('SCALING')
        eu_cell_size = variables.read_variable('EU_CELL_SIZE')
        power = variables.read_variable('POWER')
        
        # Other variables
        currently_processing = 1
        total_features = 0

        # Print run time variables to log file
        __Log.print_line("Input File: " + os.path.basename(input_features))
        __Log.print_line("Input DEM: " + os.path.basename(DEM))
        __Log.print_line('Output Folder: ' + os.path.dirname(os.path.abspath(output)))
        __Log.print_line('Output Glaciers: ' + os.path.basename(output))
        if centerlines == True: __Log.print_line('Output Centerlines: centerlines.shp' )
        __Log.print_break()
        __Log.print_line("Runtime Parameters")
        __Log.print_line("     Run Hypsometry: " + str(hypsometry))
        __Log.print_line("     Run Slope: " + str(slope))
        __Log.print_line("     Run Aspect: " + str(aspect))
        __Log.print_line("     Generate GLIMS ID's: " + str(glimsids))
        __Log.print_line("     Generate RGI ID's: " + str(rgiids))
        __Log.print_line("     Maximum Bin Elevation: " + str(max_bin))
        __Log.print_line("     Minimum Bin Elevation: " + str(min_bin))
        __Log.print_line("     Bin Size: " + str(bin_size))
        __Log.print_line("     Subset Buffer: " + str(subset_buffer) + 'x')
        __Log.print_line("     DEM Scaling Factor: " + str(scaling))
        __Log.print_line("     Centerline Euclidean Cell Size: " + str(eu_cell_size))
        __Log.print_line("     Centerline Line Power Factor: " + str(power))
        __Log.print_break() # Break for next section in the log file.
        
        #_______________________________________________________________________
        #*******Input File Cleanup**********************************************  
        
        __Log.print_line('Input Polygon Checks')
        # Check to see if the input file follows RGI table headings.
        formate_error, not_found = DP.check_formate(input_features, check_header)
        if formate_error == False:
            __Log.print_line('    Input header information is consistent with the standard set')
        if formate_error == True:
            __Log.print_line('    ERROR - Input header information is NOT consistent with the standard set')
            __Log.print_line('        Items not found: ' + not_found)
            sys.exit()
        
        # Check geometries. If there are errors, correct them and print the
        # results to the log file
        repair = DP.repair_geometry(input_copy)
        __Log.print_line('    Geometry - ' + repair[0] + ' errors found (Repaired ' + repair[1] + ')')
           
        # Check to see if there are any multi-part polygons in the input file. If
        # so, prompt the user to stop and correct. Print to log file.
        multipart = DP.check_multipart(input_copy, workspace) # Check for multi-part Polygons
        __Log.print_line('    Multi-Part Polygons - ' + multipart + ' found')
        
        # Check to see if the area from the AREA column matches the actual area
        # calculated. If not signal the user to correct. Print results to log.
        area = DP.check_area(input_copy, workspace)
        __Log.print_line('    Area - ' + area[2] + ' difference')
        __Log.print_line('        Original area: ' + area[0] + ' , Final area: ' + area[1], True)
        
        # Check to see if there are any topology errors in the input file. If there 
        # are signal the user to correct before moving forward. Print to log.
        topology = DP.check_topology(input_copy, workspace)
        __Log.print_line('    Topology - ' + topology[0] + ' errors on ' + topology[1] + ' features')
        __Log.print_line('        Rule set - Must Not Overlap (Area)', True)
        
        # Warnings: 
        if multipart <> str(0): print "WARNING:  Multi-part features found.."
        if area [2] > 1 or area[2] < -1: 'WARNING: The AREA difference exceeds the threshold.'
        if topology[0] <> str(0): raw_input(str(topology[0]) + "WARNING: Topology errors found.")
       
        __Log.print_break() # Break for next section in the log file.
        
        #_______________________________________________________________________
        #*******Prepare Input file*********************************************
        
        if glimsids == True: # Generate GLIMS id's if applicable
            __Log.print_line('Generating GLIMS IDs')
            glims_ids = POP.generate_GLIMSIDs(input_copy, workspace) # Copy to Output
            __Log.print_line('   GLIMS IDs - ' + glims_ids + ' GLIMS IDs Generated')
            total_features = glims_ids
            
        if rgiids == True: # Generate RGI id's if applicable
            __Log.print_line('Generating RGI IDs')
            rgi_ids = POP.generate_RGIIDs(input_copy) # Copy to Output
            __Log.print_line('   RGI IDs - ' + rgi_ids + ' RGI IDs Generated')
            total_features = rgi_ids
        
        __Log.print_break() # Break for next section in the log file.
        
        #_______________________________________________________________________
        #*******Calculate Statistics********************************************

        # Generate center lines output file to append centerlines
        if centerlines == True:
            output_centerlines = ARCPY.CreateFeatureclass_management(output_location, 'centerlines.shp', 'POLYLINE', '', '', 'ENABLED', input_features)
            ARCPY.AddField_management(output_centerlines, 'GLIMSID', 'TEXT', '', '', '25')
            ARCPY.AddField_management(output_centerlines, 'LENGTH', 'FLOAT')
            ARCPY.AddField_management(output_centerlines, 'SLOPE', 'FLOAT')
            ARCPY.DeleteField_management(output_centerlines, 'Id')

            
        # Create an instance of hypsometry, slope and aspect table if applicable
        if hypsometry == True: hypso_csv = CSV.CSV(table_output, 'Stats_Hypsometry', header) 
        if slope == True: slope_csv = CSV.CSV(table_output, 'Stats_slope', header) 
        if aspect == True: aspect_csv = CSV.CSV(table_output, 'Stats_aspect', header) 
        

        if centerlines == True or hypsometry == True or slope == True or aspect == True:
            rows = ARCPY.SearchCursor(input_copy) # Open shapefile to read features
            for row in rows: # For each feature in the shapefile
                
                # Get Attributes information such as GLIMS ID, Lat, Lon, area... etc.
                attribute_info, attribute_error = DC.get_attributes(row, Attribute_header)
                print ''
                print ''
                print 'Currently running: ' + str(currently_processing) + ' of ' + str(total_features)
                print 'Feature ' + str(attribute_info[0]) + ' ' + str(attribute_info[1])
                print '    Glacier Type: '  + str(attribute_info[2])
                print '    Area: ' + str(attribute_info[7]) + ' Sqr.'
                print '    Centroid (DD): ' + str(attribute_info[5]) + ', ' + str(attribute_info[6])
                if attribute_error == True: # If function failed
                    __Log.print_line(str(row.GLIMSID) + ' - ERROR - Could not read attributes')
                                
                                
                # Subset the DEM based on a single buffered glacier outline
                subset, subset_error = DC.subset(row, DEM, workspace, subset_buffer)
                if subset_error == True: # If function failed
                    __Log.print_line(str(row.GLIMSID) + ' - ERROR - Could not subset feature')
                
                
                # Get basic statistics such as minimum elevation, mean... etc.
                if hypsometry == True or slope == True or aspect == True:
                    statistics_info, statistics_error = DC.get_statistics(row, subset, workspace, scaling) 
                    print '    Elevation: ' + str(statistics_info[0]) + ' Min. / ' + str (statistics_info[1]) + ' Max.'
                    print '    Area Weighted Avg. Elev. = ' + str(statistics_info[2])
                    if statistics_error == True: # If function failed
                        __Log.print_line(str(row.GLIMSID) + ' - ERROR - Could not generate basic statistics')
                
                
                if hypsometry == True or slope == True or aspect == True:
                    print '    Running Hypsometry for Bin Mask & Table Statistics'
                    hypsometry_info, hypso_error, bin_mask = DC.get_hypsometry(row, subset, workspace, scaling, max_bin, min_bin, bin_size)
                    if hypsometry == True and hypso_error == False:
                        hypso_csv.print_line(attribute_info + statistics_info + hypsometry_info) # Print hypsometry data.
                    if hypso_error == True:
                        __Log.print_line(str(row.GLIMSID) + 'ERROR - Could not generate hypsometry information')
                
                
                if centerlines == True or slope == True or aspect == True:
                    print '    Running Center Line'
                    centerline, center_length, center_angle, centerline_error = DC.get_centerline(row, subset, workspace, power, eu_cell_size)
                    if centerline_error == False: 
                        print '    Center Line Length: ' + str(center_length) + ' & Slope Angle: ' + str(center_angle)
                        if centerlines == True:
                            ARCPY.Append_management(centerline, output_centerlines)
                    if centerline_error == True:
                        __Log.print_line(str(row.GLIMSID) + ' - ERROR - Could not generate center line')
                
                
                    if slope == True:
                        print '    Running Slope Table Statistics'
                        slope_info, slope_error = DC.get_slope(centerline, bin_mask, bin_header, workspace, scaling, bin_size)
                        slope_csv.print_line(attribute_info + statistics_info + slope_info)
                        if slope_error == True:
                            __Log.print_line(str(row.GLIMSID) + ' - ERROR - Could not calculate binned slope data')
                            
                
                    if aspect == True:
                        print '    Running Aspect Table Statistics'
                        aspect_info, aspect_error = DC.get_aspect(centerline, bin_mask, bin_header, workspace, scaling)        
                        aspect_csv.print_line(attribute_info + statistics_info + aspect_info)
                        if aspect_error == True:
                            __Log.print_line(str(row.GLIMSID) + ' - ERROR - Could not calculate binned aspect data')
                             
                # Clean Up Workspace
                try: ARCPY.Delete_management(subset)
                except: pass
                try: ARCPY.Delete_management(centerline)
                except: pass

                currently_processing += 1
            del row , rows #Delete cursors and remove locks
            
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
    Input = r'A:\Desktop\TestDataPrep\TestGlacier_Single.shp'
    Output = r'A:\Desktop\TestDataPrep\Output'
    DEM = r'A:\Desktop\TestDataPrep\Test_DEM.img'
    
    #Variables - WARNING: Use caution manually changing variables.
    import glacier_utilities.general_utilities.variables  as variables
    variables = variables.Variables()

    process (Input, Output, DEM, variables)

if __name__ == '__main__':
    driver()