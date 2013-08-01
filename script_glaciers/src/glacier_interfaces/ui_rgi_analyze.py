"""****************************************************************************
 Name:         glacier_interfaces.ui_rgi_analyze
 Purpose:     
 
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
 that careful attention be paid to the contents of the meta data / help file
 associated with these data to evaluate application limitations, restrictions
 or intended use. The creators and distributors of the application shall not
 be held liable for improper or incorrect use of the utility described and/
 or contained herein.
****************************************************************************"""
import sys, os
sys.path.append (os.path.dirname(os.path.dirname(__file__)))

import Tkinter as TK
import tkMessageBox
import glacier_utilities.general_utilities.variables as variables
import glacier_utilities.functions.ui_setup as setup


class Analyze_RGI (object):
    """classdocs: Creates a graphic user interface for analyzing  
    RGI formated glacier outlines. The tool takes in a folder contianing
    X number of shapefiles and runs them all. All outlines need to be in
    RGI format before then can be analyzed."""

    def __init__(self, master):
        """Constructor:  Takes in a main tkinter window and creates a
         user interface"""
         
        VAR = variables.Variables() # Start the variables reader
        
        self.get_menubar(master, master) # Setup menu bar items
        
        # Setup file / folder input output dialog boxes
        input_string, output_string, ver_string = self.get_io (master, master, VAR)
        self.__input_string = input_string
        self.__output_string = output_string
        self.__rgi_version = ver_string

        # Setup Module checks
        arcpy_found = setup.check_arcpy(master, 4, 0, 3, 0, 6)
        
        # Setup command buttons
        run_button = self.get_buttons (master, master, VAR)
        
        # Disable run button if critical modules are not found
        if arcpy_found == False:
            run_button.configure (state=TK.DISABLED) #Disable if modules not available
            
            
    def get_io (self, master, frame, VAR):
        """Function: File IO
        Generates input file selection menu items (label, text input box and file/
        folder selection dialog)."""
        input_frame = TK.Frame (frame)
        input_frame.grid (row =0, column =0, columnspan = 1, pady = 6)

        #Select Input Frame
        input_label = TK.Label (input_frame, text='Input Folder')
        input_label.grid(row=0, column = 0, sticky = TK.W, padx = 6)

        # Callback to get new input file and rebuild options based on it
        def __callback_select_input ():
            setup.get_directory (input_string, VAR.read_variable("INPUT_FOLDER"))
            self.__input_string = input_string # Set new input file
        input_string = TK.StringVar()
        input_entry = TK.Entry (input_frame, textvariable = input_string, width = 50)
        input_entry.grid(row=0, column = 1, padx = 6)
        input_string.set(VAR.read_variable("INPUT_FOLDER"))

        input_file = TK.Button(input_frame, text = 'Select', height = 1, width = 8, command = __callback_select_input)
        input_file.grid(row=0, column = 2, padx = (0,6), pady = (0,6))
        
        #Select Input Frame
        output_label = TK.Label (input_frame, text='Output Folder')
        output_label.grid(row=1, column = 0, sticky = TK.W, padx = 6)

        # Callback to get new input file and rebuild options based on it
        def __callback_select_output ():
            setup.get_directory (output_string, VAR.read_variable("OUTPUT_FOLDER"))
            self.__output_string = output_string # Set new input file
        output_string = TK.StringVar()
        output_entry = TK.Entry (input_frame, textvariable = output_string, width = 50)
        output_entry.grid(row=1, column = 1, padx = 6)
        output_string.set(VAR.read_variable("OUTPUT_FOLDER"))

        output_file = TK.Button(input_frame, text = 'Select', height = 1, width = 8, command = __callback_select_output)
        output_file.grid(row=1, column = 2, padx = (0,6), pady = (0,6))
        
        rgi_frame = TK.Frame (input_frame)
        rgi_frame.grid (row =2, column = 1)
                   
        label_version = TK.Label(rgi_frame, text='RGI Version ')
        label_version.grid (row =0, column=0, padx = (10,0), sticky = TK.W)
        
        ver_string = TK.StringVar()
        ver_entry = TK.Entry (rgi_frame, textvariable = ver_string, width = 6, justify = TK.CENTER)
        ver_entry.grid (row =0, column=1, padx = (0,10), sticky = TK.W)
        ver_string.set(VAR.read_variable("RGIVERSION"))
        
        return input_string, output_string, ver_string
            
            
    def get_buttons (self, master, frame, VAR):
        """Function: Get Buttons
        Sets up control buttons for the application (help, exit and run). The run
        button, in this case, writes the input variables to the varaible file (.var)
        for use by the application at runtime and saves selections for future use."""
        
        buttonFrame = TK.Frame(frame)
        buttonFrame.grid(row=5, column=0, columnspan = 3, pady = 6)

        #Help button (calls get help function)
        def __callback_help(): 
            setup.get_help()
        helpButton = TK.Button(buttonFrame, text = "Help", height = 1,
         width = 12, command=__callback_help)
        helpButton.pack(side=TK.LEFT, padx = (6,12))

        #Exit application button (calls exit function)
        def __callback_exit(): 
            setup.exit_application(master)
        exitButton = TK.Button(buttonFrame, text = "Exit", height = 1,
         width = 12, command= __callback_exit)
        exitButton.pack(side=TK.LEFT, padx = (6,12))

        #Run Program Button
        def __callback_run_analysis ():
            if self.__input_string.get() <> 'Required' and self.__output_string.get() <> 'REQUIRED':
            
                # Write variables to .var file
                VAR.set_variable("INPUT_FOLDER", "STRING", self.__input_string.get())
                VAR.set_variable("OUTPUT_FOLDER", "STRING", self.__output_string.get())
                VAR.set_variable("RGIVERSION", "STRING", self.__rgi_version.get())
                
                # Remove GUI window and destroy it.
                try: master.destroy()
                except: pass
                try: self.root.destroy()
                except: pass
                
                # RUN APPLICATION
                try: # Import needs to be here in case ARCPY not found. Crashes on import if not
                    print 'STARTING RGI ANALYSIS'
                    import glacier_scripts.rgi_analyze as ANALYZE  
                    ANALYZE.rgi_analysis(VAR)
                    print 'FINISHED RGI ANALYSIS'
                except:
                    tkMessageBox.showwarning ('Warning', 'Could NOT Analyze Folder. Check folder paths.')
            else: 
                tkMessageBox.showwarning ('Warning', 'You must select Input and Output Folders.')
                
        run_button = TK.Button(buttonFrame, text = "Run", height = 1, width = 12, command= __callback_run_analysis)
        run_button.pack(side=TK.LEFT, padx = 6)
        
        return run_button # Return the run button to be accessed by disable
      
           
            
    def get_menubar (self, master, frame):
        """Function: Menu Bar
        Menu bar bar along the top of the window."""
        menubar = TK.Menu(frame)

        def __callback_exit():
            setup.exit_application(master)
        filemenu = TK.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=__callback_exit)
        menubar.add_cascade(label="File", menu=filemenu)

        def __callback_help():
            setup.get_help()
        helpmenu = TK.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Files", command=__callback_help)
        menubar.add_cascade(label="Help", menu=helpmenu)

        frame.config(menu=menubar)

        
#DRIVER

def driver():
    main = TK.Tk()
    main.title ('Analyze RGI - v.1.0')
    Analyze_RGI (main)
    main.mainloop()

if __name__ == '__main__':
    driver()