"""-----------------------------------------------------------------------------
 Name:        Log
 Purpose:     Creates and maintains a log file.

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

import stopWatch

class log ():

    __logfile__ = ''
    __content__ = ''
    __clock__ = stopWatch.StopWatch

    def __init__ (self, output):
        global __logfile__, __content__, __clock__

        __clock__ = stopWatch.StopWatch()

        __logfile__ = output + '\\Log.txt'
        __content__ = 'Application Log File: ' + '\n'
        __content__ = __content__ +  'Year: ' + str(__clock__.getCurrentYear())
        __content__ = __content__ + ' Month: ' + str(__clock__.getCurrentMonthName())
        __content__ = __content__ + ' Day: ' + str(__clock__.getCurrentDay())
        __content__ = __content__ + ' Started: ' + str(__clock__.getCurrentTime()) + '\n' + '\n'

        log = open (__logfile__, 'w')
        log.write(__content__)
        log.close()


    def printLine (self, text):
        """Prints a line to the log file based on the input text."""
        global __content__
        __content__ = __content__ + str(__clock__.getElapsedTime()) + ' - ' + text + '\n'

        log = open (__logfile__, 'w')
        log.write(__content__)
        log.close()

    def printBreak (self):
        """Prints a line break in the log file."""
        global __content__
        __content__ = __content__ + '\n'

        log = open (__logfile__, 'w')
        log.write(__content__)
        log.close()

def main():
    pass

if __name__ == '__main__':
    main()
