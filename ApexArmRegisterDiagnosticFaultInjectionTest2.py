#/////////////////////////////////////////////////////////////////////////////
#/// @file ApexArmRegisterDiagnosticFaultInjectionTest2.py
#///
#/// This Python script verifies that Apex register test
#/// (ApexDiagArm.cpp: TestRegister()) works properly.
#/// Register content is moved to another register
#//  (register write operation takes place)
#/// then teq instruction checks of mov was successful,
#/// result of teq is changed to simulate fault. Since there
#/// is no way to force the mov instruction to act wrong,
#/// the teq instruction result is changed.
#///
#/// @if REVISION_HISTORY_INCLUDED
#/// @par Edit History
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
    ;; Start Fault Injection Point 5
    ;; End Fault Injection Point 5
;; Fault Injection Code Start
        LDR     r3, =InjectFaultFlag
        LDR     r3, [r3]
        CMP     r3, #1
;; Jump to return false only if InjectFaultFlag is set
        BEQ     ArmRegisterR1ReturnFalse
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