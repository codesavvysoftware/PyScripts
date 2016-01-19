#/////////////////////////////////////////////////////////////////////////////
#/// @file ApexCompletionTimeDiagnosticFaultInjectionTest1.py
#///
#/// This Python script verifies that Apex diagnostic completion time test
#/// (ApexDiagnostic.cpp: DgnCompletionTimeCheck(void)) operates and fails
#/// if necessary. Checking procedure relies on comparing each test's
#/// lastcomplete field with current slice number to estimate
#/// conformance with timeout requirement. The injection causes timeout
#/// value to be 0, causing the test to fail immediately.
#///
#/// @if REVISION_HISTORY_INCLUDED
#/// @par Edit History
#/// pgrzywn  30-SEP-2013 Created.
#/// mstasia  03-OCT-2013 Description added.
#/// pszramo  21-OCT-2013 Modified to match updated faultInjectionUtils.
#/// pszramo  04-NOV-2013 Updated fault injection point number for apxDiag.hpp.
#/// pszramo  16-DEC-2013 Adjustments after MISRA fixes.
#/// dtstalte 28-FEB-2014 Add new fault injection point to not falsely trip the
#///                      binary CRC diagnostic at start up.
#/// @endif
#///
#/// @par Copyright (c) 2014 Rockwell Automation Technologies, Inc.  All rights reserved.
#///
#/////////////////////////////////////////////////////////////////////////////

import faultInjectionUtils

#------------------------------------------------------------------------------
# Here is the list of files to be modified by this script, along with
# blocks of new code (first two lines of block are start and end text to
# search for and replace between) for each of the modified files.
fileModificationsDictionary = { \
    'ApexDiagnostic.cpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 5
    // End Fault Injection Point 5
    // Fault Injection Code Start
    DgnList[DGN_EXE_CRC_NUM].timeoutTimeslice = 0;
    // Fault Injection Code End
    '''
    ],
    'ApexDiagnostic.hpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 3
    // End Fault Injection Point 3
    // Fault Injection Code Start
    static const UINT32 DGN_COMPL_CHECK_INTERVAL_TIME_SLICE = (DGN_INTERVALS_PER_SECOND * 50);
    // Fault Injection Code End
    '''
    ],
    'ApexDiagBinaryCrc.cpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 4
    // End Fault Injection Point 4
    // Fault Injection Code Start
    // Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)