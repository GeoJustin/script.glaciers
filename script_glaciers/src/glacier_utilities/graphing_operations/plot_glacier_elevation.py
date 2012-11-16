"""****************************************************************************
 Name: graphing_operations.plot_glacier_elevation
 Purpose: Plots elevation from csv files generated from the post processing
      script.
 
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

class plot_glacier_elevation():
    """ Plot glaciers is designed to take .CSV files generated from the 'post_processing'
    script, one map date or earlier date and one modern date or later date, and plot them
    against each other in order to derive a plot of elevation data."""
    
    def __init__ (self, map_date, modern_date, output_file, output_name, area_column_map_date, area_column_modern_date,
                    elev_x_label, elev_y_label, elev_title, legend_map_date, legend_modern_date, header):
        """This function auto runs the contents of the plot_glaciers class when run."""
        
        # Read in the map date (earlier) CSV file
        mean_elev_early = []                # List to hold the earlier elevation data
        earlier_data = open(map_date,'r')   # Read in the earlier csv file.
        # If header is set to True skip the first line and continue on to the rest
        if header == True: earlier_data.next()
        for aRow in earlier_data:   # For each row in the csv
            line = aRow.split(',')  # Split each row based on a comma
            # Add values from the current row to the appropriate earlier data lists
            mean_elev_early.append(float(line[area_column_map_date])) # Add elevation to the elevation list

        # Read in modern data CSV file
        mean_elev_modern = []               # List to hold the modern elevation data
        modern_date = open(modern_date,'r') # Read in the modern csv file.
        # If header is set to True skip the first line and continue on to the rest
        if header == True: modern_date.next()
        for aRow in modern_date:    # For each row in the csv
            line = aRow.split(',')  # Split each row based on a comma
            # Add values from the current row to the appropriate modern data lists
            mean_elev_modern.append(float(line[area_column_modern_date])) # Add elevation to the elevation list
        
        
        # Mean elevation plot based on earlier and later data sets
        fig = plt.figure()  # Create instance of a plot
        ax = fig.add_subplot(111) # Define plot grid parameters (1x1 grid, first plot) for only one plot
        # Add data to the plot, set labels and define the colors
        ax.hist([mean_elev_early, mean_elev_modern],bins=40,label=(legend_map_date, legend_modern_date),color=('orange','gray'))
        ax.legend()                     # Add a legend to Elevation Plot
        ax.set_xlabel(elev_x_label)     # Add x label to Elevation Plot
        ax.set_ylabel(elev_y_label)     # Add y label  to Elevation Plot
        ax.set_title(elev_title)        # Add title to Elevation Plot
        savefig(output_file + '\\' + output_name + '_Histo_Mean_Elev.pdf') # Save plot as
        
        # Print out the number of glaciers in both CSV files (because we can)
        print 'Number of Glaciers, early: ' + str(len(mean_elev_early))
        print 'Number of Glaciers, later: ' + str(len(mean_elev_modern))
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
    area_column_map_date = 10
    area_column_modern_date = 10
    
    # Plot Labels - Mean Elevation - Histogram of Surface Area 
    elev_x_label = 'Mean Elevation (m)'
    elev_y_label = 'Number of Glaciers'
    legend_map_date = '1950s'
    legend_modern_date = 'Late 2000s'
    elev_title =  ''
    
    # If a header is included in the input files set True if not set False
    header = True
    
    plot_glacier_elevation (map_date, modern_date, output_folder, output_name, area_column_map_date, area_column_modern_date,
                     elev_x_label, elev_y_label, elev_title, legend_map_date, legend_modern_date, header)

if __name__ == '__main__':
    main()