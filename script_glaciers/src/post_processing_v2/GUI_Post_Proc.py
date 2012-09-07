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
import variables as VAR                                     #@UnresolvedImport

class GUI ():
    """Graphical User Interface (GUI) for Post Process application."""

    def __init__ (self, master):
        """Setup the main GUI window and load default or starting settings."""
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
        InputString.set('Required')

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
        DEMString.set('Required')

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
        OutputString.set('Required')

        OutputFile = TK.Button(InputFrame, text = 'Select', height = 1, width = 8,
         command = callback_SelectedOut)
        OutputFile.grid(row=2, column = 2, padx = (0,6), pady = (0,6))
        
        #______________________________________________________________________
        #*******Settings*******************************************************
        options_frame = TK.LabelFrame(master, text= 'Parameters')
        options_frame.grid (row =3, column =0, columnspan = 2, padx =6, pady = 6)
        
        settings_frame = TK.Frame (options_frame, relief = TK.RIDGE, bd = 1)
        settings_frame.grid (row =2, column =0, columnspan = 2, padx = 20, pady = (6,6))
        
        label_minbin = TK.Label(settings_frame, text='Min. Bin')
        label_minbin.pack(side=TK.LEFT)
        
        min_string = TK.StringVar()
        min_entry = TK.Entry (settings_frame, textvariable = min_string, width = 6, justify = TK.CENTER)
        min_entry.pack(side=TK.LEFT, padx = (12,12), pady = (6,6))
        min_string.set(VAR.Variables().read_variable("MINBIN"))
        
        label_maxbin = TK.Label(settings_frame, text='Max. Bin')
        label_maxbin.pack(side=TK.LEFT)
        
        max_string = TK.StringVar()
        max_entry = TK.Entry (settings_frame, textvariable = max_string, width = 6, justify = TK.CENTER)
        max_entry.pack(side=TK.LEFT, padx = (3,12), pady = (6,6))
        max_string.set(VAR.Variables().read_variable("MAXBIN"))
        
        label_size = TK.Label(settings_frame, text='Size')
        label_size.pack(side=TK.LEFT)
        
        size_string = TK.StringVar()
        size_entry = TK.Entry (settings_frame, textvariable = size_string, width = 6, justify = TK.CENTER)
        size_entry.pack(side=TK.LEFT, padx = (3,12), pady = (6,6))
        size_string.set(VAR.Variables().read_variable("BINSIZE"))
        
        def __callback_reset_default ():
            VAR.Variables().reset_defaults()
            min_string.set(VAR.Variables().read_variable("MINBIN"))
            max_string.set(VAR.Variables().read_variable("MAXBIN"))
            size_string.set(VAR.Variables().read_variable("BINSIZE"))
            
        helpButton = TK.Button(settings_frame, text = "Default", height = 1, width = 6, command=__callback_reset_default)
        helpButton.pack(side=TK.LEFT, padx = (6,12), pady = (6,6))
        
        
        #______________________________________________________________________
        #*******Menu Bar*******************************************************
        arcpyModule = 'NOT FOUND'
        numpyModule = 'NOT FOUND'

        try:
            import arcpy #@UnresolvedImport @UnusedImport
            arcpyModule = 'AVAILABLE'
        except: pass

        try:
            import numpy #@UnusedImport
            numpyModule = 'AVAILABLE'
        except: pass

        foundFrame = TK.Frame(master)
        foundFrame.grid(row=4, column=0, columnspan = 3, pady = 6)

        arcpyLabel = TK.Label (foundFrame, text= "Arcpy Module - ")
        arcpyLabel.pack(side=TK.LEFT, padx = (6,0))

        arcpyLabelResult = TK.Label (foundFrame, text= arcpyModule, fg = "#008000")
        if arcpyModule == 'NOT FOUND':
            arcpyLabelResult.configure(fg = "#ff0000")
        arcpyLabelResult.pack(side=TK.LEFT, padx = (0,12))

        numpyLabel = TK.Label (foundFrame, text="Numpy Module - ")
        numpyLabel.pack(side=TK.LEFT, padx = (6,0))

        numpyLabelResult = TK.Label (foundFrame, text=numpyModule, fg = "#008000")
        if numpyModule == 'NOT FOUND':
            numpyLabelResult.configure(fg = "#ff0000")
        numpyLabelResult.pack(side=TK.LEFT, padx = (0,12))
        
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
                
                VAR.Variables().set_variable("MINBIN", min_string.get())
                VAR.Variables().set_variable("MAXBIN", max_string.get())
                VAR.Variables().set_variable("BINSIZE", size_string.get())
                workspace = os.path.dirname(os.path.abspath(__file__)) + '\\workspace'
                post_processing.process (InputString.get(), OutputString.get(), DEMString.get(), workspace, size_string.get(), min_string.get(), max_string.get())
            else:
                import tkMessageBox
                tkMessageBox.showwarning ('Warning', 'You must select Input and Output files.')
                
        run = TK.Button(buttonFrame, text = "Run", height = 1, width = 12, command= callback_runImport)
        if numpyModule == 'NOT FOUND' or arcpyModule == 'NOT FOUND':
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