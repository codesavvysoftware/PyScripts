#/////////////////////////////////////////////////////////////////////////////
#/// @file If8iAdcCrcDiagnosticFaultInjectionTest1.py
#///
#/// This Python script verifies that a bad CRC written to the ADC will cause
#/// that channel to fault.
#/// Verify that the "Fault" and "Uncertain" status bits are set in the
#/// appropriate input tag.
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
    'IF8I.c': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    '''
      /* Start Fault Injection Point 2 */
      /* End Fault Injection Point 2 */
      /* Fault Injection Code Start */
      /* For each even channel number, corrupt it's CRC value by incrementing it */
      /* Verify that these channels have their "Fault" and "Uncertain" status bits set. */
      if ( (i & 1) == 0 )
      {
         write_crc[ i ]++;
      }
      /* Fault Injection Code End */
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)