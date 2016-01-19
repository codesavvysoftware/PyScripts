#/////////////////////////////////////////////////////////////////////////////
#/// @file If8iAdcWriteDiagnosticFaultInjectionTest.py
#///
#/// This Python script verifies that a mismatch between expected data written
#/// to the ADC and the data read back is detected by the DSP.
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
      /* Start Fault Injection Point 1 */
      /* End Fault Injection Point 1 */
      /* Fault Injection Code Start */
      /* Corrupt a bit in the data read back for channels 1, 3, 5 and 7. */
      /* Verify that these channels have their "Fault" and "Uncertain" status bits set. */
      readback[ 1 ] ^= 0x100;
      readback[ 3 ] ^= 0x200;
      readback[ 5 ] ^= 0x400;
      readback[ 7 ] ^= 0x800;
      /* Fault Injection Code End */
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)