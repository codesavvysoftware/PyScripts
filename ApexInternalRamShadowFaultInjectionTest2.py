#/////////////////////////////////////////////////////////////////////////////
#/// @file ApexInternalRamDataDiagnosticWithShadowRamTestsFaultInjectionTest2.py
#///
#/// This Python script verifies that Apex data pattern testing diagnostic is
#/// correctly indicating coupling faults. The injection code is inserted during
#/// run-time to simulate coupling fault. After patterns are written
#/// and successfully checked, the modified firmware will create an ECC error
#/// in one bit of the shadow area. This failure should be detected
#/// and the system should go into the safe-state.
#///
#/// @if REVISION_HISTORY_INCLUDED
#/// @par Edit History
#/// pgrzywn 30-SEP-2013 Created.
#/// spolke  03-OCT-2013 Comment updated.
#/// pszramo 21-OCT-2013 Modified to match updated faultInjectionUtils.
#/// pszramo 08-NOV-2013 Updated description and formatting.
#/// pszramo 09-DEC-2013 Adjustments after MISRA fixes.
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
    'ApexDiagRAMassy.s': [ \
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    ;Start Fault Injection Point 7
    ;End Fault Injection Point 7
                ;Fault Injection Code Start
                IMPORT  InjectFaultFlag
                ;Fault Injection Code End
    ''',
    # # # # # # # # # # # # # # # # # # # # # # # # #
    '''
    ;Start Fault Injection Point 2
    ;End Fault Injection Point 2
        ;Fault Injection Code Start
        STMFD   sp!, {r6, r7}
        LDR     r6, =InjectFaultFlag
        LDR     r7, [r6]
        CMP     r7, #1
        BNE     WithoutFaultInjection
        ;Actual fault injection
        MOV     r1, r2
        SUB     r1, r1, #DGN_RAM_SPACE_START
        ORR     r1, r1, #DGN_ECC_ERR_MASK_SINGLE
WithoutFaultInjection
        LDMFD   sp!, {r6, r7}
        ;Fault Injection Code End
    '''
    ],
    'ApexDiagRamData.cpp': [ \
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
    '''
    ]
}

# Call the procedure to modify and build the test firmware code with the
# above modifications.
faultInjectionUtils.FaultInjectionUtils().ModifyAndBuildFaultInjectionFile(fileModificationsDictionary, __file__)