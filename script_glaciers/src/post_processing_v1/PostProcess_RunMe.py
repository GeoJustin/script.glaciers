"""-----------------------------------------------------------------------------
 Name:        GINA_RunMe
 Purpose:     GUI for the 'Process for GINA' program.

 Author:      glaciologist

 Created:     26/08/2011
 Copyright:   (c) glaciologist 2011

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
-----------------------------------------------------------------------------"""

#!/usr/bin/env python
#Add the current directory to python search path.
import sys, os
sys.path.append (os.path.dirname(os.path.abspath(__file__)) + '\\Modules')

import Tkinter

class GUI ():

    def __init__ (self, master):

        TK = Tkinter #Just to shorten the name.

#_______________________________________________________________________________
#*******Menu Bar****************************************************************
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

#_______________________________________________________________________________
#*******Input Dialog************************************************************
        InputFrame = TK.Frame (master)
        InputFrame.grid (row =0, column =0, columnspan = 1, pady = 6)

        #Select Input Frame-----------------------------------------------------
        InputPath = TK.Label (InputFrame, text='Select Glaciers')
        InputPath.grid(row=0, column = 0, sticky = TK.W, padx = 6)

        def callback_SelectedIn ():
            self.getFile (InputString)
        InputString = TK.StringVar()
        InputEntry = TK.Entry (InputFrame, textvariable = InputString, width = 50)
        InputEntry.grid(row=0, column = 1, padx = 6)

        inputFile = TK.Button(InputFrame, text = 'Select', height = 1, width = 8,
         command = callback_SelectedIn)
        inputFile.grid(row=0, column = 2, padx = (0,6), pady = (0,6))

        #Select Output Frame---------------------------------------------------
        OutputPath = TK.Label (InputFrame, text='Select Output')
        OutputPath.grid(row=1, column = 0, sticky = TK.W, padx = 6, pady = (6,6))

        def callback_SelectedOut ():
            self.getDirectory (OutputString)
        OutputString = TK.StringVar()
        OutputEntry = TK.Entry (InputFrame, textvariable = OutputString, width = 50)
        OutputEntry.grid(row=1, column = 1, padx = 6, pady = (6,6))

        OutputFile = TK.Button(InputFrame, text = 'Select', height = 1, width = 8,
         command = callback_SelectedOut)
        OutputFile.grid(row=1, column = 2, padx = (0,6), pady = (0,6))

        #Select DEM Frame------------------------------------------------------
        DEMPath = TK.Label (InputFrame, text='Select DEM')
        DEMPath.grid(row=2, column = 0, sticky = TK.W, padx = 6, pady = (6,6))

        def callback_Selected ():
            self.getFile (DEMString)
        DEMString = TK.StringVar()
        DEMEntry = TK.Entry (InputFrame, textvariable = DEMString, width = 50, state = TK.DISABLED)
        DEMEntry.grid(row=2, column = 1, padx = 6, pady = (6,6))

        DEMFile = TK.Button(InputFrame, text = 'Select', height = 1, width = 8, command = callback_Selected, state = TK.DISABLED)
        DEMFile.grid(row=2, column = 2, padx = (0,6), pady = (0,6))


        #Pre-populate fields.--------------------------------------------------
        InputString.set('Required')
        DEMString.set('Required (not required for GLIMS)')
        OutputString.set('Required')

#_______________________________________________________________________________
#********Check Box Options******************************************************
        checkFrame = TK.Frame(master)
        checkFrame.grid(row=3, column=0, columnspan = 3, pady = 6)

        checkGLIMS = TK.IntVar ()
        checkGINA = TK.IntVar ()
        checkStats = TK.IntVar ()

        #Statistics are specific to weather or not GINA is created
        def __callbackGINA ():
            if checkGINA.get() == 1: #GINA is selected.
                checkBoxStats.configure (state=TK.NORMAL)
            if checkGINA.get() == 0: #GINA is not selected.
                checkBoxStats.configure (state=TK.DISABLED)
                checkBoxStats.deselect()
                DEMEntry.configure (state=TK.DISABLED)
                DEMFile.configure (state=TK.DISABLED)

        def __callbackDEM ():
            if checkStats.get() == 1 == 1: #GINA is selected.
                DEMEntry.configure (state=TK.NORMAL)
                DEMFile.configure (state=TK.NORMAL)
            if checkStats.get() == 0: #GINA is not selected.
                DEMEntry.configure (state=TK.DISABLED)
                DEMFile.configure (state=TK.DISABLED)

        checkBoxGLIMS = TK.Checkbutton(checkFrame, text = "GLIMS", variable = checkGLIMS, onvalue = 1, offvalue = 0)
        checkBoxGLIMS.pack(side=TK.LEFT, padx = (6,12))

        checkBoxGINA = TK.Checkbutton(checkFrame, text = "GINA", variable = checkGINA, onvalue = 1, offvalue = 0, command=__callbackGINA)
        checkBoxGINA.pack(side=TK.LEFT, padx = (6,12))

        checkBoxStats = TK.Checkbutton(checkFrame, text = "Stats (CSV)", variable = checkStats, onvalue = 1, offvalue = 0, state = TK.DISABLED, command=__callbackDEM)
        checkBoxStats.pack(side=TK.LEFT, padx = (6,12))

#_______________________________________________________________________________
#*******Modules Available Input Frame*******************************************
        arcpyModule = 'NOT FOUND'
        numpyModule = 'NOT FOUND'

        try:
            import arcpy #@UnusedImport @UnresolvedImport
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

#_______________________________________________________________________________
#*******Button Frame************************************************************
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
            import modules.Process
            if InputString.get() <> 'Required' and OutputString.get() <> 'Required':
                master.destroy()
                try: self.root.destroy()
                except: pass
                project = os.path.dirname(os.path.abspath(__file__)) + '\\projection\\NAD_1983_Alaska_Albers.prj'
                workspace = os.path.dirname(os.path.abspath(__file__)) + '\\Workspace'

                modules.Process.process (InputString.get(), OutputString.get(), DEMString.get(), project, workspace, checkGLIMS.get(), checkGINA.get(), checkStats.get())
            else:
                import tkMessageBox
                tkMessageBox.showwarning ('Warning', 'You must select Input and Output files.')
        run = TK.Button(buttonFrame, text = "Run", height = 1, width = 12, command= callback_runImport)

        if numpyModule == 'NOT FOUND' or arcpyModule == 'NOT FOUND':
            run.configure (state=TK.DISABLED) #Disable if modules not available
        run.pack(side=TK.LEFT, padx = 6)


#_______________________________________________________________________________
#***FUNCTIONS*******************************************************************
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
    main = Tkinter.Tk()
    main.title ('Post Process - v.1.0')
    GUI (main)
    main.mainloop()

if __name__ == '__main__':
    driver()
