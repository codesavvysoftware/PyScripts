#/////////////////////////////////////////////////////////////////////////////
#/// @file Irt8iAdcCrcDiagnosticFaultInjectionTest2.py
#///
#/// This Python script verifies that a bad CRC read from the ADC will cause
#/// that channel to fault.
#/// Verify that the "Fault" status bit is set in the appropriate input tag.
#///
#/// @if REVISION_HISTORY_INCLUDED
#/// @par Edit History
#/// kolat   18-Jan-2016 Created.
#/// @endif
#///
#/// @par Copyright (c) 2016 Rockwell Automation Technologies, Inc.  All rights reserved.
#///
#/////////////////////////////////////////////////////////////////////////////

import faultInjectionUtils

#------------------------------------------------------------------------------
# Here is the list of files to be modified by this script, along with
# blocks of new code (first two lines of block are start and end text to
# search for and replace between) for each of the modified files.
fileModificationsDictionary = { \
    'IRT8I.c': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    '''
      /* Start Fault Injection Point 3 */
      /* End Fault Injection Point 3 */
      /* Fault Injection Code Start */
      /* For each odd channel number, corrupt it's read CRC value by incrementing it */
      /* Verify that these channels have their "Fault" status bit set. */
      if ( (ADC_bit & 1) == 1 )
      {
         read_crc[ ADC_bit ]++;
      }
      /* Fault Injection Code End */
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)