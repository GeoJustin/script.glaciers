"""****************************************************************************
 Name:         formate_rgi.formate_rgi
 Purpose:     
 
Created:         Nov 16, 2012
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
from glaciers.formate_output import output_log


class FormateRGI (object):
    """classdocs """

    def __init__(self):
        """Constructor:  """
        print 'Running'
        output_log.Log('A:\Desktop')




def driver ():
    FormateRGI ()
if __name__ == '__main__':
    driver()