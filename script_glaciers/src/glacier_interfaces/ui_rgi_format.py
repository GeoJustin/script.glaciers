"""****************************************************************************
 Name:         format_rgi.format_rgi_ui
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
import sys, os
sys.path.append (os.path.dirname(os.path.dirname(__file__)))

import Tkinter as TK
import tkMessageBox
import glacier_utilities.general_utilities.variables as variables
import glacier_utilities.functions.ui_setup as setup

class format_RGI_GUI (object):
    """classdocs: Creates a graphich user interface for setting up inputs to
    the format rgi class. This includes input file, output file and field
    mappings."""

    def __init__(self, master):
        """Constructor:  Takes in a main tkinter window and creates a
         user interface"""
    
        self.__original_fields = [] 
    
        VAR = variables.Variables() # Start the variables reader
            
        self.get_menubar(master, master) # Setup menu bar items
        
        # Setup file / folder input output dialog boxes
        input_string, output_string = self.get_io (master, master, VAR)
        self.__input_string = input_string
        self.__output_string = output_string
                    
                    
        options_frame, mapping_list = self.get_mapping (master, VAR)
        self.__options_frame = options_frame
        self.__mapping_list = mapping_list
    
        # Setup Module checks
        arcpy_found = setup.check_arcpy(master, 4, 0, 3, 0, 6)
        
        # Setup command buttons
        run_button = self.get_buttons (master, master, VAR)
        
        # Disable run button if critical modules are not found
        if arcpy_found == False:
            run_button.configure (state=TK.DISABLED) #Disable if modules not available
        
        # Build options list for the first time. This is here since it can 
        # not be built until both the input and options frames are in place
        self.set_option_list (master, VAR)

    
    
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
        def __callback_runImport ():
            if self.__input_string.get() <> 'Required' and self.__output_string.get() <> 'Required':
            
                # Write variables to .var file
                VAR.set_variable("INPUT_FILE", "STRING", self.__input_string.get())
                VAR.set_variable("OUTPUT_FILE", "STRING", self.__output_string.get())
                
                # Put together mapping dictionary
                mapping_dict = {}
                for item in self.__mapping_list:
                    if item[1].get() <> '':
                        mapping_dict [item[0]] = item[1].get()
                
                # Remove GUI window and destroy it.
                try: master.destroy()
                except: pass
                try: self.root.destroy()
                except: pass
                
                # RUN APPLICATION
                # Import needs to be here in case ARCPY not found. Crashes on import if not
                import glacier_scripts.rgi_format as rgi_format                                              #@UnresolvedImport
                rgi_format.FormatRGI(self.__input_string.get(), self.__output_string.get(), mapping_dict, VAR)
                
            else: 
                tkMessageBox.showwarning ('Warning', 'You must select Input and Output files.')
                
        run_button = TK.Button(buttonFrame, text = "Run", height = 1, width = 12, command= __callback_runImport)
        run_button.pack(side=TK.LEFT, padx = 6)
        
        return run_button # Return the run button to be accessed by disable
   
    
    def get_io (self, master, frame, VAR):
        """Function: File IO
        Generates input file selection menu items (label, text input box and file/
        folder selection dialog)."""
        input_frame = TK.Frame (frame)
        input_frame.grid (row =0, column =0, columnspan = 1, pady = 6)

        #Select Input Frame
        input_label = TK.Label (input_frame, text='Glaciers')
        input_label.grid(row=0, column = 0, sticky = TK.W, padx = 6)

        # Callback to get new input file and rebuild options based on it
        def __callback_select_input ():
            setup.get_file (input_string, VAR.read_variable("INPUT_FILE"), [('Shapefile','*.shp')])
            self.__input_string = input_string # Set new input file
            self.set_option_list (master, VAR) # Create New option window with new inputs
        input_string = TK.StringVar()
        input_entry = TK.Entry (input_frame, textvariable = input_string, width = 50)
        input_entry.grid(row=0, column = 1, padx = 6)
        input_string.set(VAR.read_variable("INPUT_FILE"))

        input_file = TK.Button(input_frame, text = 'Select', height = 1, width = 8, command = __callback_select_input)
        input_file.grid(row=0, column = 2, padx = (0,6), pady = (0,6))

        #Select Output Frame
        output_label = TK.Label (input_frame, text='Save As')
        output_label.grid(row=1, column = 0, sticky = TK.W, padx = 6, pady = (6,6))

        def __callback_output ():
            setup.get_save(output_string, VAR.read_variable("OUTPUT_FILE"), [('Shapefile','*.shp')], '.shp',)
        output_string = TK.StringVar()
        output_entry = TK.Entry (input_frame, textvariable = output_string, width = 50)
        output_entry.grid(row=1, column = 1, padx = 6, pady = (6,6))
        output_string.set(VAR.read_variable("OUTPUT_FILE"))

        output_file = TK.Button(input_frame, text = 'Select', height = 1, width = 8, command = __callback_output)
        output_file.grid(row=1, column = 2, padx = (0,6), pady = (0,6))
        
        return input_string, output_string
    
    
    def get_mapping (self, frame, VAR):
        """Function: Get Mapping
        Generates user selection interface for choosing mapping options."""
        mapping = [] # List of drop down boxes.
        
        #Settings Frame
        options_frame = TK.LabelFrame(frame, text= 'Field Mapping')
        options_frame.grid (row =3, column =0, columnspan = 3, padx =6, pady = 6)
        
        option_list = tuple(['']) # a tuple containing ''
        # Add a tuple for each of the field names from the input file
        option_list += tuple([item.encode() for item in self.__original_fields])
        
        pos_row = 0 # Track current row to position the option menu and label
        pos_col = 0 # Track current col to position the option menu and label
        rgi_columns = VAR.read_variable("RGI_SPEC") # Get RGI column headers
        for heading in rgi_columns: # For each header
            
            # Create Label for RGI Column
            output_label = TK.Label (options_frame, text= heading[0])
            output_label.grid(row= pos_row, column = pos_col, padx = (0,12), sticky = TK.W)
            
            # Create Option menu populated with input table fields
            map_string = TK.StringVar()
            map_entry = TK.OptionMenu (options_frame, map_string, *option_list)
            map_entry.config(width = 10, relief=TK.SUNKEN, bg= 'white')
            map_string.set(option_list[0])
            map_entry.grid(row= pos_row, column = pos_col + 1, sticky = TK.E)
            
            # Add the RGI Column label and option menu string to a list
            mapping.append([heading[0], map_string])
        
            pos_row += 1 # Incriment current positioning row by one
            if pos_row == 6: # If it is the sixth row
                pos_row = 0  # Reset row position to the top
                pos_col = 2  # Offset the columns by 2
                
        # Return a reference to the option frame and the list of Column names and map_string
        return options_frame, mapping
            
    
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
       
    
    def set_option_list (self, master, VAR):
        """Function: Set Option Lists
        Attempts to read an input shapefile and get a list of optional 
        headers to map"""
        try:
            self.__original_fields = []
            import arcpy as ARCPY                  #@UnresolvedImport
            fields_list = ARCPY.ListFields(self.__input_string.get())
            for field in fields_list: # Loop through the field names
                if not field.required: 
                    # If they are not required append them to the list of field names.
                    self.__original_fields.append(field.name)
        except: 'could not find header list'
        
        self.__options_frame.destroy() # Destroy current option frame
        
        # Rebuild option frame with (attempt to get new input file)
        options_frame, mapping_list = self.get_mapping (master, VAR)
        self.__options_frame = options_frame # Reset Variables
        self.__mapping_list = mapping_list
        
        return True

#DRIVER
def driver():
    main = TK.Tk()
    main.title ('Format RGI - v.1.0')
    format_RGI_GUI (main)
    main.mainloop()

if __name__ == '__main__':
    driver()