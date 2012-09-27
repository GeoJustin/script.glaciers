"""****************************************************************************
 Name: graphing_operations.plot_glacier_area
 Purpose: Plots Area from csv files, generated from the post processing script,
     against one another.
 
Created: Feb. 06, 2011
Author:  Anthony Arendt (arendta@gi.alaska.edu)
Location: Geophysical Institute | University of Alaska, Fairbanks
Contributors:
    Justin L. Rich (justin.rich@gi.alaska.edu) - Edited: Sept. 26, 2012

Parameters: This module requires several modules including scipy, numpy and
    matplotlib which are all part of pylab. See http://www.scipy.org/PyLab
    for more information and downloads of these modules.

Copyright:   (c) Arendta 2011
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
from pylab import *                                         #@UnusedWildImport

class plot_glacier_area():
    """ Plot glaciers is designed to take .CSV files generated from the 'post_processing'
    script, one map date or earlier date and one modern date or later date, and plot them
    against each other in order to derive a plot of area data."""
    
    def __init__ (self, map_date, modern_date, output_file, output_name, area_column_map_date, area_column_modern_date,
                   area_x_label, area_y_label, area_title, legend_map_date, legend_modern_date, header):
        """This function auto runs the contents of the plot_glaciers class when run."""
        
        # Read in the map date (earlier) CSV file
        area_early = []                     # List to hold the earlier area data
        earlier_data = open(map_date,'r')   # Read in the earlier csv file.
        # If header is set to True skip the first line and continue on to the rest
        if header == True: earlier_data.next()
        for aRow in earlier_data:   # For each row in the csv
            line = aRow.split(',')  # Split each row based on a comma
            # Add values from the current row to the appropriate earlier data lists
            area_early.append(float(line[area_column_map_date])*1e6) # Add area to the area list

        # Read in modern data CSV file
        area_modern = []                    # List to hold the modern area data
        modern_data = open(modern_date,'r') # Read in the modern csv file.
        # If header is set to True skip the first line and continue on to the rest
        if header == True: modern_data.next()
        for aRow in modern_data:    # For each row in the csv
            line = aRow.split(',')  # Split each row based on a comma
            # Add values from the current row to the appropriate modern data lists
            area_modern.append(float(line[area_column_modern_date])*1e6) # Add area to the area list
            
        
        # Area plot based on earlier and later data sets
        fig = plt.figure() # Create instance of a plot
        ax = fig.add_subplot(111) # Define plot grid parameters (1x1 grid, first plot) for only one plot
        # Add data to the plot, set labels and define the colors
        ax.hist([log10(area_early),log10(area_modern)],bins=40,label=(legend_map_date,legend_modern_date),color=('orange','gray'))
        ax.legend()                     # Add legend to Area Plot
        ax.set_xlabel(area_x_label)     # Add x label to Area Plot
        ax.set_ylabel(area_y_label)     # Add y label  to Area Plot
        ax.set_title(area_title)        # Add title to Area Plot
        savefig(output_file + '\\' + output_name + '_Histo_Area.pdf')
        
        # Print out the number of glaciers in both CSV files (because we can)
        print 'Number of Glaciers, early: ' + str(len(area_early))
        print 'Number of Glaciers, later: ' + str(len(area_modern))
        print 'complete'


#_______________________________________________________________________________
#***  DRIVER *******************************************************************
# HARD CODE INPUTS HERE !
def main():
    # Input CSV files (generated from post process scripts)
    map_date = r'A:\Desktop\Test\KLGO_DRGs_In_BinStats.csv'
    modern_date = r'A:\Desktop\Test\KLGO_2010_BinStats.csv'
    output_folder = r'A:\Desktop\Test'          # Output folder to place files
    output_name = 'KLGO'                        # Name to attach to the files
    
    # Column containing area in km2
    area_column_map_date = 6
    area_column_modern_date = 6

    # Plot Labels - Area - Histogram of Surface Area 
    area_x_label = 'log10 Area (sq. meters)'
    area_y_label = 'Number of Glaciers'
    legend_map_date = '1950s'
    legend_modern_date = 'Late 2000s'
    area_title = ''  
    
    # If a header is included in the input files set True if not set False
    header = True
    
    plot_glacier_area (map_date, modern_date, output_folder, output_name, area_column_map_date, area_column_modern_date,
                    area_x_label, area_y_label, area_title, legend_map_date, legend_modern_date, header)

if __name__ == '__main__':
    main()