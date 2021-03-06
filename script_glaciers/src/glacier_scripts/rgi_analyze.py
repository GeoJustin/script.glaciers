"""****************************************************************************
 Name: repair_rgi.repair_rgi
 Purpose: To repair any geometry error that may occur and to find errors in
        area calculation, topology and find any multi-part / single-part polygons
 
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
import sys, os
sys.path.append (os.path.dirname(os.path.dirname(__file__)))

import glob
import arcpy as ARCPY                                        #@UnresolvedImport
import glacier_utilities.functions.data_prep as DP
import glacier_utilities.functions.data_pop as POP
import glacier_utilities.functions.data_checks as CHECK
import glacier_utilities.general_utilities.environment as ENV

class rgi_analysis ():
    
    def __init__ (self, variables):
        
        # Read variables
        input_folder = variables.read_variable('INPUT_FOLDER')
        output_folder = variables.read_variable('OUTPUT_FOLDER')
        check_header = variables.read_variable('RGI_SPEC')
        version = variables.read_variable('RGIVERSION')

        # Setup working environment
        environment = ENV.setup_arcgis(output_folder)
        workspace = environment.workspace
        __Log = environment.log
        
        # Print run time parameters
        __Log.print_line("Input File: " + input_folder)
        __Log.print_line('Output Folder: ' + output_folder)
        __Log.print_line('RGI Header to Match (Name Only): ')
        __Log.print_line('   ' + str(check_header))
        __Log.print_break()
        
        tracking_list = [["File Name", "Tot.", "GM", "M-P", "Area km2", "% Diff.", "Topology Errors", "Date Error", "Format Error", "Case Error", "Sliver Error"]] # A list to hold tracking information
        
        # For each feature class within the input folder...
        for shapefile in glob.glob (os.path.join (input_folder, '*.shp')):
            tracking_info = [] # A list to hold individual tracking information
            
            __Log.print_line(os.path.basename(shapefile))
            tracking_info.append(os.path.basename(shapefile)[0:12])
            tracking_info.append(str(ARCPY.GetCount_management(shapefile)))
                    
            # Copy feature to workspace (output folder)
            working_shapefile = output_folder + '\\' + os.path.basename(shapefile)
            ARCPY.CopyFeatures_management (shapefile, working_shapefile)


            # Check to see if the input file follows RGI table headings.
            formate_error, not_found = DP.check_formate(working_shapefile, check_header)
            if formate_error == False:
                __Log.print_line('    Input header information is consistent with the standard set')
            if formate_error == True:
                __Log.print_line('    ERROR - Input header information is NOT consistent with the standard set')
                __Log.print_line('        Items not found: ' + not_found)
                
            # Check geometries. If there are errors, correct them and print the
            # results to the log file
            repair = DP.repair_geometry(working_shapefile)
            __Log.print_line('    Geometry - ' + repair[0] + ' errors found (Repaired ' + str(int(repair [0]) - int(repair[1])) + ')')
            tracking_info.append(str(repair[0]))
                
            # Check to see if there are any multi-part polygons in the input file. If
            # so, prompt the user to stop and correct. Print to log file.
            multipart = DP.check_multipart(working_shapefile, workspace) # Check for multi-part Polygons
            __Log.print_line('    Multi-Part Polygons - ' + multipart + ' found')
            tracking_info.append(str(multipart))
             
            # Check to see if the area from the AREA column matches the actual area
            # calculated. If not signal the user to correct. Print results to log.
            area = DP.check_area(working_shapefile, workspace)
            __Log.print_line('    Area - ' + area[2] + ' difference')
            __Log.print_line('        Original area: ' + area[0] + ' , Final area: ' + area[1], True)
            tracking_info.append(area [0])
            tracking_info.append(str(round(( (float(area[0])/float(area[1])) *100.0) -100.0, 1)))
             
            # Check to see if there are any topology errors in the input file. If there 
            # are signal the user to correct before moving forward. Print to log.
            topology = DP.check_topology(working_shapefile, workspace)
            __Log.print_line('    Topology - ' + topology[0] + ' errors on ' + topology[1] + ' features')
            __Log.print_line('        Rule set - Must Not Overlap (Area)', True)
            tracking_info.append(str(topology[0]))
             
            # Check to see if the fix column lengths such as RGIID, GLIMSID, GLACTYPE
            # are consistent with what is expected.      
            __Log.print_line('    Field Length Check:')
            RGI_length = CHECK.check_attribute_length(working_shapefile, 'RGIID')
            GLIMS_length = CHECK.check_attribute_length(working_shapefile, 'GLIMSID')
            GLACTYPE_Length = CHECK.check_attribute_length(working_shapefile, 'GLACTYPE')
            BGNDATE_Length = CHECK.check_attribute_length(working_shapefile, 'BGNDATE')
            ENDDATE_Length = CHECK.check_attribute_length(working_shapefile, 'ENDDATE')
            __Log.print_line('        RGID Expected: 14 - Actual Length(s): ' + ','.join(RGI_length), True)
            __Log.print_line('        GLID Expected: 14 - Actual Length(s): ' + ','.join(GLIMS_length), True)
            __Log.print_line('        GLAC Expected:  4 - Actual Length(s): ' + ','.join(GLACTYPE_Length), True)
            __Log.print_line('        BGND Expected:  8 - Actual Length(s): ' + ','.join(BGNDATE_Length), True)
            __Log.print_line('        ENDD Expected:  8 - Actual Length(s): ' + ','.join(ENDDATE_Length), True)
            
            # Check to see if the values in the RGIFLAG column has values that are expected
            RGIFLAG = CHECK.check_attributes(working_shapefile, 'RGIFLAG')
            GLACTYPE = CHECK.check_attributes(working_shapefile, 'GLACTYPE')
            __Log.print_line('    RGIFLAG Entries: ' + ','.join(RGIFLAG))
            __Log.print_line('    GLACTYPE Entries: ' + ','.join(GLACTYPE))
             
            # Check no data date values are 9's and not 0's
            nodata_bgndate = CHECK.check_nodata_data (working_shapefile, 'BGNDATE')
            __Log.print_line('    Start Date Format 9 and not 0: ' + str(nodata_bgndate))
            nodata_enddate = CHECK.check_nodata_data (working_shapefile, 'ENDDATE')
            __Log.print_line('    End Date Format 9 and not 0: ' + str(nodata_enddate))
            tracking_info.append(str(sum(nodata_bgndate.values()) + sum(nodata_enddate.values())))
           
            # Check the date format. Dates should be 'YYYYMMDD'
            format_error = CHECK.check_date_format (working_shapefile, 'BGNDATE', 'ENDDATE')
            __Log.print_line('    Date Format Errors: ' + str(format_error))
            tracking_info.append(str(format_error))
           
           
            # Check for case errors in fields. Should be first letter upper case, 
            # lower case everything else.
            case_errors = CHECK.check_is_uppercase(working_shapefile, 'RGIFLAG')
            __Log.print_line('    RGIFLAG Case Errors: ' + str(case_errors))
            tracking_info.append(str(case_errors))
            
            # Check the number of glaciers that do not meet the threshold
            threshold_error = CHECK.check_area(working_shapefile, 0.001, 'AREA')
            __Log.print_line('    Threshold (0.001 km2) Errors: ' + str(threshold_error))
            tracking_info.append(str(threshold_error))
           
            # Regenerate basic stats.
            POP.auto_generate_RGIIDs (working_shapefile, version)
            __Log.print_line ('    Recalculated RGI IDs')
            
            POP.generate_GLIMSIDs(working_shapefile, workspace)
            __Log.print_line ('    Recalculated GLIMS IDs')
            
            POP.generate_centroid(working_shapefile)
            __Log.print_line ('    Recalculated CENLAT and CENLON')
            
           
            __Log.print_break() # Break for next section in the log file.
            tracking_list.append(tracking_info)
            
        # Print Tracking Info Lists
        __Log.print_line('Summary')
        __Log.print_line('-' * 80, True)
        __Log.print_line('<table align="center" width="700em" border="1" cellpadding="5em">', True)
        for tracking in tracking_list:
            __Log.print_line('<tr><td>' + ('</td><td>'.join(tracking)) + '</td></tr>', True)
        __Log.print_line('</Table>', True)
        
        # Script Complete. Try and delete workspace   
        removed = environment.remove_workspace()
        if removed == True:
            __Log.print_break()
            __Log.print_line('Processing Complete')
        else:
            __Log.print_break()
            __Log.print_line('Workspace Could not be deleted')
            __Log.print_line('Processing Complete')
        
#_______________________________________________________________________________
#***  DRIVER *******************************************************************
# HARD CODE INPUTS HERE !

def driver():
    input_folder = r'A:\Desktop\Mapdate'
    output_folder = r'A:\Desktop\Mapdate\Test'

    import glacier_utilities.general_utilities.variables  as variables
    VAR = variables.Variables()
    
    VAR.set_variable('INPUT_FOLDER', 'STRING', input_folder)
    VAR.set_variable('OUTPUT_FOLDER', 'STRING', output_folder)
        
    rgi_analysis (VAR)

if __name__ == '__main__':
    driver()