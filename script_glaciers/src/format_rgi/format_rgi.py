"""****************************************************************************
 Name:         format_rgi.formate_rgi
 Purpose:     
 
Created:         Nov 16, 2012
Author:          Justin Rich (justin.rich@gi.alaska.edu)
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
import os
import sys
import arcpy as ARCPY                                       #@UnresolvedImport
import glacier_utilities.general_utilities.environment as ENV

class FormatRGI (object):
    """classdocs """

    def __init__(self, input_file, output_file, mappings, variables):
        """Constructor:  """
        
        # Setup working environment
        environment = ENV.setup_arcgis(os.path.dirname(os.path.abspath(output_file)))
        __Log = environment.log
        
        # Create a copy of the input file in the output folder. This will be the
        # actual result file after fields are updated. This is done so no changes
        # are imposed on the original file.
        try:
            new_file = ARCPY.CopyFeatures_management(input_file, output_file)
        except:
            print 'Output Glacier file already exists or the output folder is not available.'
            sys.exit()


        # List of original field names in the file that will be deleted or re-mapped
        original_fields = [] 
        fields_list = ARCPY.ListFields(new_file)
        for field in fields_list: # Loop through the field names
            if not field.required: # If they are not required append them to the list of field names.
                original_fields.append(field.name)
                
        __Log.print_line('Original Field Names:')
        __Log.print_line('    ' + str(original_fields))
                
        # Create a temp field for each of the fields to be re-mapped
        counter = 1 # Temp field number
        temp_fields = [] # Temp fields to delete later
        for index, mapping in enumerate (mappings):
            temp_field = 'TEMP_' + str(counter) # Temp Field name
            ARCPY.AddField_management (new_file, temp_field, 'TEXT', '', '', 100)
            
            ARCPY.CalculateField_management (new_file, temp_field, '!' + mapping[0] + '!', 'PYTHON')

            mappings [index] = (temp_field, mapping [1])
            temp_fields.append(temp_field) # Add temp field to list
            counter += 1 # Increment the counter by 1
        # Drop original fields
        ARCPY.DeleteField_management (new_file, original_fields)
            
        # Get RGI headers
        rgi_specs = variables.read_variable('RGI_SPEC')
        print rgi_specs
        for header in rgi_specs:
            print header[0], header[1], header[2], header[3], header[4]
            ARCPY.AddField_management (new_file, header[0], header[1], header[2], header[3], header[4])
        
        # Map temp fields to new fields and delete the temp fields
        for mapping in mappings:
            ARCPY.CalculateField_management (new_file, mapping[1], '!' + mapping[0] + '!', 'PYTHON')
        # Drop original fields
        ARCPY.DeleteField_management (new_file, temp_fields)
            
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
def driver ():
    input_file = r'A:\Desktop\TestDataPrep\formate_test.shp'
    output_file = r'A:\Desktop\TestDataPrep\Output\formate_output.shp'
    mapping = [('Name', 'NAME'), ('Area', 'AREA')]

    import glacier_utilities.general_utilities.variables  as variables
    VAR = variables.Variables()
    
    FormatRGI (input_file, output_file, mapping, VAR)
if __name__ == '__main__':
    driver()