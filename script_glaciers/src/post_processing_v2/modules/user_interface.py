"""****************************************************************************
 Name: post_processing_v2.GUI_Post_Proc
 Purpose: Graphical User Interface for Post Process application.
 
Created: Aug 24, 2012
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
#Add the current directory to python search path.
import sys
import os
sys.path.append (os.path.dirname(os.path.abspath(__file__)) + '\\modules')

import Tkinter as TK
import tkMessageBox
import tkFileDialog
import variables                                        #@UnresolvedImport
import post_processing                                  #@UnresolvedImport
                    
class GUI (object):
    """Graphical User Interface (GUI) for Post Process application."""

    def __init__ (self, master):
        """Setup the main GUI window and load default or starting settings."""
        
        VAR = variables.Variables() # Start the variables reader
        
        self.get_menubar(master) # Setup menu bar items
        
        # Setup file / folder input output dialog boxes
        input_string, dem_string, output_string = self.get_io (master, VAR)
        self.__input_string = input_string
        self.__dem_string = dem_string
        self.__output_string = output_string
        
        #Settings Frame
        options_frame = TK.LabelFrame(master, text= 'Parameters')
        options_frame.grid (row =3, column =0, columnspan = 3, padx =6, pady = 6)
        
        # Setup Centerline options
        centerline_boolean, cellsize_string, smoothing_string, cellsize_entry, smoothing_entry= self.get_centerline (options_frame, VAR)
        self.__centerline_boolean = centerline_boolean
        self.__cellsize_string = cellsize_string
        self.__smoothing_string = smoothing_string
        self.__cellsize_entry = cellsize_entry
        self.__smoothing_entry = smoothing_entry
        
        # Setup optional table check button frame
        hypsometry_boolean, slope_boolean, aspect_boolean = self.get_tables (options_frame, VAR)
        self.__hypsometry_boolean = hypsometry_boolean
        self.__slope_boolean = slope_boolean
        self.__aspect_boolean = aspect_boolean
        
        # Setup optional populate field check buttons
        glims_boolean, rgi_boolean = self.get_populate (options_frame, VAR)
        self.__glims_boolean = glims_boolean
        self.__rgi_boolean = rgi_boolean
        
        # Setup application parameters needed at runtime i.e. scale raster
        scaling_string, buffer_string = self.get_parameters (options_frame, VAR)
        self.__scaling_string = scaling_string
        self.__buffer_string = buffer_string
        
        # Setup bin options for application
        min_string, max_string, size_string = self.get_bins (options_frame, VAR)
        self.__min_string = min_string
        self.__max_string = max_string
        self.__size_string = size_string
        
        # Setup a restore defaults button for the application
        self.reset_default (options_frame, VAR)
        
        # Setup Module checks
        arcpy_found = self.check_modules (master)
        
        # Setup command buttons
        run_button = self.get_buttons (master, master, VAR)
        
        # Disable run button if critical modules are not found
        if arcpy_found == False:
            run_button.configure (state=TK.DISABLED) #Disable if modules not available
        
        self.enable() # Enable or disable buttons depending on need


    def check_modules (self, frame):
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
        modules_frame.grid(row=4, column=0, columnspan = 3, pady = 6)

        arcpy_label = TK.Label (modules_frame, text= "ArcPy Module - ")
        arcpy_label.pack(side=TK.LEFT, padx = (6,0))

        arcpy_found = TK.Label (modules_frame, text = 'Available', fg = "#008000")
        if arcpy_module == False:
            arcpy_found.configure(text = "NOT Available", fg = "#ff0000")
        arcpy_found.pack(side=TK.LEFT, padx = (0,12))
        
        return arcpy_module


    def enable (self):
        """Function: Enable
        Enables or Disables widgets as needed."""
        if self.__centerline_boolean.get() == False and self.__slope_boolean.get() == False and self.__aspect_boolean.get() == False: 
            self.__cellsize_entry.configure (state=TK.DISABLED)
            self.__smoothing_entry.configure (state=TK.DISABLED)
            
        if self.__centerline_boolean.get() == True or self.__slope_boolean.get() == True or self.__aspect_boolean.get() == True:
            self.__cellsize_entry.configure (state=TK.NORMAL)
            self.__smoothing_entry.configure (state=TK.NORMAL)


    def exit (self, master):
        """Function: exit
        System exit function to stop the program and destroy the GUI window."""
        master.destroy()
        try: self.root.destroy()
        except: pass
        sys.exit()
        
            
    def get_bins (self, frame, VAR):
        """ Function: Get Bins
        Sets up a frame to hold the bin size options"""
        settings_frame = TK.Frame (frame, relief = TK.RIDGE, bd = 1)
        settings_frame.grid (row =2, column =0, columnspan = 3, padx = (6,0), pady = (0,6), sticky = TK.W)
        
        label_minbin = TK.Label(settings_frame, text='Min. Bin')
        label_minbin.pack(side=TK.LEFT, padx = (12,0), pady = (6,6))
        
        min_string = TK.StringVar()
        min_entry = TK.Entry (settings_frame, textvariable = min_string, width = 6, justify = TK.CENTER)
        min_entry.pack(side=TK.LEFT, padx = (12,12), pady = (6,6))
        min_string.set(VAR.read_variable("MINBIN"))
        
        label_maxbin = TK.Label(settings_frame, text='Max. Bin')
        label_maxbin.pack(side=TK.LEFT)
        
        max_string = TK.StringVar()
        max_entry = TK.Entry (settings_frame, textvariable = max_string, width = 6, justify = TK.CENTER)
        max_entry.pack(side=TK.LEFT, padx = (3,12), pady = (6,6))
        max_string.set(VAR.read_variable("MAXBIN"))
        
        label_size = TK.Label(settings_frame, text='Size')
        label_size.pack(side=TK.LEFT)
        
        size_string = TK.StringVar()
        size_entry = TK.Entry (settings_frame, textvariable = size_string, width = 6, justify = TK.CENTER)
        size_entry.pack(side=TK.LEFT, padx = (3,12), pady = (6,6))
        size_string.set(VAR.read_variable("BINSIZE"))

        return min_string, max_string, size_string


    def get_buttons (self, master, frame, VAR):
        """Function: Get Buttons
        Sets up control buttons for the application (help, exit and run). The run
        button, in this case, writes the input variables to the varaible file (.var)
        for use by the application at runtime and saves selections for future use."""
        
        buttonFrame = TK.Frame(frame)
        buttonFrame.grid(row=5, column=0, columnspan = 3, pady = 6)

        #Help button (calls get help function)
        helpButton = TK.Button(buttonFrame, text = "Help", height = 1,
         width = 12, command=self.get_help)
        helpButton.pack(side=TK.LEFT, padx = (6,12))

        #Exit application button (calls exit function)
        def __callback_exit(): 
            self.exit(master)
        exitButton = TK.Button(buttonFrame, text = "Exit", height = 1,
         width = 12, command= __callback_exit)
        exitButton.pack(side=TK.LEFT, padx = (6,12))

        #Run Program Button
        def __callback_runImport ():
            if self.__input_string.get() <> 'Required' and self.__output_string.get() <> 'Required' and self.__dem_string.get() <> 'Required':
            
                # Write variables to .var file
                VAR.set_variable("INPUT", "STRING", self.__input_string.get())
                VAR.set_variable("DEM", "STRING", self.__dem_string.get())
                VAR.set_variable("OUTPUT", "STRING", self.__output_string.get())
                VAR.set_variable("CENTERLINES", "BOOLEAN", self.__centerline_boolean.get())
                VAR.set_variable("EU_CELL_SIZE", "INTEGER", self.__cellsize_string.get())
                VAR.set_variable("SMOOTHING", "INTEGER", self.__smoothing_string.get())
                VAR.set_variable("HYPSOMETRY", "BOOLEAN", self.__hypsometry_boolean.get())
                VAR.set_variable("SLOPE", "BOOLEAN", self.__slope_boolean.get())
                VAR.set_variable("ASPECT", "BOOLEAN", self.__aspect_boolean.get())
                VAR.set_variable("GLIMSIDS", "BOOLEAN", self.__glims_boolean.get())
                VAR.set_variable("RGIIDS", "BOOLEAN", self.__rgi_boolean.get())
                VAR.set_variable("SCALING", "INTEGER", self.__scaling_string.get())
                VAR.set_variable("BUFFER", "INTEGER", self.__buffer_string.get())
                VAR.set_variable("MINBIN", "INTEGER", self.__min_string.get())
                VAR.set_variable("MAXBIN", "INTEGER", self.__max_string.get())
                VAR.set_variable("BINSIZE", "INTEGER", self.__size_string.get())
                
                output_created = False
                try: # Creates an output folder to place files. This guarantees and empty folder
                    output = self.__output_string.get() + '\\Post_Processing'
                    os.makedirs(output)
                    output_created = True
                except: 
                    tkMessageBox.showwarning ('Warning', 'Output Folder can not be written. It may already exist.')
                                        
                if output_created == True:
                    # Remove GUI window and destroy it.
                    try: master.destroy()
                    except: pass
                    try: self.root.destroy()
                    except: pass
                    
                    # RUN APPLICATION
                    post_processing.process(self.__input_string.get(), output, self.__dem_string.get(), VAR)
                
            else: 
                tkMessageBox.showwarning ('Warning', 'You must select Input and Output files.')
                
        run_button = TK.Button(buttonFrame, text = "Run", height = 1, width = 12, command= __callback_runImport)
        run_button.pack(side=TK.LEFT, padx = 6)
   
   
    def get_centerline (self, frame, VAR):
        """Function: Get Centerline
        Sets up the options for generating center line information."""
        centerline_frame = TK.Frame (frame, relief = TK.RIDGE, bd = 1)
        centerline_frame.grid (row =0, column =0, columnspan = 3, padx = (6,6), pady = (3,0), sticky = TK.W)
        
        label_centerline = TK.Label(centerline_frame, text='Output Centerline')
        label_centerline.pack(side=TK.LEFT, padx = (12,0), pady = (6,6))
        
        centerline_boolean = TK.BooleanVar()
        centerline_boolean.set(VAR.read_variable("CENTERLINES"))
        
        def __callback_centerline ():
            self.enable()
        check_centerline = TK.Checkbutton(centerline_frame, text='', variable = centerline_boolean, command=__callback_centerline, onvalue = True, offvalue = False)
        check_centerline.pack(side=TK.LEFT, padx = 0, pady = 6)
        
        
        label_cellsize = TK.Label(centerline_frame, text='Cell Size')
        label_cellsize.pack(side=TK.LEFT)
        
        cellsize_string = TK.StringVar()
        cellsize_entry = TK.Entry (centerline_frame, textvariable = cellsize_string, width = 6, justify = TK.CENTER)
        cellsize_entry.pack(side=TK.LEFT, padx = (3,12), pady = (6,6))
        cellsize_string.set(VAR.read_variable("EU_CELL_SIZE"))
        
        label_smoothing = TK.Label(centerline_frame, text='Smoothing Factor')
        label_smoothing.pack(side=TK.LEFT)
        
        smoothing_string = TK.StringVar()
        smoothing_entry = TK.Spinbox(centerline_frame, textvariable = smoothing_string, from_=0, to=10, width = 4,justify = TK.CENTER, wrap = TK.TRUE)
        smoothing_entry.pack(side=TK.LEFT, padx = (3,12), pady = (6,6))
        smoothing_string.set(VAR.read_variable("SMOOTHING"))
        
        return centerline_boolean, cellsize_string, smoothing_string, cellsize_entry, smoothing_entry
       
   
    def get_directory (self, string):
        """Method: Get directory
        An extension of the tkFileDialog module to be used internally for purposes
        of selecting a directory using a navigable user interface."""
        vDirectory = tkFileDialog.askdirectory(title='Please select a directory')
        if len(vDirectory) > 0:
            string.set (vDirectory)
            return vDirectory
        
        
    def get_file (self, string, types):
        """Method: Get file
        Purpose - An extension of the tkFileDialog module to be used internally."""
        vFile = tkFileDialog.askopenfilename (title='Please select a file', filetypes = types)
        if len(vFile) > 0:
            string.set (vFile)
            return vFile
   
   
    def get_help (self):
        """ Function: Get Help
        A function that opens the help file which gives instructions on running
        the application and how the application works."""
        tkMessageBox.showwarning ('Warning', 'Help currently not available.')
        
        
    def get_io (self, frame, VAR):
        """Function: File IO
        Generates input file selection menu items (label, text input box and file/
        folder selection dialog)."""
        input_frame = TK.Frame (frame)
        input_frame.grid (row =0, column =0, columnspan = 1, pady = 6)

        #Select Input Frame
        input_label = TK.Label (input_frame, text='Select Glaciers')
        input_label.grid(row=0, column = 0, sticky = TK.W, padx = 6)

        def __callback_select_input ():
            self.get_file (input_string, [('Shapefile','*.shp')])
        input_string = TK.StringVar()
        input_entry = TK.Entry (input_frame, textvariable = input_string, width = 50)
        input_entry.grid(row=0, column = 1, padx = 6)
        input_string.set(VAR.read_variable("INPUT"))

        input_file = TK.Button(input_frame, text = 'Select', height = 1, width = 8, command = __callback_select_input)
        input_file.grid(row=0, column = 2, padx = (0,6), pady = (0,6))
        
        #Select DEM Frame
        dem_label = TK.Label (input_frame, text='Select DEM')
        dem_label.grid(row=1, column = 0, sticky = TK.W, padx = 6, pady = (6,6))

        def __callback_dem ():
            self.get_file (dem_string, [('Image', '*.img'), ('Tiff', '*.tif')])
        dem_string = TK.StringVar()
        dem_entry = TK.Entry (input_frame, textvariable = dem_string, width = 50)
        dem_entry.grid(row=1, column = 1, padx = 6, pady = (6,6))
        dem_string.set(VAR.read_variable("DEM"))

        dem_file = TK.Button(input_frame, text = 'Select', height = 1, width = 8, command = __callback_dem)
        dem_file.grid(row=1, column = 2, padx = (0,6), pady = (0,6))

        #Select Output Frame
        output_label = TK.Label (input_frame, text='Select Output')
        output_label.grid(row=2, column = 0, sticky = TK.W, padx = 6, pady = (6,6))

        def __callback_output ():
            self.get_directory (output_string)
        output_string = TK.StringVar()
        output_entry = TK.Entry (input_frame, textvariable = output_string, width = 50)
        output_entry.grid(row=2, column = 1, padx = 6, pady = (6,6))
        output_string.set(VAR.read_variable("OUTPUT"))

        output_file = TK.Button(input_frame, text = 'Select', height = 1, width = 8, command = __callback_output)
        output_file.grid(row=2, column = 2, padx = (0,6), pady = (0,6))
        
        return input_string, dem_string, output_string


    def get_menubar (self, frame):
        """Function: Menu Bar
        Menu bar bar along the top of the window."""
        menubar = TK.Menu(frame)

        def __callback_exit():
            self.exit(frame)
        filemenu = TK.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=__callback_exit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = TK.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Files", command=self.get_help)
        menubar.add_cascade(label="Help", menu=helpmenu)

        frame.config(menu=menubar)


    def get_parameters (self, frame, VAR):
        """Function: Get Parameters
        Set up a frame to hold parameter options need to run the application
         at runtime."""
        parameters_frame = TK.Frame (frame, relief = TK.RIDGE, bd = 1)
        parameters_frame.grid (row =1, column =2, padx = (0,6), pady = 3, sticky = TK.W)
        
        label_parameters = TK.Label(parameters_frame, text='Parameters')
        label_parameters.grid (row =0, column = 0, padx = 6, pady = (3,0))
        
        scaling_frame = TK.Frame (parameters_frame)
        scaling_frame.grid (row =1, column =0, sticky = TK.W)
        
        label_scaling = TK.Label(scaling_frame, text='Scaling')
        label_scaling.grid (row =0, column = 0, padx = 6, pady = 0, sticky = TK.W)
        
        scaling_string = TK.StringVar()
        scale_options = ["1", "10", "100", "1000", "10000", "100000", "1000000"]
        option_entry = TK.Spinbox(scaling_frame, textvariable = scaling_string, values = scale_options, width = 10,justify = TK.CENTER, wrap = TK.TRUE)
        option_entry.grid (row = 0, column = 1, padx = (0, 6), pady = 0, sticky = TK.W)
        scaling_string.set(VAR.read_variable("SCALING"))
        
        buffer_frame = TK.Frame (parameters_frame)
        buffer_frame.grid (row =2, column =0, pady = (0, 27), sticky = TK.W)
        
        label_buffer = TK.Label(buffer_frame, text='Buffer Fact.')
        label_buffer.grid (row =0, column = 0, padx = 6, pady = 3, sticky = TK.W)
        
        buffer_string = TK.StringVar()
        buffer_entry = TK.Spinbox(buffer_frame, textvariable = buffer_string, from_=0, to=10, width = 6,justify = TK.CENTER, wrap = TK.TRUE)
        buffer_entry.grid (row =0, column = 1, padx = (3,12), pady = (3, 0))
        buffer_string.set(VAR.read_variable("BUFFER"))
        
        return scaling_string, buffer_string
    

    def get_populate (self, frame, VAR):
        """Function: Get Populate
        Sets up a frame to hold optional populate field check buttons."""
        populate_frame = TK.Frame (frame, relief = TK.RIDGE, bd = 1)
        populate_frame.grid (row =1, column =1, padx = 3, pady = 3, sticky = TK.W)
        
        label_populate = TK.Label(populate_frame, text='Populate Attributes')
        label_populate.grid (row =0, padx = 9, pady = (3,0))
            
        glims_boolean = TK.BooleanVar()
        check_glims = TK.Checkbutton(populate_frame, text="GLIMS ID's", variable = glims_boolean, onvalue = True, offvalue = False)
        check_glims.grid (row =1, padx = 10, sticky = TK.W)
        glims_boolean.set(VAR.read_variable("GLIMSIDS"))
        
        rgi_boolean = TK.BooleanVar()
        check_rgi = TK.Checkbutton(populate_frame, state = TK.DISABLED, text="RGI ID's", variable = rgi_boolean, onvalue = True, offvalue = False)
        check_rgi.grid (row =2, padx = 10, pady = (0,26), sticky = TK.W)
        rgi_boolean.set(VAR.read_variable("RGIIDS"))

        return glims_boolean, rgi_boolean
    

    def get_tables(self, frame, VAR):
        """Function: Get Tables
        Sets up a frame to hold optional table check buttons"""
        table_frame = TK.Frame (frame, relief = TK.RIDGE, bd = 1)
        table_frame.grid (row =1, column =0, padx = (6,0), pady = 3, sticky = TK.W)
        
        label_tables = TK.Label(table_frame, text='Output Tables')
        label_tables.grid (row =0, padx = 12, pady = (3,0), sticky = TK.W)
        
        hypsometry_boolean = TK.BooleanVar()
        check_hypsometry = TK.Checkbutton(table_frame, text='Hypsometry', variable = hypsometry_boolean, onvalue = True, offvalue = False)
        check_hypsometry.grid (row =1, padx = 14, sticky = TK.W)
        hypsometry_boolean.set(VAR.read_variable("HYPSOMETRY"))
        
        def __callback_tables():
            self.enable()
            
        slope_boolean = TK.BooleanVar()
        check_slope = TK.Checkbutton(table_frame, text='Slope', variable = slope_boolean, onvalue = True, offvalue = False, command=__callback_tables)
        check_slope.grid (row =2, padx = 14, sticky = TK.W)
        slope_boolean.set(VAR.read_variable("SLOPE"))
        
        aspect_boolean = TK.BooleanVar()
        check_aspect = TK.Checkbutton(table_frame, text='Aspect', variable = aspect_boolean, onvalue = True, offvalue = False, command=__callback_tables)
        check_aspect.grid (row =3, padx = 14, pady = (0,3), sticky = TK.W)
        aspect_boolean.set(VAR.read_variable("ASPECT"))

        return hypsometry_boolean, slope_boolean, aspect_boolean
   
   
    def reset_default (self, frame, VAR):
        """Function: reset Defaults
        Sets up a button to reset the defaults on all option fields """
        def __callback_reset_default ():
            VAR.reset_defaults()
            
            self.__input_string.set(VAR.read_variable("INPUT"))
            self.__dem_string.set(VAR.read_variable("DEM"))
            self.__output_string.set(VAR.read_variable("OUTPUT"))
            self.__centerline_boolean.set(VAR.read_variable("CENTERLINES"))
            self.__cellsize_string.set(VAR.read_variable("EU_CELL_SIZE"))
            self.__smoothing_string.set(VAR.read_variable("SMOOTHING"))
            self.__hypsometry_boolean.set(VAR.read_variable("HYPSOMETRY"))
            self.__slope_boolean.set(VAR.read_variable("SLOPE"))
            self.__aspect_boolean.set(VAR.read_variable("ASPECT"))
            self.__glims_boolean.set(VAR.read_variable("GLIMSIDS"))
            self.__rgi_boolean.set(VAR.read_variable("RGIIDS"))
            self.__scaling_string.set(VAR.read_variable("SCALING"))
            self.__buffer_string.set(VAR.read_variable("BUFFER"))
            self.__min_string.set(VAR.read_variable("MINBIN"))
            self.__max_string.set(VAR.read_variable("MAXBIN"))
            self.__size_string.set(VAR.read_variable("BINSIZE"))
            
            self.enable()
            
        defaultButton = TK.Button(frame, text = "Default", height = 1, width = 10, command=__callback_reset_default)
        defaultButton.grid (row =2, column =2, padx = (3,6), pady = (0,6), sticky = TK.E)

        
    
#DRIVER
def driver():
    main = TK.Tk()
    main.title ('Post Process - v.2.0')
    GUI (main)
    main.mainloop()

if __name__ == '__main__':
    driver()