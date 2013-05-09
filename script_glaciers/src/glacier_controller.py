"""****************************************************************************
 Name:         glacier_controller
 Purpose:      Setup a task bar with access to all glacier reformatting and 
            analysis user interfaces.
 
Created:         May 9, 2013
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
import sys, os
sys.path.append (os.path.dirname(os.path.dirname(__file__)))

import Tkinter as TK

class Controller ():

    def __init__ (self, master):
        """Sets up a menu bar. In this case the menu bar runs operations associated
        with RGI formating and Glacier post-processing. Basic menu bar setup is as
        follows:
            1 - Create a File Menu (TK.Menu(var's))
            2 - Add Menu Item (.add_command(var's))
            3 - Add Separator if applicable (.add_separator(var's))
            4 - Add File Menu to Menu Bar (.add_cascade(var's))"""
            
        self.__master_frame = master # Holds the Master Frame as global
        
        # Add an empty frame to control initial master frame size
        mainFrame = TK.Frame(master, width=400, height= 0)
        mainFrame.grid(row=0, column = 0)
        
        menubar = TK.Menu(master) # Start instance of Menu bar

        # File Menu -------------------------
        filemenu = TK.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.exit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        # Format Attribute Columns
        formenu = TK.Menu(menubar, tearoff=0)
        formenu.add_command(label='Format RGI', command=self.format_rgi)
        menubar.add_cascade(label='Format', menu=formenu)
        
        # Generate Attribute Information -------
        genmenu = TK.Menu(menubar, tearoff=0)
        genmenu.add_command(label="Generate RGI ID's", command=self.open_generate_rgiid)
        genmenu.add_command(label="Generate GLIMS ID's", command=self.open_generate_glimsid)
        menubar.add_cascade(label="Generate", menu=genmenu)
        
        # Run Glacier Analysis and Post-Processing
        anlmenu = TK.Menu(menubar, tearoff=0)
        anlmenu.add_command(label="Analyze Folder", command=self.analyze_folder)
        anlmenu.add_separator()
        anlmenu.add_command(label="Post-Process", command=self.postprocess)
        menubar.add_cascade(label='Analysis', menu=anlmenu)

        # Help Menu -------------------------
        helpmenu = TK.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Files", command=self.help)
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        master.config(menu=menubar)
        
        
    def format_rgi (self):
        """Open an instance of Format RGI's controller and replace the 
        contents of the current main window with it."""
        import glacier_interfaces.ui_rgi_format as FORMRGI
        self.__main_frame_cleanup()
        FORMRGI.format_RGI_GUI(self.__master_frame)
        
        
    def open_generate_rgiid (self):
        """Open an instance of the Generate RGI ID's controller and replace
        the contents of the current main window with it."""
        import glacier_interfaces.ui_add_rgiid as RGIID
        self.__main_frame_cleanup()
        RGIID.Populate_RGI_GUI(self.__master_frame)
        
        
    def open_generate_glimsid (self):
        """Open an instance of the Generate GLIMS ID's controller and replace
        the contents of the current main window with it."""
        import glacier_interfaces.ui_add_glimsid as GLIMSID
        self.__main_frame_cleanup()
        GLIMSID.Populate_GLIMS_GUI(self.__master_frame)
        
    
    def analyze_folder (self):
        """Open an instance of the RGI Analysis controller and replaces the 
        contents of the current main window with it."""
        import glacier_interfaces.ui_rgi_analyze as ANALYZE
        self.__main_frame_cleanup()
        ANALYZE.Analyze_RGI(self.__master_frame)
    
    
    def postprocess (self):
        """Open an instance of the Post Processing controller and replace
        the contents of the current main window with it."""
        import glacier_interfaces.ui_postproc as POSTPROC
        self.__main_frame_cleanup()
        POSTPROC.GUI(self.__master_frame)
        
        
    def help (self):
        """Open a help menu that includes descriptions of all processes and 
        information on their inputs and basic descriptions of how they work."""
        import webbrowser
        helpfile = os.path.dirname(os.path.abspath(__file__)) + '\\documentation\\PostProcessing.jpg'
        webbrowser.open(helpfile)
        
        
    def exit (self):
        """Destroys the current user interface window and stops all current 
        processes associated with it."""
        self.master.destroy()
        sys.exit()
    
    def __main_frame_cleanup (self):
        """PRIVATE: A function that cleans the current main frame window for the 
        purpose of adding new content to it."""
        for widget in self.__master_frame.grid_slaves():
            widget.grid_remove()
        
            
# Window Driver -------------------------------------------
def driver():
    main = TK.Tk()
    main.title ('Glacier Post-Processing')
    Controller (main)
    main.mainloop()
    
if __name__ == '__main__':
    driver()