"""****************************************************************************
 Name: post_processing_v2.modules.functions_data_added
 Purpose: 
 
Created: Oct 19, 2012
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
import arcpy as ARCPY                                       #@UnresolvedImport

def get_median ():
    """Return Median value of all pixels in the given DEM"""
#    try:
#        sorted_list = sorted(value_list) # Sort List
#        middle = len(value_list) / 2 # Find the middle of the list
#        # Check if the list has an even or odd length (0 = Even & 1 = Odd
#        if len(value_list) % 2 == 0: 
#            # If even average middle two values. Remember to -1 since list starts at 0
#            median = str((sorted_list[middle-1] + sorted_list[middle]) / 2.0)
#        else:
#            # If odd get middle value and append it to list
#            median = str(sorted_list[middle])
#        return 
#    except:
#        return 'SOMETHING'