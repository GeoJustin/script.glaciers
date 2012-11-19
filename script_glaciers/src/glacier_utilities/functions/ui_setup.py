"""****************************************************************************
 Name:         glacier_utilities.functions.ui_setup
 Purpose:     
 
Created:         Nov 19, 2012
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
import sys
import Tkinter as TK
import tkMessageBox
import tkFileDialog


def check_arcpy (frame, frow = 0, fcolumn = 0, fcolumnspan = 1, fpadx = 6, fpady = 6):
    """Function: Check Modules
    Attempts to import critical modules and returns whether the were imported
    successfully or not. Also, displays a label on the user interface listing
    the modules availability."""
    arcpy_module = False

    try:
        import arcpy                            #@UnresolvedImport @UnusedImport
        arcpy_module = True
    except: pass

    modules_frame = TK.Frame(frame)
    modules_frame.grid(row=frow, column=fcolumn, columnspan = fcolumnspan, pady = fpady)

    arcpy_label = TK.Label (modules_frame, text= "ArcPy Module - ")
    arcpy_label.pack(side=TK.LEFT)

    arcpy_found = TK.Label (modules_frame, text = 'Available', fg = "#008000")
    if arcpy_module == False:
        arcpy_found.configure(text = "NOT Available", fg = "#ff0000")
    arcpy_found.pack(side=TK.LEFT)
    
    return arcpy_module


def get_directory (string):
    """Method: Get directory
    An extension of the tkFileDialog module to be used internally for purposes
    of selecting a directory using a navigable user interface."""
    vDirectory = tkFileDialog.askdirectory(title='Please select a directory')
    if len(vDirectory) > 0:
        string.set (vDirectory)
        return vDirectory
    
    
def get_file (string, types):
    """Method: Get file
    Purpose - An extension of the tkFileDialog module to be used internally."""
    vFile = tkFileDialog.askopenfilename (title='Please select a file', filetypes = types)
    if len(vFile) > 0:
        string.set (vFile)
        return vFile


def get_help (help_file = ''):
    """ Function: Get Help
    A function that opens the help file which gives instructions on running
    the application and how the application works."""
    tkMessageBox.showwarning ('Warning', 'Help currently not available.')
        

def exit_application (master):
    """Function: exit
    System exit function to stop the program and destroy the GUI window."""
    try: 
        master.destroy() # Destroy master / main / root window
        sys.exit() # Exit the system
    except: 
        sys.exit() # Exit the system
    