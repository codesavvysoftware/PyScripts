#/////////////////////////////////////////////////////////////////////////////
#/// @file ApexInternalSafeRamDiagnosticFaultInjectionTest1.py
#///
#/// This Python script verifies that when there is inconsistency between
#/// regular and prime value in SafeRAM, i.e. prime value is not bit-reverse
#/// of regular one, Apex RAM diagnostics (ApexDiagSafeRam.cpp) will raise exception.
#/// Code injection relies on inserting prime value being bit-reverse of actual
#/// prime value. The injection is inserted after 30 seconds from powerup
#/// and Safe-RAM test execution period is set to 70 seconds.
#///
#/// @if REVISION_HISTORY_INCLUDED
#/// @par Edit History
#/// pgrzywn 30-SEP-2013 Created.
#/// pszramo 21-OCT-2013 Modified to match updated faultInjectionUtils.
#/// mstasia 07-NOV-2013 Description modified.
#/// pszramo 17-DEC-2013 Adjustments after MISRA fixes.
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
    'ApexDiagSafeRam.cpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 1
    // End Fault Injection Point 1
    // Fault Injection Code Start
    if (InjectFaultFlag == 1)
    {
        DgnSafeRam.intDataramSizePrime = !DgnSafeRam.intDataramSizePrime;
    }
    // Fault Injection Code End
    ''',
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 2
    // End Fault Injection Point 2
    // Fault Injection Code Start
    InjectFaultFlag = 0;
    // Fault Injection Code End
    '''
    ],
    'ApexDiagnostic.hpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 1
    // End Fault Injection Point 1
// Fault Injection Code Start
extern UINT32 InjectFaultFlag;
// Fault Injection Code End
    ''',
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 2
    // End Fault Injection Point 2
    // Fault Injection Code Start
    static const UINT32 DGN_FI_DELAY_SEC = 30;
    // Fault Injection Code End
    '''
    ],
    'ApexDiagnostic.cpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 1
    // End Fault Injection Point 1
// Fault Injection Code Start
UINT32 InjectFaultFlag = 0;
// Fault Injection Code End
    ''',
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 2
    // End Fault Injection Point 2
    // Fault Injection Code Start
    if (HI_ApexReg.SystemTime > (DGN_FI_DELAY_SEC * MILLISECONDS_IN_SECOND * MICROSECONDS_IN_MILLISECOND))
    {
        InjectFaultFlag = 1;
    }
    // Fault Injection Code End
    ''',
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 4
    // End Fault Injection Point 4
    // Fault Injection Code Start
    DgnList[DGN_SAFE_RAM_NUM].stepValueTimeslice = MsToDgnSlices(DGN_FI_SEVENTY_SEC_MS);
    // Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)