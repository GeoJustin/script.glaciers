"""****************************************************************************
 Name:         glacier_utilities.functions.projection.data_checks
 Purpose:      Basic Functions to Check data Quality
 
Created:         Apr 23, 2013
Author:          Justin Rich (justin.rich@gi.alaska.edu)
Location: Geophysical Institute | University of Alaska, Fairbanks
Contributors:

Copyright:   (c) Justin L. Rich 2013
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

def check_attributes (input_file, *columns):
    """Returns the various attributes in a given column or columns.
    The function is intended to be used as a check of column entries to see
    if they match the expected values for a column(s)."""
    
    column_attributes = [] # Empty list to append attribute lengths
    field_names = ARCPY.ListFields(input_file) # Input field names
    
    rows = ARCPY.SearchCursor(input_file) # Open search cursor
    for row in rows:
        for field in field_names:
            if any(field.name == col for col in columns): # If the field matches input column
                entry = str(row.getValue(field.name)) # Get length of attribute value
                
                if str(entry) not in column_attributes: # If attribute isn't in list
                    column_attributes.append(str(entry))# Add attribute to list
    del row, rows    
    return column_attributes # Return the list of lengths


def check_attribute_length (input_file, *columns):
    """Returns the various lengths of attributes in a given column or columns.
    The function is intended to be used as a check of column lengths to see
    if they match the number of characters expected for the column(s)."""
    
    column_lengths = [] # Empty list to append attribute lengths
    field_names = ARCPY.ListFields(input_file) # Input field names
    
    rows = ARCPY.SearchCursor(input_file) # Open search cursor
    for row in rows:
        for field in field_names:
            if any(field.name == col for col in columns): # If the field matches input column
                entry_length = len(str(row.getValue(field.name))) # Get length of attribute value
                
                if str(entry_length) not in column_lengths: # If length isn't in list
                    column_lengths.append(str(entry_length))# Add length to list
                    
    del row, rows  
    return column_lengths # Return the list of lengths
        
        
def check_nodata_data(input_file, *columns):
    """Returns the number of incorrectly labeled dates. This functions primary 
    purpose is to look for no data values that are set to '00' or '0000' 
    instead of '99' or '9999'."""
    
    nodata = {'YEAR': 0, 'MONTH': 0, 'DAY': 0}
    field_names = ARCPY.ListFields(input_file) # Input field names
    
    rows = ARCPY.SearchCursor(input_file) # Open search cursor
    for row in rows:
        for field in field_names:
            if any(field.name == col for col in columns): # If the field matches input column
                date = row.getValue(field.name)
                if date[0:4] == '0000': nodata['YEAR'] = nodata['YEAR'] + 1
                if date[4:6] == '00': nodata['MONTH'] = nodata['MONTH'] + 1
                if date[6:8] == '00': nodata['DAY'] = nodata['DAY'] + 1
    del row, rows  
    return nodata # Return the list of lengths


def check_date_format (input_file, *columns):
    """Check the date format is in the correct order of 'YYYYMMDD'."""
    format_warning = 0
    field_names = ARCPY.ListFields(input_file) # Input field names
    
    rows = ARCPY.SearchCursor(input_file) # Open search cursor
    for row in rows:
        for field in field_names:
            if any(field.name == col for col in columns): # If the field matches input column
                date = row.getValue(field.name)
                if date[0:2] not in ('19', '20', '-9'): format_warning += 1
    del row, rows
    return format_warning
                

def check_is_uppercase (input_file, *columns):
    """Returns the number of records in a table contain all upper case letters. 
    If all letters in a column are upper case it is considered True, else False"""
    case_error = 0
    field_names = ARCPY.ListFields(input_file) # Input field names
    
    rows = ARCPY.SearchCursor(input_file) # Open search cursor
    for row in rows:
        for field in field_names:
            if any(field.name == col for col in columns): # If the field matches input column
                
                for word in row.getValue(field.name).split(' '):
                    try:
                        if word[0].islower(): case_error += 1
                        if word[1:].isupper(): case_error += 1
                    except:
                        case_error += 1
    return case_error


def check_area (input_file, threshold = 0.001, column = 'AREA'):
    """Returns the number of polygons which are less then a specified threshold."""
    threshold_error = 0
    rows = ARCPY.SearchCursor(input_file) # Open search cursor
    for row in rows:
        if float(row.getValue(column)) < threshold: threshold_error += 1
    del row, rows
    return threshold_error
    
    

#_______________________________________________________________________________
#***  DRIVER *******************************************************************
# HARD CODE INPUTS HERE !
def driver():
    returned = check_date_format ('A:\\Desktop\\RGI32\\RGI32RAW\\01_rgi32_Alaska.shp', 'BGNDATE', 'ENDDATE')
    print returned

    
if __name__ == '__main__':
    driver()




