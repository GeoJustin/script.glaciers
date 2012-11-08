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
import variables                                        #@UnresolvedImport

class GUI ():
    """Graphical User Interface (GUI) for Post Process application."""

    def __init__ (self, master):
        """Setup the main GUI window and load default or starting settings."""
        
        VAR = variables.Variables() # Start the variables reader
        
        #______________________________________________________________________
        #*******Menu Bar*******************************************************
        def __callback_Help (): #This is also used by 'Help' button.
            import webbrowser
            helpfile = os.path.dirname(os.path.abspath(__file__)) + '\\Help.html'
            webbrowser.open(helpfile)

        def __callback_Exit (): #This is also used by 'Exit' button
            master.destroy()
            try: self.root.destroy()
            except: pass
            sys.exit()

        #File Menu
        menubar = TK.Menu(master)

        filemenu = TK.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=__callback_Exit)
        menubar.add_cascade(label="File", menu=filemenu)

        #Help Menu
        helpmenu = TK.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Files", command=__callback_Help)
        menubar.add_cascade(label="Help", menu=helpmenu)

        master.config(menu=menubar)
        
        #______________________________________________________________________
        #*******Menu Bar*******************************************************
        InputFrame = TK.Frame (master)
        InputFrame.grid (row =0, column =0, columnspan = 1, pady = 6)

        #Select Input Frame
        InputPath = TK.Label (InputFrame, text='Select Glaciers')
        InputPath.grid(row=0, column = 0, sticky = TK.W, padx = 6)

        def callback_SelectedIn ():
            self.getFile (InputString)
        InputString = TK.StringVar()
        InputEntry = TK.Entry (InputFrame, textvariable = InputString, width = 50)
        InputEntry.grid(row=0, column = 1, padx = 6)
        InputString.set(VAR.read_variable("INPUT"))

        inputFile = TK.Button(InputFrame, text = 'Select', height = 1, width = 8,
         command = callback_SelectedIn)
        inputFile.grid(row=0, column = 2, padx = (0,6), pady = (0,6))
        
        #Select DEM Frame
        DEMPath = TK.Label (InputFrame, text='Select DEM')
        DEMPath.grid(row=1, column = 0, sticky = TK.W, padx = 6, pady = (6,6))

        def callback_Selected ():
            self.getFile (DEMString)
        DEMString = TK.StringVar()
        DEMEntry = TK.Entry (InputFrame, textvariable = DEMString, width = 50)
        DEMEntry.grid(row=1, column = 1, padx = 6, pady = (6,6))
        DEMString.set(VAR.read_variable("DEM"))

        DEMFile = TK.Button(InputFrame, text = 'Select', height = 1, width = 8,
         command = callback_Selected)
        DEMFile.grid(row=1, column = 2, padx = (0,6), pady = (0,6))

        #Select Output Frame
        OutputPath = TK.Label (InputFrame, text='Select Output')
        OutputPath.grid(row=2, column = 0, sticky = TK.W, padx = 6, pady = (6,6))

        def callback_SelectedOut ():
            self.getDirectory (OutputString)
        OutputString = TK.StringVar()
        OutputEntry = TK.Entry (InputFrame, textvariable = OutputString, width = 50)
        OutputEntry.grid(row=2, column = 1, padx = 6, pady = (6,6))
        OutputString.set(VAR.read_variable("OUTPUT"))

        OutputFile = TK.Button(InputFrame, text = 'Select', height = 1, width = 8,
         command = callback_SelectedOut)
        OutputFile.grid(row=2, column = 2, padx = (0,6), pady = (0,6))
        
        #______________________________________________________________________
        #*******Settings*******************************************************
        options_frame = TK.LabelFrame(master, text= 'Parameters')
        options_frame.grid (row =3, column =0, columnspan = 2, padx =6, pady = 6)
 
 
        
        function_frame = TK.Frame (options_frame, relief = TK.RIDGE, bd = 1)
        function_frame.grid (row =0, column =0, padx = (20, 3), pady = (6,3), sticky = TK.W)
        
        label_tables = TK.Label(function_frame, text='Output Tables')
        label_tables.grid (row =0, padx = 12, pady = (3,0))
        
        hypsometry_boolean = TK.BooleanVar()
        check_hypsometry = TK.Checkbutton(function_frame, text='Hypsometry', variable = hypsometry_boolean, onvalue = True, offvalue = False)
        check_hypsometry.grid (row =1, padx = 12, sticky = TK.W)
        hypsometry_boolean.set(VAR.read_variable("HYPSOMETRY"))
        
        slope_boolean = TK.BooleanVar()
        check_slope = TK.Checkbutton(function_frame, state = TK.DISABLED, text='Slope', variable = slope_boolean, onvalue = True, offvalue = False)
        check_slope.grid (row =2, padx = 12, sticky = TK.W)
        slope_boolean.set(VAR.read_variable("SLOPE"))
        
        aspect_boolean = TK.BooleanVar()
        check_aspect = TK.Checkbutton(function_frame, state = TK.DISABLED, text='Aspect', variable = aspect_boolean, onvalue = True, offvalue = False)
        check_aspect.grid (row =3, padx = 12, pady = (0,3), sticky = TK.W)
        aspect_boolean.set(VAR.read_variable("ASPECT"))
        
        
        
        populate_frame = TK.Frame (options_frame, relief = TK.RIDGE, bd = 1)
        populate_frame.grid (row =0, column =1, padx = (3,3), pady = (6,3), sticky = TK.W)
        
        label_populate = TK.Label(populate_frame, text='Populate Attributes')
        label_populate.grid (row =0, padx = 12, pady = (3,0))
            
        glims_boolean = TK.BooleanVar()
        check_glims = TK.Checkbutton(populate_frame, text="GLIMS ID's", variable = glims_boolean, onvalue = True, offvalue = False)
        check_glims.grid (row =1, padx = 12, sticky = TK.W)
        glims_boolean.set(VAR.read_variable("GLIMSIDS"))
        
        rgi_boolean = TK.BooleanVar()
        check_rgi = TK.Checkbutton(populate_frame, state = TK.DISABLED, text="RGI ID's", variable = rgi_boolean, onvalue = True, offvalue = False)
        check_rgi.grid (row =2, padx = 12, pady = (0,26), sticky = TK.W)
        rgi_boolean.set(VAR.read_variable("RGIIDS"))



        parameters_frame = TK.Frame (options_frame, relief = TK.RIDGE, bd = 1)
        parameters_frame.grid (row =0, column =2, padx = (3,20), pady = (6,3), sticky = TK.W)
        
        label_parameters = TK.Label(parameters_frame, text='Scaling')
        label_parameters.grid (row =0, padx = 12, pady = (3,0))
        
        scaling_string = TK.StringVar()
        option_scaling = TK.OptionMenu(parameters_frame, scaling_string, "1", "10", "100", "1000", "10000", "100000", "1000000")
        option_scaling['width'] = 7
        option_scaling['relief'] = TK.FLAT
        option_scaling.grid (row = 1)
        scaling_string.set(VAR.read_variable("SCALING"))



        settings_frame = TK.Frame (options_frame, relief = TK.RIDGE, bd = 1)
        settings_frame.grid (row =1, column =0, columnspan = 3, padx = 20, pady = (3,6))
        
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
        
        
        
        def __callback_reset_default ():
            VAR.reset_defaults()
            InputString.set(VAR.read_variable("INPUT"))
            DEMString.set(VAR.read_variable("DEM"))
            OutputString.set(VAR.read_variable("OUTPUT"))
            hypsometry_boolean.set(VAR.read_variable("HYPSOMETRY"))
            slope_boolean.set(VAR.read_variable("SLOPE"))
            aspect_boolean.set(VAR.read_variable("ASPECT"))
            glims_boolean.set(VAR.read_variable("GLIMSIDS"))
            rgi_boolean.set(VAR.read_variable("RGIIDS"))
            scaling_string.set(VAR.read_variable("SCALING"))
            min_string.set(VAR.read_variable("MINBIN"))
            max_string.set(VAR.read_variable("MAXBIN"))
            size_string.set(VAR.read_variable("BINSIZE"))
            
        defaultButton = TK.Button(settings_frame, text = "Default", height = 1, width = 6, command=__callback_reset_default)
        defaultButton.pack(side=TK.LEFT, padx = (6,12), pady = (6,6))
        
        
        #______________________________________________________________________
        #*******Menu Bar*******************************************************
        arcpyModule = 'NOT FOUND'

        try:
            import arcpy #@UnresolvedImport @UnusedImport
            arcpyModule = 'AVAILABLE'
        except: pass

        foundFrame = TK.Frame(master)
        foundFrame.grid(row=4, column=0, columnspan = 3, pady = 6)

        arcpyLabel = TK.Label (foundFrame, text= "Arcpy Module - ")
        arcpyLabel.pack(side=TK.LEFT, padx = (6,0))

        arcpyLabelResult = TK.Label (foundFrame, text= arcpyModule, fg = "#008000")
        if arcpyModule == 'NOT FOUND':
            arcpyLabelResult.configure(fg = "#ff0000")
        arcpyLabelResult.pack(side=TK.LEFT, padx = (0,12))
        
        #______________________________________________________________________
        #*******Menu Bar*******************************************************
        buttonFrame = TK.Frame(master)
        buttonFrame.grid(row=5, column=0, columnspan = 3, pady = 6)

        #Help Button
        helpButton = TK.Button(buttonFrame, text = "Help", height = 1,
         width = 12, command=__callback_Help)
        helpButton.pack(side=TK.LEFT, padx = (6,12))

        #Exit Program Button
        exitButton = TK.Button(buttonFrame, text = "Exit", height = 1,
         width = 12, command=__callback_Exit)
        exitButton.pack(side=TK.LEFT, padx = (6,12))

        #Run Program Button
        def callback_runImport ():
            import post_processing                                  #@UnresolvedImport
            if InputString.get() <> 'Required' and OutputString.get() <> 'Required' and DEMString.get() <> 'Required':
                master.destroy()
                try: self.root.destroy()
                except: pass
            
                VAR.set_variable("INPUT", "STRING", InputString.get())
                VAR.set_variable("DEM", "STRING", DEMString.get())
                VAR.set_variable("OUTPUT", "STRING", OutputString.get())
                VAR.set_variable("HYPSOMETRY", "BOOLEAN", hypsometry_boolean.get())
                VAR.set_variable("SLOPE", "BOOLEAN", slope_boolean.get())
                VAR.set_variable("ASPECT", "BOOLEAN", aspect_boolean.get())
                VAR.set_variable("GLIMSIDS", "BOOLEAN", glims_boolean.get())
                VAR.set_variable("RGIIDS", "BOOLEAN", rgi_boolean.get())
                VAR.set_variable("SCALING", "INTEGER", scaling_string.get())
                VAR.set_variable("MINBIN", "INTEGER", min_string.get())
                VAR.set_variable("MAXBIN", "INTEGER", max_string.get())
                VAR.set_variable("BINSIZE", "INTEGER", size_string.get())
                
                try:
                    output = OutputPath.get() + '\\Post_Processed'
                    os.makedirs(output)
                except: 
                    import tkMessageBox
                    tkMessageBox.showwarning ('Warning', 'Output Folder can not be written. It may already exist.')
                    sys.exit()
                    
                post_processing.process(InputString.get(), output, DEMString.get(), VAR)
            else:
                import tkMessageBox
                tkMessageBox.showwarning ('Warning', 'You must select Input and Output files.')
                
        run = TK.Button(buttonFrame, text = "Run", height = 1, width = 12, command= callback_runImport)
        if arcpyModule == 'NOT FOUND':
            run.configure (state=TK.DISABLED) #Disable if modules not available
        run.pack(side=TK.LEFT, padx = 6)
        
    #______________________________________________________________________
    #*******Menu Bar*******************************************************
    def getDirectory (self, string):
        """Method: Get directory
        Purpose - An extension of the tkFileDialog module to be used internally."""
        import tkFileDialog
        vDirectory = tkFileDialog.askdirectory(title='Please select a directory')
        if len(vDirectory) > 0:
            string.set (vDirectory)
            return vDirectory

    def getFile (self, string):
        """Method: Get file
        Purpose - An extension of the tkFileDialog module to be used internally."""
        import tkFileDialog
        vFile = tkFileDialog.askopenfilename (title='Please select a file', filetypes = [('Shapefile','*.shp'), ('Tiff', '*.tif'), ('Image', '*.img')])
        if len(vFile) > 0:
            string.set (vFile)
            return vFile

#DRIVER
def driver():
    main = TK.Tk()
    main.title ('Post Process - v.2.0')
    GUI (main)
    main.mainloop()

if __name__ == '__main__':
    driver()