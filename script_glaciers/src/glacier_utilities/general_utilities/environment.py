"""****************************************************************************
 Name:         glacier_utilities.general_utilities.environment
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
import glacier_utilities.output_file.output_file_log as LOG

class setup_arcgis (object):
    """Sets up a work environment for working with ArcGIS. Class is designed
    to reduce redundant entries across multiple scripts."""

    def __init__(self, output_folder):
        """Constructor:  Sets up an Arc GIS work environment"""
        self.workspace = ''     # Set workspace Variable
        self.log = object       # Set log file to variable
        
        self.setup_arcgis_workspace(output_folder)
    
    
    def setup_arcgis_workspace (self, output_folder, arcinfo = True, spatial = True):
        """Function: Setup ArcGIS workspace
        Imports the ArcPy module, sets up a workspace, starts a log file
        and then returns them"""
        try: # Start Log file and write it to the output folder
            l = LOG.Log(output_folder)
        except: 
            sys.exit('Log file could not be written to the output folder.')
        
        if arcinfo == True: # If arc info is needed
            try:  # Get ArcInfo License if it's available
                import arcinfo                  #@UnresolvedImport @UnusedImport
            except:
                l.print_line('ArcInfo license NOT available')
                sys.exit('ArcInfo license NOT available')

        if spatial == True: # If arc GIS spatial analysis is needed
            try: # Check out Spatial Analyst extension if available.
                if ARCPY.CheckExtension('Spatial') == 'Available':
                    ARCPY.CheckOutExtension('Spatial')
                    l.print_line('Spatial Analyst is available')
            except:
                l.print_line('Spatial Analyst extension not available')
                sys.exit('Spatial Analyst extension not available')

        try: # Set environment
            scratch_space = output_folder + '\\workspace'
            os.makedirs(scratch_space) # Create Workspace
            ARCPY.env.workspace = scratch_space
        except:
            l.print_line('WARNING - Workspace folder already exists.')
            sys.exit('WARNING - Workspace folder already exists.')
    
        self.workspace = scratch_space  # Set workspace Variable
        self.log = l                    # Set log file to variable
    
        return True
    
    
    def delete_items (self, items = []):
        """Function: Delete Items
        Takes a list of items and deletes them one by one using the 
        Delete tool within ARCPY"""
        deleted_all = True
        for item in items:
            try: # Try to Delete items
                ARCPY.Delete_management(item)
            except:
                deleted_all = False
        return deleted_all
    

    def remove_workspace (self):
        """Function: Remove Workspace
        Removes the workspace held by this function"""
        try: # Try to Delete items
            ARCPY.Delete_management(self.workspace)
        except: 
            return False
        return True


def driver ():
    setup_arcgis ()
if __name__ == '__main__':
    driver()