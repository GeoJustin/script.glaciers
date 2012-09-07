"""*****************************************************************************
 Name: Stop Watch
 Purpose: Prints a message to the console or ArcGIS processing window

 Author:      Justin Rich (justin.rich@gi.alaska.edu)
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
*****************************************************************************"""
import time

class StopWatch ():
    """StopWatch extends the time module and is used for basic time keeping and
    is largely used to reduce the amount of input needed to run time commands 
    in other modules. Stop Watch also keeps track of initial start time in order
    to calculate elapsed times."""

    __cpuTime= float(0)
    __startTime= ''

    def __init__(self):
        """init initializes the clock marking a start time and setting it to a 
        global variable to be called back later."""
        
        global __cpuTime
        __cpuTime = time.clock()
        
        global __startTime
        __startTime = time.strftime('%I:%M:%S:%p:')

#_______________________________________________________________________________
#***Methods*********************************************************************
    def reset_start_time (self):
        """Zeros out the clock and starts the timer over again at zero ."""
        global __cpuTime, __startTime
        __cpuTime = time.clock()
        __startTime = time.strftime('%I:%M:%S:%p:')

    def get_start_time (self):
        """Returns the current time in a readable format. This method is
         currently under construction"""
        return __startTime

    def get_elapsed_time (self):
        """Returns the elapsed time since the module was originally call
        or from the time it was last reset using 'resetStartTime'."""
        t = time.strftime ('%H:%M:%S', time.gmtime(time.clock() - __cpuTime))
        return t

    def pause (self, seconds):
        """Causes application to sleep for the number of seconds passed through."""
        time.sleep(seconds)

    def get_day (self):
        """Returns the day of the week as a number."""
        day = time.strftime('%d')
        return day
    
    def get_month_number (self):
        """Returns the month as a number."""
        month = time.strftime('%m')
        return month
    
    def get_month_name (self):
        """Returns the current month name."""
        monthName = time.strftime('%B')
        return monthName
    
    def get_time (self):
        """Returns the current time using a 12-hour clock and displays hours,
        minutes, seconds and AM/PM notation."""
        localtime = time.strftime('%I:%M:%S:%p:')
        return localtime

    def get_year (self):
        """Returns the current year."""
        year = time.strftime('%Y')
        return year
    
# Driver
def main ():
    StopWatch()
if __name__ == '__main__':
    main()
