#/////////////////////////////////////////////////////////////////////////////
#/// @file ApexFirmwareBinaryCrcDiagnosticFaultInjectionTest1.py
#///
#/// This Python script verifies that Apex is correctly checking the firmware
#/// binary. It sets the expected CRC value to an incorrect value by
#/// incrementing it. Then it is verified that Apex faults due to a bad CRC
#/// value.
#///
#/// @if REVISION_HISTORY_INCLUDED
#/// @par Edit History
#/// pgrzywn 30-SEP-2013 Created.
#/// spolke  03-OCT-2013 Comment updated.
#/// pszramo 21-OCT-2013 Modified to match updated faultInjectionUtils.
#/// pszramo 11-DEC-2013 Adjustments after MISRA fixes.
#/// @endif
#///
#/// @par Copyright (c) 2013 Rockwell Automation Technologies, Inc.  All rights reserved.
#///
#/////////////////////////////////////////////////////////////////////////////

import faultInjectionUtils

#------------------------------------------------------------------------------
# Here is the list of files to be modified by this script, along with
# blocks of new code (first two lines of block are start and end text to
# search for and replace between) for each of the modified files.
fileModificationsDictionary = { \
    'ApexDiagBinaryCrc.cpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 1
    // End Fault Injection Point 1
    // Fault Injection Code Start
    m_CrcExpected++;
    // Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)