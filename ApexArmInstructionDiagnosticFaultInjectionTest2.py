#/////////////////////////////////////////////////////////////////////////////
#/// @file ApexArmInstructionDiagnosticFaultInjectionTest2.py
#///
#/// This Python script verifies that Apex 16-bit signed multiplication
#/// instructions test (ApexDiagArm.cpp: TestSigned16BitMultiplication())
#/// operates and fails if necessary, i.e. result of smulbb instruction
#/// is incremented and returned for comparison that will result in assert.
#/// Since there is no way to force the instruction to return wrong value,
#/// the value after smulbb is incremented to allow test to fail.
#///
#/// @if REVISION_HISTORY_INCLUDED
#/// @par Edit History
#/// pgrzywn 30-SEP-2013 Created.
#/// mstasia 03-OCT-2013 Description added.
#/// pszramo 21-OCT-2013 Modified to match updated faultInjectionUtils.
#/// fzembok 05-NOV-2013 Fault injection point fixes.
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
    'ApexDiagArmAsm.s': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    ;; Start Fault Injection Point 3
    ;; End Fault Injection Point 3
;; Fault Injection Code Start
    IMPORT  InjectFaultFlag
;; Fault Injection Code End
    ''',
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    ;; Start Fault Injection Point 2
    ;; End Fault Injection Point 2
;; Fault Injection Code Start
        LDR     r2, =InjectFaultFlag
        LDR     r2, [r2]
        CMP     r2, #1
;; Add 1 only if InjectFaultFlag is set
        ADDEQ   r0, r0, #1
;; Fault Injection Code End
    '''
    ],
    'ApexDiagArm.cpp': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    // Start Fault Injection Point 1
    // End Fault Injection Point 1
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
    // Start Fault Injection Point 6
    // End Fault Injection Point 6
    // Fault Injection Code Start
    DgnList[DGN_ARM_NUM].stepValueTimeslice = MsToDgnSlices(DGN_FI_FIVE_SEC_MS);
    // Fault Injection Code End
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)