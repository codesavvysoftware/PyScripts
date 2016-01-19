#/////////////////////////////////////////////////////////////////////////////
#/// @file ApexInternalRamEccCircuitDiagnosticFaultInjectionTest1.py
#///
#/// This Python script verifies that Apex ECC circuit test diagnostic
#/// is faulting if seeded double-bit ECC error has not been detected.
#/// The injected code modifies sramEccError variable at start-up to clear
#/// indication of error detection. This way the script simulates that
#/// a seeded double-bit error is not detected.
#///
#/// @if REVISION_HISTORY_INCLUDED
#/// @par Edit History
#/// pgrzywn 30-SEP-2013 Created.
#/// spolke  03-OCT-2013 Comment updated.
#/// pszramo 21-OCT-2013 Modified to match updated faultInjectionUtils.
#/// pszramo 08-NOV-2013 Updated description.
#/// pszramo 06-DEC-2013 Adjustments after MISRA fixes.
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
    'ApexDiagEcc.cpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 1
    // End Fault Injection Point 1
    // Fault Injection Code Start
    if (!testData->singleBitError)
    {
        sramEccError &= ~HI_BIT_SRAMECC_PER;
    }
    // Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)