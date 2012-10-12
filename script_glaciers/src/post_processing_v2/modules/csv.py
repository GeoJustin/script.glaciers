"""****************************************************************************
 Name: csv
 Purpose: Create and handle printing to a csv file. 
 
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

class csv ():
    """csv is used to create, update and print information to a csv file.
    Attributes:
        csv Name (optional): A String for the name of the csv file.
        headers (optional): A list of headers to populate the csv file."""
    
    __csvfile = '' # Global variable - csv file name.
    __header = []  # Global variable - The header of the csv file.
    __content = [] # List of Lists. Each internal list contains one row.
    __records = 0
    
    # Create the csv file (.csv file) and populate the first line with headers.
    def __init__ (self, output, csv_name = 'csv', headers = []):
        """init starts the stop watch, creates the Log '.txt' file and populates 
        it with the current date and time."""
        
        global __csvfile, __header # Accessed Globals
        __csvfile = output + '\\' + csv_name  + '.csv'
        __header = headers
        
        output_file = open (__csvfile, 'w') # Open CSV hard copy
        for item in __header:    # Print the header to the CSV.
            output_file.write(item + ',')
        output_file.close() # Close the csv hard copy
        
#______________________________________________________________________________
#***Methods********************************************************************
    def get_header (self):
        """Return the csv header as a list."""
        return __header
    
    
    def get_name (self):
        """Return the csv path and name."""
        return __csvfile
    
    
    def get_records (self):
        """Return the number of records in the csv."""
        return __records
    
    
    def print_line (self, row_list):
        """Prints a line to the csv file."""
        global __content, __records    # Accessed Globals
        __content.append(row_list)
        
        output_file = open (__csvfile, 'w') # Open CSV hard copy
        for item in __header: # Print the header to the CSV.
            output_file.write(item + ',')
        output_file.write('\n') # Move cursor to next line
        
        # Write __content to the CSV. 
        for each_list in __content: # Iterate through each List
            for each_item in each_list: # Iterate through Items
                output_file.write(each_item + ',')
            output_file.write('\n') # Move cursor to next row in CSV
        
        output_file.close() # Close the csv hard copy
        __records += 1 # Increase the Record Count by 1
        return "PRINTED TO CSV"

             
#Driver
def main():
    pass
if __name__ == '__main__':
    main()

        
        