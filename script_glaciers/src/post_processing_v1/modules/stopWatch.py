"""*****************************************************************************
 Name: Stop Watch
 Purpose: Prints a message to the console or ArcGIS processing window

 Author:      Justin Rich (justin.rich@gi.alaska.edu)

 Created:     March 8, 2011
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
*****************************************************************************"""
import time

class StopWatch ():
    """StopWatch extends the time module."""

    __cpuTime__= float(0)
    __startTime__= ''

    def __init__(self):
        global __cpuTime__
        __cpuTime__ = time.clock()
        
        global __startTime__
        __startTime__ = time.strftime('%I:%M:%S:%p:')

#_______________________________________________________________________________
#***Methods*********************************************************************
    def resetStartTime (self):
        """Zeros out the clock and starts the timer over again at zero ."""
        global __cpuTime__, __startTime__
        __cpuTime__ = time.clock()
        __startTime__ = time.strftime('%I:%M:%S:%p:')

    def getStartTime (self):
        """Returns the current time in a readable format. This method is
         currently under construction"""
        return __startTime__

    def getElapsedTime (self):
        """Returns the elapsed time since the module was originally call
        or from the time it was last reset using 'resetStartTime'."""
        t = time.strftime ('%H:%M:%S', time.gmtime(time.clock() - __cpuTime__))
        return t

    def pause (self, seconds):
        """Causes application to sleep for the number of seconds passed through."""
        time.sleep(seconds)

    def getCurrentDay (self):
        """Returns the day of the week as a number."""
        day = time.strftime('%d')
        return day
    
    def getCurrentMonth (self):
        """Returns the month as a number."""
        month = time.strftime('%m')
        return month
    
    def getCurrentMonthName (self):
        """Returns the current month name."""
        monthName = time.strftime('%B')
        return monthName
    
    def getCurrentTime (self):
        """Returns the current time using a 12-hour clock and displays hours,
        minutes, seconds and AM/PM notation."""
        localtime = time.strftime('%I:%M:%S:%p:')
        return localtime

    def getCurrentYear (self):
        """Returns the current year."""
        year = time.strftime('%Y')
        return year
